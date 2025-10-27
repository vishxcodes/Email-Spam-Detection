# 📧 Email Spam Detector using NLP and Streamlit

This project is an **Email Spam Detection System** built using **Natural Language Processing (NLP)** and **Machine Learning**. It classifies email or SMS text as **Spam** or **Not Spam** using text analysis techniques and a trained ML model.

---

## 🚀 Features
- Preprocesses text using tokenization, stopword removal, punctuation removal, and lemmatization  
- Converts text to numerical features using **TF-IDF Vectorization**  
- Trains multiple ML models (e.g., Logistic Regression, Naive Bayes) for spam detection  
- Provides an interactive **Streamlit web interface** for real-time classification  

---

## 🧠 Tech Stack
- **Python**
- **scikit-learn** – Model training and TF-IDF vectorization  
- **NLTK** – Text preprocessing (tokenization, lemmatization, stopword removal)  
- **pandas, matplotlib, seaborn** – Data analysis and visualization  
- **Streamlit** – Web UI  

---

## 📂 Project Structure
├── PYTHON_PROJECT.ipynb # Model training and preprocessing notebook
├── app.py # Streamlit frontend (to be added)
├── spam_model.pkl # Trained ML model (optional)
├── vectorizer.pkl # TF-IDF vectorizer (optional)
├── requirements.txt # Required Python packages
└── README.md # Project documentation

---

## ⚙️ Installation & Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/email-spam-detector.git
   cd email-spam-detector

2. Install dependencies:
   ```bash
   pip install -r requirements.txt

3. Run the Streamlit app:
    ```bash
    streamlit run app.py

---

## 📊 Model Workflow
- Load and clean dataset
- Convert text to lowercase
- Tokenize and remove stopwords/punctuations
- Apply stemming or lemmatization
- Vectorize text using TF-IDF
- Train and evaluate ML models
- Save trained model using joblib or pickle

## 🧩 Future Enhancements
- Integration with email APIs for real-time detection
- Experiment with deep learning models (e.g., LSTM or BERT)
- Deploy app on Streamlit Cloud or Hugging Face Spaces

## 👨‍💻 Authors
Developed by a team of Computer Engineering students as part of an academic project on NLP and Machine Learning.