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

## Results

Below is a summary of the performance of the Whisper `medium`, `large-v3`, and `large-v3-turbo` models across all datasets. The results are presented for two conditions: **Standard** (no contextual prompt) and **Prompted** (using an oracle prompt with the correct jargon).

The best result for each metric within a given dataset and condition is marked in **bold**.

| Language       | Dataset          | Condition | Model            |   WER ↓   |  B-WER ↓  |   U-WER ↓    |   MER ↓   |    WIL ↓     |
|:---------------|:-----------------|:----------|:-----------------|:---------:|:---------:|:------------:|:---------:|:------------:|
| **English**    | **CHiME-6**      | Standard  | `medium`         |   0.382   |  0.811    |    0.416     |   0.367   |    0.330     |
|                |                  |           | `large-v3`       | **0.362** | **0.785** |  **0.402**   | **0.347** |    0.308     |
|                |                  |           | `large-v3-turbo` |   0.377   |   0.868   |    0.425     |   0.354   |  **0.303**   |
|                |                  | Prompted  | `medium`         | **0.359** | **0.377** |    0.428     | **0.338** |  **0.279**   |
|                |                  |           | `large-v3`       |   0.373   |   0.746   |    0.437     |   0.355   |    0.306     |
|                |                  |           | `large-v3-turbo` |   0.409   |   0.522   |  **0.411**   |   0.340   |    0.280     |
|                | **Earnings-22**  | Standard  | `medium`         |   0.292   |   0.786   |    0.278     |   0.264   |    0.217     |
|                |                  |           | `large-v3`       |   0.267   | **0.750** |    0.248     | **0.243** |  **0.199**   |
|                |                  |           | `large-v3-turbo` | **0.266** |   0.836   |  **0.241**   |   0.251   |    0.204     |
|                |                  | Prompted  | `medium`         |   0.254   | **0.417** |    0.271     |   0.238   |    0.187     |
|                |                  |           | `large-v3`       | **0.251** |   0.709   |  **0.242**   |   0.237   |    0.191     |
|                |                  |           | `large-v3-turbo` |   0.257   |   0.564   |    0.258     | **0.230** |  **0.182**   |
|                | **FLEURS**       | Standard  | `medium`         |   0.116   |   0.663   |    0.085     |   0.111   |    0.100     |
|                |                  |           | `large-v3`       | **0.107** | **0.587** |    0.078     | **0.102** |  **0.090**   |
|                |                  |           | `large-v3-turbo` |   0.112   |   0.760   |  **0.077**   |   0.108   |    0.098     |
|                |                  | Prompted  | `medium`         | **0.083** | **0.250** |    0.076     | **0.080** |  **0.068**   |
|                |                  |           | `large-v3`       |   0.095   |   0.509   |  **0.073**   |   0.091   |    0.079     |
|                |                  |           | `large-v3-turbo` |   0.093   |   0.419   |    0.080     |   0.089   |    0.078     |
|                | **SPGISpeech**   | Standard  | `medium`         |   0.099   |   0.745   |    0.084     |   0.078   |    0.066     |
|                |                  |           | `large-v3`       | **0.071** | **0.725** |  **0.053**   | **0.070** |  **0.059**   |
|                |                  |           | `large-v3-turbo` |   0.081   |   0.903   |    0.057     |   0.079   |    0.068     |
|                |                  | Prompted  | `medium`         |   0.099   | **0.248** |    0.101     |   0.068   |    0.052     |
|                |                  |           | `large-v3`       |   0.072   |   0.692   |  **0.056**   |   0.071   |    0.059     |
|                |                  |           | `large-v3-turbo` | **0.068** |   0.434   |    0.062     | **0.064** |  **0.051**   |
|                | **Synth. Terms** | Standard  | `medium`         |   0.215   |   0.704   |    0.140     |   0.197   |    0.169     |
|                |                  |           | `large-v3`       | **0.189** | **0.647** |  **0.119**   | **0.172** |  **0.146**   |
|                |                  |           | `large-v3-turbo` |   0.194   |   0.662   |    0.122     |   0.177   |    0.150     |
|                |                  | Prompted  | `medium`         | **0.072** | **0.196** |    0.062     | **0.071** |  **0.053**   |
|                |                  |           | `large-v3`       |   0.148   |   0.519   |    0.100     |   0.139   |    0.117     |
|                |                  |           | `large-v3-turbo` |   0.074   |   0.221   |  **0.057**   | **0.071** |    0.055     |
|                | **Wikidata**     | Standard  | `medium`         |   0.265   |   0.879   |    0.186     |   0.244   |    0.218     |
|                |                  |           | `large-v3`       | **0.246** | **0.859** |    0.167     | **0.229** |  **0.205**   |
|                |                  |           | `large-v3-turbo` |   0.247   |   0.869   |  **0.163**   |   0.230   |    0.206     |
|                |                  | Prompted  | `medium`         | **0.141** | **0.386** |  **0.133**   | **0.132** |  **0.105**   |
|                |                  |           | `large-v3`       |   0.196   |   0.671   |    0.144     |   0.183   |    0.158     |
|                |                  |           | `large-v3-turbo` |   0.176   |   0.573   |    0.135     |   0.163   |    0.142     |
|                | **GLOBE**        | Standard  | `medium`         |   0.182   |   0.648   |    0.142     |   0.167   |    0.156     |
|                |                  |           | `large-v3`       |   0.178   |   0.859   |    0.110     |   0.171   |    0.162     |
|                |                  |           | `large-v3-turbo` | **0.148** | **0.631** |  **0.101**   | **0.141** |  **0.133**   |
|                |                  | Prompted  | `medium`         | **0.101** | **0.208** |    0.111     |   0.097   |    0.084     |
|                |                  |           | `large-v3`       |   0.148   |   0.711   |    0.099     |   0.142   |    0.134     |
|                |                  |           | `large-v3-turbo` | **0.101** |   0.316   |  **0.095**   | **0.092** |  **0.083**   |
| **Portuguese** | **CORAA**        | Standard  | `medium`         |   0.483   |   0.741   |    0.488     |   0.404   |    0.362     |
|                |                  |           | `large-v3`       | **0.344** | **0.640** |  **0.335**   | **0.309** |  **0.267**   |
|                |                  |           | `large-v3-turbo` |   0.400   |   0.835   |    0.356     |   0.358   |    0.313     |
|                |                  | Prompted  | `medium`         |   0.369   | **0.351** |    0.415     |   0.332   |    0.279     |
|                |                  |           | `large-v3`       | **0.320** |   0.548   |  **0.321**   | **0.291** |  **0.247**   |
|                |                  |           | `large-v3-turbo` |   0.343   |   0.484   |    0.367     |   0.323   |    0.272     |
|                | **FLEURS**       | Standard  | `medium`         |   0.145   |   0.634   |    0.108     |   0.122   |    0.110     |
|                |                  |           | `large-v3`       | **0.091** | **0.535** |  **0.057**   | **0.089** |  **0.081**   |
|                |                  |           | `large-v3-turbo` |   0.105   |   0.649   |    0.068     |   0.101   |    0.092     |
|                |                  | Prompted  | `medium`         | **0.081** | **0.206** |    0.076     |   0.079   |    0.071     |
|                |                  |           | `large-v3`       |   0.108   |   0.441   |    0.092     |   0.083   |    0.075     |
|                |                  |           | `large-v3-turbo` |   0.084   |   0.314   |  **0.069**   | **0.078** |  **0.069**   |
|                | **LapsBM**       | Standard  | `medium`         |   0.150   |   0.693   |    0.103     |   0.145   |    0.131     |
|                |                  |           | `large-v3`       | **0.128** | **0.466** |  **0.078**   | **0.124** |  **0.108**   |
|                |                  |           | `large-v3-turbo` |   0.143   |   0.852   |    0.102     |   0.141   |    0.127     |
|                |                  | Prompted  | `medium`         | **0.069** | **0.045** |    0.074     | **0.067** |  **0.055**   |
|                |                  |           | `large-v3`       |   0.109   |   0.398   |    0.085     |   0.106   |    0.093     |
|                |                  |           | `large-v3-turbo` |   0.082   |   0.216   |  **0.070**   |   0.080   |    0.065     |
|                | **Synth. Terms** | Standard  | `medium`         |   0.216   |   0.832   |    0.132     |   0.197   |    0.166     |
|                |                  |           | `large-v3`       |   0.197   |   0.773   |    0.117     |   0.179   |    0.148     |
|                |                  |           | `large-v3-turbo` | **0.193** | **0.749** |  **0.115**   | **0.176** |  **0.146**   |
|                |                  | Prompted  | `medium`         | **0.071** | **0.136** |    0.072     | **0.069** |  **0.046**   |
|                |                  |           | `large-v3`       |   0.138   |   0.548   |    0.088     |   0.130   |    0.104     |
|                |                  |           | `large-v3-turbo` |   0.077   |   0.214   |  **0.060**   |   0.073   |    0.055     |
|                | **Wikidata**     | Standard  | `medium`         |   0.183   |   0.777   |    0.091     |   0.178   |    0.163     |
|                |                  |           | `large-v3`       | **0.165** | **0.730** |    0.071     | **0.161** |  **0.148**   |
|                |                  |           | `large-v3-turbo` |   0.165   |   0.750   |  **0.066**   |   0.162   |    0.150     |
|                |                  | Prompted  | `medium`         | **0.068** | **0.216** |    0.061     | **0.066** |  **0.054**   |
|                |                  |           | `large-v3`       |   0.110   |   0.507   |  **0.052**   |   0.108   |    0.099     |
|                |                  |           | `large-v3-turbo` |   0.083   |   0.315   |  **0.052**   |   0.081   |    0.073     |

---

## How to Cite

To cite this work, please use the following BibTeX entry: TBA