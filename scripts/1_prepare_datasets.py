from tqdm import tqdm
from datasets import load_dataset
import pandas as pd
import json

annotated_tables = [
    '..data/literature_annotations/fleurs_en_train.csv',
    '..data/literature_annotations/fleurs_pt_train.csv',
    '..data/literature_annotations/chime6.csv',
    '..data/literature_annotations/CORAA.csv',
    '..data/literature_annotations/earnings22.csv',
    '..data/literature_annotations/laps_bm_train.csv',
    '..data/literature_annotations/spgispeech_dev.csv',
    '..data/literature_annotations/globe.csv',
]


def extract_fleurs_data(ids, language):
    fleurs = load_dataset("google/fleurs", language, split="train", streaming=True)

    selected_samples = []

    pbar = tqdm(enumerate(fleurs))
    total_ids = len(ids)
    for i, sample in pbar:

        pbar.set_description(f"[{i}]\t{len(ids)}/{total_ids}({(100 - (len(ids) / total_ids * 100)):.2f}%)")
        dataset_id = sample["id"]
        if dataset_id not in ids:
            continue
        d = {
            'dataset_id': dataset_id,
            'transcription': sample['transcription'],
            'audio_array': list(sample['audio']['array']),
            'audio_sampling_rate': sample['audio']['sampling_rate'],
        }
        selected_samples.append(d)
        ids.remove(dataset_id)

        if len(ids) == 0:
            pbar.set_description(f"[{i}]\t{len(ids)}/{total_ids}({(100 - (len(ids) / total_ids * 100)):.2f}%)")
            break

    return selected_samples


def extract_chime6(ids):
    dataset = load_dataset("DynamicSuperb/SuperbOODAsrSpon_CHIME6-Test", split="test").shuffle(seed=42)
    selected_samples = []

    pbar = tqdm(enumerate(dataset))
    total_ids = len(ids)
    for i, sample in pbar:
        pbar.set_description(f"[{i}]\t{len(ids)}/{total_ids}({(100 - (len(ids) / total_ids * 100)):.2f}%)")
        dataset_id = sample["file"]
        if dataset_id not in ids:
            continue

        d = {
            'dataset_id': dataset_id,
            'transcription': sample['label'],
            'audio_array': list(sample['audio']['array']),
            'audio_sampling_rate': sample['audio']['sampling_rate'],
        }
        selected_samples.append(d)
        ids.remove(dataset_id)
        if len(ids) == 0:
            pbar.set_description(f"[{i}]\t{len(ids)}/{total_ids}({(100 - (len(ids) / total_ids * 100)):.2f}%)")
            break

    return selected_samples


def extract_coraa(ids):
    dataset = load_dataset("nilc-nlp/CORAA-MUPE-ASR", split="train", streaming=True)
    selected_samples = []

    pbar = tqdm(enumerate(dataset))
    total_ids = len(ids)
    for i, sample in pbar:
        pbar.set_description(f"[{i}]\t{len(ids)}/{total_ids}({(100 - (len(ids) / total_ids * 100)):.2f}%)")
        dataset_id = sample["file_path"].replace('/', '_')
        if dataset_id not in ids:
            continue

        d = {
            'dataset_id': dataset_id,
            'transcription': sample['original_text'],
            'audio_array': list(sample['audio']['array']),
            'audio_sampling_rate': sample['audio']['sampling_rate'],
        }
        selected_samples.append(d)
        ids.remove(dataset_id)
        if len(ids) == 0:
            pbar.set_description(f"[{i}]\t{len(ids)}/{total_ids}({(100 - (len(ids) / total_ids * 100)):.2f}%)")
            break

    return selected_samples


def extract_earnings22(ids):
    dataset = load_dataset("sanchit-gandhi/earnings22_split", split="train", streaming=True)
    selected_samples = []

    pbar = tqdm(enumerate(dataset))
    total_ids = len(ids)
    for i, sample in pbar:
        pbar.set_description(f"[{i}]\t{len(ids)}/{total_ids}({(100 - (len(ids) / total_ids * 100)):.2f}%)")
        dataset_id = sample['id']
        if dataset_id not in ids:
            continue

        d = {
            'dataset_id': dataset_id,
            'transcription': sample['sentence'],
            'audio_array': list(sample['audio']['array']),
            'audio_sampling_rate': sample['audio']['sampling_rate'],
        }
        selected_samples.append(d)
        ids.remove(dataset_id)
        if len(ids) == 0:
            pbar.set_description(f"[{i}]\t{len(ids)}/{total_ids}({(100 - (len(ids) / total_ids * 100)):.2f}%)")
            break

    return selected_samples


def extract_laps_bm(ids):
    dataset = load_dataset("laudite-ufg/laps_bm", split="train", streaming=True)
    selected_samples = []

    pbar = tqdm(enumerate(dataset))
    total_ids = len(ids)
    for i, sample in pbar:
        pbar.set_description(f"[{i}]\t{len(ids)}/{total_ids}({(100 - (len(ids) / total_ids * 100)):.2f}%)")
        dataset_id = sample['audio_filename']
        if dataset_id not in ids:
            continue

        d = {
            'dataset_id': dataset_id,
            'transcription': sample['transcription'],
            'audio_array': list(sample['audio']['array']),
            'audio_sampling_rate': sample['audio']['sampling_rate'],
        }
        selected_samples.append(d)
        ids.remove(dataset_id)
        if len(ids) == 0:
            pbar.set_description(f"[{i}]\t{len(ids)}/{total_ids}({(100 - (len(ids) / total_ids * 100)):.2f}%)")
            break

    return selected_samples


def extract_spgispeech(ids):
    selected_samples = []
    total_ids = len(ids)
    dataset = load_dataset("kensho/spgispeech", "dev", split="validation", streaming=True, trust_remote_code=True)
    pbar = tqdm(enumerate(dataset))
    for i, sample in pbar:
        pbar.set_description(f"[{i}]\t{len(ids)}/{total_ids}({(100 - (len(ids) / total_ids * 100)):.2f}%)")
        dataset_id = sample["wav_filename"]  # .replace('/', '')
        if dataset_id not in ids:
            continue

        d = {
            'dataset_id': dataset_id,
            'transcription': sample['transcript'],
            'audio_array': list(sample['audio']['array']),
            'audio_sampling_rate': sample['audio']['sampling_rate'],
        }
        selected_samples.append(d)
        ids.remove(dataset_id)
        if len(ids) == 0:
            pbar.set_description(f"[{i}]\t{len(ids)}/{total_ids}({(100 - (len(ids) / total_ids * 100)):.2f}%)")
            break

    return selected_samples


def extract_globe(ids):
    selected_samples = []
    total_ids = len(ids)
    dataset = load_dataset("MushanW/GLOBE", split="train", streaming=True)
    pbar = tqdm(enumerate(dataset))
    for i, sample in pbar:
        pbar.set_description(f"[{i}]\t{len(ids)}/{total_ids}({(100 - (len(ids) / total_ids * 100)):.2f}%)")
        dataset_id = sample["speaker_id"] + '-' + sample["audio"]["path"]
        if dataset_id not in ids:
            continue

        d = {
            'dataset_id': dataset_id,
            'transcription': sample['transcript'],
            'audio_array': list(sample['audio']['array']),
            'audio_sampling_rate': sample['audio']['sampling_rate'],
        }
        selected_samples.append(d)
        ids.remove(dataset_id)
        if len(ids) == 0:
            pbar.set_description(f"[{i}]\t{len(ids)}/{total_ids}({(100 - (len(ids) / total_ids * 100)):.2f}%)")
            break
    return selected_samples


def combine_annotations(df_annotations, selected_samples, target_word_column='target_word'):
    for i, sample in enumerate(selected_samples):
        df_ = df_annotations[df_annotations['dataset_id'] == sample['dataset_id']]
        if df_.empty:
            print(f"WARNING: no annotations for dataset {sample['dataset_id']}")
            continue

        target_words = df_[target_word_column].tolist()[0]
        selected_samples[i][target_word_column] = target_words
    return selected_samples


if __name__ == "__main__":

    for annotated_table in annotated_tables:
        df = pd.read_csv(annotated_table)
        ids = df["dataset_id"].tolist()
        selected_samples = None

        target_word_column = 'target_word'

        if annotated_table == "fleurs_en_train.csv":
            selected_samples = extract_fleurs_data(ids, language="en_us")
        if annotated_table == "fleurs_pt_train.csv":
            selected_samples = extract_fleurs_data(ids, language="pt_br")
        if annotated_table == "chime6.csv":
            selected_samples = extract_chime6(ids)
        if annotated_table == "CORAA.csv":
            selected_samples = extract_coraa(ids)
        if annotated_table == "earnings22.csv":
            selected_samples = extract_earnings22(ids)
        if annotated_table == "laps_bm_train.csv":
            selected_samples = extract_laps_bm(ids)
        if annotated_table == "spgispeech_dev.csv":
            selected_samples = extract_spgispeech(ids)
        if annotated_table == "globe.csv":
            selected_samples = extract_globe(ids)
            target_word_column = 'target_words'

        if selected_samples is None:
            print(f"WARNING: no annotations for dataset {annotated_table}")
            continue

        # Combine literature dataset data with annotation data (target words)
        selected_samples = combine_annotations(df, selected_samples, target_word_column=target_word_column)

        # Save combine data as json
        with open(annotated_table.replace(".csv", ".json"), "w", encoding="utf-8") as f:
            json.dump(selected_samples, f, indent=4)