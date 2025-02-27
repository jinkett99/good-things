# **Good Things** – Automatic Speech Recognition (ASR) Repository  
*"Good things must share."*

This repository contains scripts and implementations for various **Automatic Speech Recognition (ASR) tasks**, including model deployment, fine-tuning, hot-word detection, and self-supervised learning.

---

## **Setup Instructions**  

Follow these steps in the specified order to run the scripts successfully:

### **1. Clone the Repository**  
```bash
git clone https://github.com/jinkett99/good-things.git
cd good-things
```

### **2. Install Dependencies**  
```bash
pip install -r requirements.txt
```

---

## **[Question 2] Deploying an ASR Micro-Service**  
**📂 Directory:** `asr`  
This module sets up a FastAPI microservice for ASR model inference.

### **2(a) Start the ASR Micro-Service**  
```bash
cd asr
uvicorn asr_api:app --port 8001 --reload
```
**API Docs:** [`http://localhost:8001/docs`](http://localhost:8001/docs)

### **2(b) Test the Micro-Service**  
Check service availability:  
```bash
curl http://localhost:8001/ping
```
Expected output: `"pong"`

### **2(c) Run ASR Inference on an Audio File**  
```bash
curl -F "file=@./cv-valid-dev/sample-000000.mp3;type=audio/mpeg" http://localhost:8001/asr
```
Returns transcription output.

### **2(d) Batch Process Audio Files**  
```bash
python cv-decode.py
```
- Sends POST requests to the ASR inference endpoint.  
- Transcribes `.mp3` files in the `cv-valid-dev` folder.  
- Overwrites `cv-valid-dev.csv` with generated text.

### **2(e) Deploy the API in Docker**  
1. **Build Docker Image**  
   ```bash
   cd app
   docker build -t asr-api .
   ```
   *(Ensure Docker daemon is running.)*

2. **Run the Docker Container**  
   ```bash
   docker run -p 8001:8001 asr-api
   ```
   - Spins up the ASR inference API at [`http://localhost:8001/asr`](http://localhost:8001/asr).
   
**Dataset Download:**  
The Common Voice dataset is **not included** in the repo for efficiency. Download it here:  
📥 [Common Voice Dataset](https://www.dropbox.com/scl/fi/i9yvfqpf7p8uye5o8k1sj/common_voice.zip?rlkey=lz3dtjuhekc3xw4jnoeoqy5yu&dl=0)

---

## **[Questions 3 & 4] Fine-Tuning an ASR Model**  
**📂 Directory:** `asr_train`  
This module covers model exploration, data preprocessing, feature engineering, tokenizer building, fine-tuning, evaluation, and inference.

### **3(a) Full Fine-Tuning Script**  
Notebook: `cv-train-2a.ipynb`

### **3(b) Access Fine-Tuned Model Checkpoint**  
Model: `wav2vec2-large-960h-cv`

### **3(c) Training Logs & Metrics**  
- Training, validation, and evaluation metrics (WER) are logged.  
- Inference performance across test sets is available.

### **Running Locally vs. Google Colab**  
For local execution, **remove `/content/drive/MyDrive/Colab Notebooks/wav2vec2-finetune/`** from file paths.  

**Dataset Download:**  
The Common Voice dataset is **not included** in the repo for efficiency. Download it here:  
📥 [Common Voice Dataset](https://www.dropbox.com/scl/fi/i9yvfqpf7p8uye5o8k1sj/common_voice.zip?rlkey=lz3dtjuhekc3xw4jnoeoqy5yu&dl=0)

### **[Question 4] Baseline vs. Fine-Tuned Model Report**  
📄 **Report:** `training-report.pdf` (Main repository)

---

## **[Question 5] Hot-Word Detection & Context Similarity**  
**📂 Directory:** `hotword-detection`  
This module detects hot-words in transcribed text and uses text embeddings for context similarity analysis.

### **5(a) Run Hot-Word Detection**  
Notebook: `cv-hotword-5a.ipynb`  
- Detects hot-words in transcriptions.  
- Outputs corresponding `.mp3` filenames into `detected.txt`.

### **5(b) Detect Similar Phrases to Hot-Words**  
Notebook: `cv-hotword-similarity-5b.ipynb`  
- Uses **HuggingFace's** `"hkunlp/instructor-large"` text embedding model.  
- Adds similarity indicators to the original transcription dataset.

### **Running Locally vs. Google Colab**  
For local execution, **remove `/content/drive/MyDrive/Colab Notebooks/hotword-detection/`** from file paths.  

---

## **[Question 6] Self-Supervised Learning (SSL) for ASR**  
**📄 Article Review:** `essay-ssl.pdf` (Main repository)  
- Proposes an SSL pipeline for ASR focusing on **dysarthric speech**.  
- Draws insights from *"Deploying Self-Supervised Learning in the Wild for Hybrid ASR"*.

---

## **Contributing**  
Feel free to open issues and submit pull requests. Contributions are welcome!

