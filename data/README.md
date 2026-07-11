# Data Directory Information

This directory contains the novel contributions of our work: annotation
files for literature-derived datasets, and the full novel datasets we
created ourselves.

License: all data here is released under **CC BY 4.0** — see `LICENSE` in
this directory for details and provenance notes.

## `original_datasets/` — novel synthetic datasets (full audio + text)

These four subsets are entirely our own work (LLM-generated terms and/or
Wikidata-sourced terms, synthesized with KokoroTTS) and are freely
redistributable:

| Subset | Language | Description |
|---|---|---|
| `synthetic_terms/` | English | ~520 utterances with entirely novel, 100% OOV, LLM-generated technical terms |
| `synthetic_terms_pt/` | Portuguese | ~520 utterances, Portuguese equivalent |
| `wikidata_synthetic/` | English | ~5,270 utterances embedding foreign-origin proper nouns sourced from Wikidata |
| `wikidata_synthetic_pt/` | Portuguese | ~5,250 utterances, Portuguese equivalent (via Phonetic Approximation in Brazilian Portuguese) |

Each subset folder contains:
- `audio/` — the `.wav` files (not tracked in git — see "Getting the audio" below)
- `data.xlsx` — human-readable metadata: id, sentence text, target terms, IPA transcriptions, audio path, TTS voice/speed/language