import warnings
import jiwer
from tqdm import tqdm
import Levenshtein
import gc
import ijson
import numpy as np
import torch
import whisper


def find_best_matching_subsequence(seq: list[str], target: list[str]):
    """
    Finds the contiguous subsequence of seq (of length equal to target)
    that have the smallest Levenshtein distance to target.

    Returns:
        tuple: (best_subsequence: list[str], min_distance: int)
    """
    len_seq = len(seq)
    len_target = len(target)

    if len_seq == 0:
        # If the input sequence is empty, the distance is the length of the target (as string)
        return [], len(" ".join(target))

    min_dist = float('inf')
    best_subseq = []

    # Slide a window of size len_target over the input sequence
    if len_seq >= len_target:
        for start in range(len_seq - len_target + 1):
            window = seq[start:start + len_target]
            dist = Levenshtein.distance(" ".join(window), " ".join(target))

            if dist < min_dist:
                min_dist = dist
                best_subseq = window
    else:
        # If the target is longer than the input sequence, compare the entire sequence
        dist = Levenshtein.distance(" ".join(seq), " ".join(target))
        best_subseq = seq
        min_dist = dist

    return best_subseq, min_dist


def is_subsequence(subsequence, sequence):
    """ Check if subsequence is a contiguous subsequence of sequence. """
    n = len(subsequence)
    return any(subsequence == sequence[i:i + n] for i in range(len(sequence) - n + 1))


transforms = jiwer.Compose(
    [
        jiwer.ExpandCommonEnglishContractions(),
        jiwer.RemoveEmptyStrings(),
        jiwer.ToLowerCase(),
        jiwer.RemoveMultipleSpaces(),
        jiwer.Strip(),
        jiwer.RemovePunctuation(),
        jiwer.ReduceToListOfListOfWords(),
    ]
)


def normalize_and_tokenize(text: str) -> list[str]:
    tokens = transforms(str(text))
    return tokens[0] if tokens else []


def normalize(text: str) -> str:
    _transforms = jiwer.Compose(
        [
            jiwer.ExpandCommonEnglishContractions(),
            jiwer.RemoveEmptyStrings(),
            jiwer.ToLowerCase(),
            jiwer.RemoveMultipleSpaces(),
            jiwer.Strip(),
            jiwer.RemovePunctuation(),
        ]
    )
    return _transforms(str(text))


def compute_wers(prediction: str, transcription: str, target_words: list[str]) -> dict[str, float]:
    """ Computes the WER, B-WER and U-WER for a single prediction. """

    biased_words = target_words  # The target words are the biased words.

    # Compute the WER
    wer_value = jiwer.wer(
        [transcription],
        [prediction],
        truth_transform=transforms,
        hypothesis_transform=transforms
    )

    # Compute the B-WER and U-WER
    """ The B-WER and U-WER have a limitation in relation to repetitive target words in the prediction.
        In this case, it is used the best subsequence of the target word prediction that matches the reference
        target words, ignoring the repetitions that should be more distant from the reference target word.
    """

    normalized_ref = normalize(transcription)
    normalized_pred = normalize(prediction)

    normalized_pred_tokens = normalize_and_tokenize(prediction)

    u_pred_calc = normalized_pred
    u_ref_calc = normalized_ref
    b_pred_calc = ""
    b_ref_calc = ""

    tokenized_normalized_ref = transforms([normalized_ref])[0]
    for biased_word in biased_words:
        normalized_b_word = normalize(biased_word)
        normalized_b_word_tokens = normalize_and_tokenize(biased_word)

        # For each biased word in reference, add the biased term in the b_pred and b_ref to calculate b-wer
        # and remove the biased term from the u_pred and u_ref to calculate u-wer
        if is_subsequence(normalized_b_word_tokens, tokenized_normalized_ref):
            # Find most common sequence of biased tokens in the reference
            best_subseq, _d = find_best_matching_subsequence(normalized_pred_tokens,
                                                             normalized_b_word_tokens)

            # Add the biased terms for b-wer
            # Add the best subsequence to the biased prediction words
            biased_pred = " ".join(best_subseq)
            b_pred_calc += " " + biased_pred
            b_pred_calc = b_pred_calc.strip()
            # Add the normalized_b_word to the biased reference words
            b_ref_calc += " " + normalized_b_word
            b_ref_calc = b_ref_calc.strip()

            # Remove the biased terms for u-wer
            # Remove the biased_pred from the u_pred_calc
            u_pred_calc = u_pred_calc.replace(biased_pred, "").strip()
            # Remove the normalized_b_word from the u_ref_calc
            u_ref_calc = u_ref_calc.replace(normalized_b_word, "").strip()
        else:
            continue

    if b_ref_calc.replace(" ", "").replace("\n", "") == "":
        # It means that no biased words were found in the reference.
        warnings.warn(f"B-WER reference is empty. Setting B-WER to 0.")
        b_wer_value = 0.0
    elif b_pred_calc.replace(" ", "").replace("\n", "") == "":
        # In this case, the prediction is empty. This means that the model didn't transcribe any biased words.
        # However, this situation is not expected to happen, once best_subseq should
        # have the same size of the normalized_b_word_tokens.
        b_wer_value = 1.0
        warnings.warn("B-WER prediction is empty. Setting B-WER to 1. IT IS NOT EXPECTED TO HAPPEN.")
        print(f"Prediction: {prediction}\n transcription: {transcription}\n target_words: {target_words}\n")
    else:

        b_wer_value = jiwer.wer(
            [b_ref_calc],
            [b_pred_calc],
            truth_transform=transforms,
            hypothesis_transform=transforms
        )

    if u_ref_calc.replace(" ", "").replace("\n", "") == "":
        # It means that the reference is empty or all the words were biased.
        warnings.warn("U-WER reference is empty. Setting U-WER to 0.")
        u_wer_value = 0.0
    elif u_pred_calc.replace(" ", "").replace("\n", "") == "":
        # In this case, the unbiased prediction is empty. This means that the model didn't transcribe anything
        # or only biased words.
        u_wer_value = 1.0  # I think it should be 1.0, once the previous condition was false, that means there
        # are words in the reference that is not biased and the model should predict them.
        warnings.warn("U-WER prediction is empty. Setting U-WER to 1.")
    else:
        u_wer_value = jiwer.wer(
            [u_ref_calc],
            [u_pred_calc],
            truth_transform=transforms,
            hypothesis_transform=transforms
        )

    return {
        "WER": wer_value,
        "B-WER": b_wer_value,
        "U-WER": u_wer_value
    }


_TFM = jiwer.Compose([
    jiwer.ExpandCommonEnglishContractions(),
    jiwer.RemoveEmptyStrings(),
    jiwer.ToLowerCase(),
    jiwer.RemoveMultipleSpaces(),
    jiwer.Strip(),
    jiwer.RemovePunctuation(),
    jiwer.ReduceToListOfListOfWords(),
])


def _stats(ref: str, hyp: str):
    m = jiwer.compute_measures(
        ref, hyp,
        truth_transform=_TFM,
        hypothesis_transform=_TFM
    )
    H = m["hits"]
    S = m["substitutions"]
    D = m["deletions"]
    I = m["insertions"]

    len_ref = len(_TFM([ref])[0])
    len_hyp = len(_TFM([hyp])[0])

    return H, S, D, I, len_ref, len_hyp


def compute_mer(prediction: str, transcription: str) -> float:
    _, S, D, I, _, _ = _stats(transcription, prediction)
    N = S + D + I + _stats(transcription, prediction)[0]  # H+S+D+I
    mer = (S + D + I) / N if N else 0.0
    return mer


def compute_wil(prediction: str, transcription: str) -> float:
    H, S, D, I, N1, N2 = _stats(transcription, prediction)
    wil = 1.0 - (2 * H) / (N1 + N2) if (N1 + N2) else 0.0
    return wil


test_datasets = {
    'synthetic_en': {
        "path": "original/synthetic_terms/dataset.json",
        "language": "en",
    },
    'synthetic_pt': {
        "path": "original/synthetic_terms_pt/dataset.json",
        "language": "pt",
    },
    'wikidata_en': {
        "path": "original/wikidata_synthetic/dataset.json",
        "language": "en",
    },
    'wikidata_pt': {
        "path": "original/wikidata_synthetic_pt/dataset.json",
        "language": "pt",
    },
    'fleurs_en_train': {
        "path": "literature/fleurs_en_train.json",
        "language": "en",
    },
    'fleurs_pt_train': {
        "path": "literature/fleurs_pt_train.json",
        "language": "pt",
    },
    'chime6': {
        "path": "literature/chime6.json",
        "language": "en",
    },
    'CORAA': {
        "path": "literature/CORAA.json",
        "language": "pt",
    },
    'earnings22': {
        "path": "literature/earnings22.json",
        "language": "en",
    },
    'laps_bm': {
        "path": "literature/laps_bm_train.json",
        "language": "pt",
    },
    'spgispeech': {
        "path": "literature/spgispeech_dev.json",
        "language": "en",
    },
    'globe': {
        "path": "literature/globe.json",
        "language": "en",
    },
}



def make_prediction(model, device, audio_array, audio_sampling_rate, target_words, language, use_prompt):
    transcribe_args = {
        "language": language if language else None,
        "task": "transcribe",
        "temperature": 0.0,
    }

    if use_prompt:
        prompt = ', '.join(target_words)
        transcribe_args["initial_prompt"] = prompt

    # To ndarray
    audio_array = np.array(audio_array).astype(np.float32)

    transcription = model.transcribe(audio_array, **transcribe_args)
    transcription = transcription['text'].strip()
    return transcription


# whisper_model_sizes = ["tiny", "base", "small", "medium", "large-v3"]
whisper_model_sizes = ["medium", "large-v3", "large-v3-turbo"]

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

for model_size in whisper_model_sizes:
    print(f"\nUsing Whisper model size: {model_size}...")
    model = whisper.load_model(model_size, device=device)

    for dataset_name in test_datasets:
        print(f"\n\tTesting {dataset_name}...")

        results = {
            "WER": [], "B-WER": [], "U-WER": [], "MER": [], "WIL": []
        }
        results_prompt = {
            "WER": [], "B-WER": [], "U-WER": [], "MER": [], "WIL": []
        }

        file_path = test_datasets[dataset_name]['path']
        language = test_datasets[dataset_name]['language']
        _target_word_column = 'target_word' if dataset_name != 'globe' else 'target_words'

        with open(file_path, "r", encoding='utf-8') as f:
            dataset_generator = ijson.items(f, 'item')

            for i, sample in enumerate(tqdm(dataset_generator)):
                target_words = sample[_target_word_column]
                if not target_words:
                    continue
                if isinstance(target_words, str):
                    target_words = target_words.split(',')
                target_words = [w.strip() for w in target_words if w.strip()]

                for use_prompt in [False, True]:
                    prediction = make_prediction(model, device, sample['audio_array'], sample['audio_sampling_rate'],
                                                 target_words, language, use_prompt)
                    transcription = sample['transcription']
                    wers = compute_wers(prediction, transcription, target_words)
                    mer = compute_mer(prediction, transcription)
                    wil = compute_wil(prediction, transcription)
                    if use_prompt:
                        results_prompt["WER"].append(wers["WER"])
                        results_prompt["B-WER"].append(wers["B-WER"])
                        results_prompt["U-WER"].append(wers["U-WER"])
                        results_prompt["MER"].append(mer)
                        results_prompt["WIL"].append(wil)
                    else:
                        results["WER"].append(wers["WER"])
                        results["B-WER"].append(wers["B-WER"])
                        results["U-WER"].append(wers["U-WER"])
                        results["MER"].append(mer)
                        results["WIL"].append(wil)

                    del prediction, transcription, wers, mer, wil

            if device == "cuda":
                torch.cuda.empty_cache()
            gc.collect()

        # Compute average results
        avg_results = {metric: sum(values) / len(values) if values else 0.0 for metric, values in results.items()}
        print(f"\t\tAverage results for {dataset_name}({model_size}): {avg_results}")
        avg_prompt_results = {metric: sum(values) / len(values) if values else 0.0 for metric, values in results_prompt.items()}
        print(f"\t\tAverage results with prompt for {dataset_name}({model_size}): {avg_prompt_results}")

        gc.collect()

    del model
    if device == "cuda":
        torch.cuda.empty_cache()
    gc.collect()