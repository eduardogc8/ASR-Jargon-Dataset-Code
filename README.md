# A Dataset for Evaluating ASR on Specialized Vocabulary

This repository contains the official code for the paper: **"A Dataset for Evaluating ASR on Specialized Vocabulary"**.

Here, you can find the scripts to reproduce all experiments, including the baseline evaluations on our novel jargon-focused ASR datasets.

---

## Datasets on Hugging Face

All novel datasets presented in this work will be publicly available on the Hugging Face Hub.

* **Link to Dataset:** TBA

---

## How to Reproduce Our Results

The process involves two main steps: automatically downloading the datasets and then running the evaluation script.

### **Step 1: Download and Prepare Datasets**

The `1_prepare_datasets.py` script automatically download and cache all the required data.

### **Step 2: Run Experiments**

This script runs the full evaluation using the Whisper models on all datasets. The results (WER, B-WER, etc.) will be printed to the console.

---

## How to Cite

To cite this work, please use the following BibTeX entry: TBA