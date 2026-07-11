# Data Directory Information

This directory contains the novel contributions of our work: the annotation files for literature-derived datasets and novel datasets.

## `original_datasets/`

The four novel datasets created for this work:

| Subset | Language |
|---|---|
| `synthetic_terms/` | English |
| `synthetic_terms_pt/` | Portuguese |
| `wikidata_synthetic/` | English |
| `wikidata_synthetic_pt/` | Portuguese |

Each folder has `data.xlsx` (text, target terms, IPA, audio path) and `audio/*.wav`. Full audio is hosted on Hugging Face — see the top-level README for the link.

## `literature_annotations/`

Jargon-term annotations for samples from existing literature datasets:
- [FLEURS (English and Portuguese)](https://huggingface.co/datasets/google/fleurs)
- [CHIME6](https://huggingface.co/datasets/DynamicSuperb/SuperbOODAsrSpon_CHIME6-Test)
- [CORAA](https://huggingface.co/datasets/nilc-nlp/CORAA-MUPE-ASR)
- [Earnings22](https://huggingface.co/datasets/sanchit-gandhi/earnings22_split)
- [LapsBM](https://huggingface.co/datasets/laudite-ufg/laps_bm)
- [SPGISpeech](https://huggingface.co/datasets/kensho/spgispeech)
- [GLOBE](https://huggingface.co/datasets/MushanW/GLOBE)

It **does not** contain the original, large audio corpora from other sources due to **licensing restrictions** and **file size**.

The script `scripts/1_prepare_datasets.py` will automatically fetch the data and cache it locally. It is necessary to run this script before executing experiments.
