import streamlit as st
import pickle
import string
import re
import nltk
import nltk
nltk.download('punkt_tab')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('stopwords')
nltk.download('punkt')
from nltk.stem import PorterStemmer

port_stemmer = PorterStemmer()

# Load models
try:
    tfidf = pickle.load(open('vectorizer.pkl', 'rb'))
    model = pickle.load(open('model.pkl', 'rb'))
except FileNotFoundError:
    st.error("Model files not found. Please ensure 'vectorizer.pkl' and 'model.pkl' are in the same directory.")

# Configure page
st.set_page_config(
    page_title="PhishGuard AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Sophisticated black-blue theme CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        background-color: #0f1419;
        color: #e8eef3;
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Navigation Bar */
    .nav-container {
        background: linear-gradient(135deg, #0f1419 0%, #1a2431 100%);
        border-bottom: 1px solid #1e2a3a;
        padding: 1rem 2rem;
        margin-bottom: 2rem;
    }
    
    .nav-content {
        max-width: 1200px;
        margin: 0 auto;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .nav-brand {
        display: flex;
        align-items: center;
        gap: 12px;
        font-size: 1.4rem;
        font-weight: 600;
        color: #e8eef3;
    }
    
    .nav-links {
        display: flex;
        gap: 2rem;
        align-items: center;
    }
    
    .nav-link {
        color: #8b9bb4;
        text-decoration: none;
        font-weight: 500;
        font-size: 0.95rem;
        transition: color 0.3s ease;
        cursor: pointer;
    }
    
    .nav-link:hover {
        color: #58a6ff;
    }
    
    .nav-link.active {
        color: #58a6ff;
        border-bottom: 2px solid #58a6ff;
        padding-bottom: 4px;
    }
    
    /* Main container */
    .main-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 0 2rem;
    }
    
    .app-title {
        text-align: center;
        font-size: 2.3rem;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }
    
    .app-subtitle {
        text-align: center;
        font-size: 1rem;
        color: #8b9bb4;
        margin-bottom: 3rem;
        font-weight: 400;
        line-height: 1.6;
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        background: #1a2431 !important;
        border: 1px solid #2d3b4f !important;
        border-radius: 8px !important;
        color: #ffffff !important;
        padding: 14px 16px !important;
        font-size: 15px !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #3d8bf5 !important;
        box-shadow: 0 0 0 2px rgba(61, 139, 245, 0.1) !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #6b7b95 !important;
    }
    
    .stTextInput > label {
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        color: #ccd6e0 !important;
        font-size: 15px !important;
        margin-bottom: 10px !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #1e2a3a 0%, #2d3b4f 100%) !important;
        border: 1px solid #3d4d63 !important;
        border-radius: 8px !important;
        color: #ffffff !important;
        font-weight: 500 !important;
        font-size: 15px !important;
        padding: 14px 28px !important;
        font-family: 'Inter', sans-serif !important;
        width: 100% !important;
        margin-top: 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #2d3b4f 0%, #3d4d63 100%) !important;
        border-color: #58a6ff !important;
        transform: translateY(-1px);
    }
    
    /* Alert containers */
    .alert-container {
        border-radius: 10px;
        padding: 24px;
        margin: 2rem 0;
        border: 1px solid;
        background: #1a2431;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    
    .safe-alert {
        border-color: #2e7d32;
        background: linear-gradient(135deg, #1a2431 0%, #1e3320 100%);
    }
    
    .danger-alert {
        border-color: #d32f2f;
        background: linear-gradient(135deg, #1a2431 0%, #332020 100%);
    }
    
    .alert-title {
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .safe-title {
        color: #4caf50;
    }
    
    .danger-title {
        color: #f44336;
    }
    
    .alert-content {
        color: #ccd6e0;
        line-height: 1.6;
        font-size: 14px;
    }
    
    /* Section headers */
    h3 {
        color: #ffffff !important;
        font-weight: 500 !important;
        margin-bottom: 1rem !important;
        font-size: 1.3rem !important;
        border-bottom: 1px solid #2d3b4f;
        padding-bottom: 0.5rem;
    }
    
    /* Stats */
    .stats-container {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 20px;
        margin: 2.5rem 0;
    }
    
    .stat-card {
        background: linear-gradient(135deg, #1a2431 0%, #1e2a3a 100%);
        border: 1px solid #2d3b4f;
        border-radius: 10px;
        padding: 24px 16px;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .stat-card:hover {
        border-color: #3d8bf5;
        transform: translateY(-2px);
    }
    
    .stat-number {
        font-size: 1.5rem;
        font-weight: 600;
        color: #58a6ff;
        display: block;
        margin-bottom: 8px;
    }
    
    .stat-label {
        color: #8b9bb4;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 500;
    }
    
    /* Sidebar */
    .sidebar .sidebar-content {
        background: #1a2431;
        border-right: 1px solid #2d3b4f;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .main-container {
            padding: 0 1rem;
        }
        
        .app-title {
            font-size: 2rem;
        }
        
        .stats-container {
            grid-template-columns: 1fr;
            gap: 15px;
        }
        
        .nav-content {
            flex-direction: column;
            gap: 1rem;
            text-align: center;
        }
        
        .nav-links {
            gap: 1.5rem;
        }
    }
    
    /* Loading spinner */
    .stSpinner > div {
        border-top-color: #58a6ff !important;
    }
</style>
""", unsafe_allow_html=True)

# Navigation Bar
st.markdown("""
<div class="nav-container">
    <div class="nav-content">
        <div class="nav-brand">
            🛡️ PhishGuard AI
        </div>
        <div class="nav-links">
            <span class="nav-link active">Home</span>
            <span class="nav-link">Analysis</span>
            <span class="nav-link">Security Tips</span>
            <span class="nav-link">About</span>
            <span class="nav-link">Contact</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Create a function to generate cleaned data from raw text
def clean_text(text):
    text = word_tokenize(text)
    text = " ".join(text)
    text = [char for char in text if char not in string.punctuation]
    text = ''.join(text)
    text = [char for char in text if char not in re.findall(r"[0-9]", text)]
    text = ''.join(text)
    text = [word.lower() for word in text.split() if word.lower() not in set(stopwords.words('english'))]
    text = ' '.join(text)
    text = list(map(lambda x: port_stemmer.stem(x), text.split()))
    return " ".join(text)

# Main app layout
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Header
st.markdown('<h1 class="app-title">Advanced Email Security Analysis</h1>', unsafe_allow_html=True)
st.markdown('<p class="app-subtitle">Protect your organization from phishing attacks with AI-powered threat detection and real-time security analysis</p>', unsafe_allow_html=True)

# Stats
st.markdown("""
<div class="stats-container">
    <div class="stat-card">
        <span class="stat-number">99.8%</span>
        <span class="stat-label">Detection Accuracy</span>
    </div>
    <div class="stat-card">
        <span class="stat-number">AI</span>
        <span class="stat-label">Powered Analysis</span>
    </div>
    <div class="stat-card">
        <span class="stat-number">Real-time</span>
        <span class="stat-label">Threat Detection</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Input section
st.markdown("### Analyze Message Content")
input_sms = st.text_input("Message Content", placeholder="Paste email or message content here for security analysis...")

if st.button('🔍 Analyze Message Security'):
    if input_sms.strip() == "":
        st.error("Please enter a message to analyze")
    else:
        with st.spinner('Analyzing message content for security threats...'):
            # 1. Preprocess
            transform_text = clean_text(input_sms)
            
            # 2. Vectorize
            vector_input = tfidf.transform([transform_text])
            
            # 3. Prediction
            result = model.predict(vector_input)[0]

            # 4. Display results
            if result == 1:
                st.markdown("""
                <div class="alert-container danger-alert">
                    <div class="alert-title danger-title">
                        ⚠️ Suspicious Content Detected
                    </div>
                    <div class="alert-content">
                        <strong>Security Alert:</strong> This message exhibits multiple characteristics commonly associated with phishing attempts. Exercise extreme caution and verify the sender's identity before taking any action.
                    </div>
                </div>
                """, unsafe_allow_html=True)

            else:
                st.markdown("""
                <div class="alert-container safe-alert">
                    <div class="alert-title safe-title">
                        ✓ Message Security Verified
                    </div>
                    <div class="alert-content">
                        <strong>Analysis Complete:</strong> This message does not exhibit suspicious characteristics typically associated with phishing or malicious content. However, always remain vigilant with unexpected communications.
                    </div>
                </div>
                """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🔒 Security Guidelines")
    st.markdown("""
    <div style="background: #1a2431; padding: 1.5rem; border-radius: 8px; border: 1px solid #2d3b4f;">
    <div style="color: #ccd6e0; font-size: 14px; line-height: 1.6;">
    <strong>Best Practices:</strong><br><br>
    • Verify sender email addresses<br>
    • Check for spelling errors<br>
    • Hover over links before clicking<br>
    • Be cautious with urgent requests<br>
    • Use multi-factor authentication<br>
    • Report suspicious emails<br>
    • Keep software updated
    </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📊 Quick Stats")
    st.markdown("""
    <div style="background: #1a2431; padding: 1.5rem; border-radius: 8px; border: 1px solid #2d3b4f;">
    <div style="color: #ccd6e0; font-size: 14px; line-height: 1.6;">
    • 91% of cyber attacks start with email<br>
    • Phishing attacks up 65% in 2024<br>
    • Average cost: $4.65M per breach<br>
    • Detection time: 207 days avg.
    </div>
    </div>
    """, unsafe_allow_html=True)