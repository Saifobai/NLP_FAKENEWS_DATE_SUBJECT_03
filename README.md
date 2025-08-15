# 📰 Fake News Detection with NLP

A Natural Language Processing (NLP) project that detects fake news using various text embeddings (SBERT, TF-IDF, Bag-of-Words), supervised learning models, and evaluation pipelines.

---

## 📁 Project Structure

```
project-root/
├── dataset/
│   ├── train_data.csv
│   ├── test_data.csv
│   ├── test_labels.csv
│   └── prediction.csv
├── model.pkl
├── model_comparison.csv
├── model_evaluation.txt
├── final_test_evaluation.csv
├── preprocessing.py
├── app.py
├── main.ipynb
└── README.md
```

---

### Model download from here

https://drive.google.com/file/d/15N4QmwZC3WDFeVgBrFdaAIs2ZPMOyPmp/view?usp=drive_link

### Training data download from here

https://drive.google.com/file/d/1W4GH2-KQoo8S73zpytmI5D6kJjd_1TFf/view?usp=drive_link

## ⚙️ Setup & Installation

```bash
# Clone the repository
git clone <repo-url>
cd NLP_FAKENEWS

# Create virtual environment
python -m venv venv
source venv/bin/activate      # or venv\Scriptsctivate on Windows

# Install dependencies
pip install -r requirements.txt
```

### 📦 Example `requirements.txt`

```
pandas
numpy
scikit-learn
nltk
beautifulsoup4
sentence-transformers
joblib
```

---

## 📥 Download Model & Dataset

> ⚠️ Large files such as `model.pkl` (~87 MB) and `dataset/train_data.csv` (~100 MB) are not stored in the repo.  
> Please download them from Google Drive (link provided separately) and place them in:

```
project-root/
├── model.pkl
└── dataset/
    └── train_data.csv
```

---

## 🔄 Pipeline Overview

| Step                   | Description                                                            |
| ---------------------- | ---------------------------------------------------------------------- |
| **1. Data Loading**    | Load CSVs, encode labels (FAKE=0, REAL=1)                              |
| **2. Text Cleaning**   | HTML removal, lowercasing, tokenizing, lemmatization, stopword removal |
| **3. Embedding**       | - SBERT (`all-MiniLM-L6-v2`) <br> - TF-IDF <br> - Bag-of-Words         |
| **4. Model Training**  | Logistic Regression, SGDClassifier over embeddings                     |
| **5. Evaluation**      | Compare models using accuracy, precision, recall, F1                   |
| **6. Save Best Model** | Saved as `model.pkl`                                                   |
| **7. Prediction**      | Predict test labels, export to `dataset/prediction.csv`                |

---

## ▶️ Running the Project

```bash
python app.py
# OR open main.ipynb in Jupyter Notebook to run step-by-step
```

---

## ✅ Output Files

| File                        | Description                                  |
| --------------------------- | -------------------------------------------- |
| `model.pkl`                 | Best-performing SBERT model                  |
| `model_comparison.csv`      | Metrics for each model compared              |
| `dataset/prediction.csv`    | Numeric predictions on test dataset          |
| `final_test_evaluation.csv` | Metrics using `test_labels.csv` if available |

---

## 📝 Notes

- The script auto-downloads required NLTK resources.
- SBERT model download may take time on first run.
- Ensure dataset files are in correct folders before running.

---

## 🚀 Future Improvements

- Perform hyperparameter tuning (GridSearch/Cross-validation)
- Apply dataset augmentation or handle class imbalance
