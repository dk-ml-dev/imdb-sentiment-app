# main.py

import streamlit as st
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.datasets import imdb
from tensorflow.keras.preprocessing import sequence
from deep_translator import GoogleTranslator
from utils.db import create_table, insert_review, fetch_reviews

# Load word index from Keras
word_index = imdb.get_word_index()
reverse_word_index = {value: key for (key, value) in word_index.items()}

# Load model
model = load_model("model/simple_rnn_imdb.h5")

# Setup DB
create_table()


# Utility: decode encoded review
def decode_review(encoded):
    return " ".join([reverse_word_index.get(i, "?") for i in encoded])


# Preprocess review for model
def preprocess_text(text):
    words = text.lower().split()
    encoded_review = [word_index.get(word, 2) + 3 for word in words]
    padded_review = sequence.pad_sequences([encoded_review], maxlen=500)
    return padded_review


# Predict sentiment
def predict_sentiment(review_text):
    padded = preprocess_text(review_text)
    prediction = model.predict(padded, verbose=0)[0][0]
    sentiment = "Positive 😊" if prediction >= 0.6 else "Negative 😞" if prediction <= 0.4 else "Neutral 😐"
    return sentiment, prediction


# UI
st.set_page_config(page_title="🎬 IMDB Sentiment Analyzer", layout="wide")
st.title("🎬 IMDB Movie Review Sentiment Analysis")
st.write("Enter a movie review to classify its sentiment.")

# Try example
if st.button("🔁 Try Example Review"):
    st.session_state.example_text = "I had high expectations going in. The trailer was compelling, and the cast list impressive. The first act delivered—solid pacing and acting. Then came act two, which dragged. By the finale, I was just tired. All in all, a mixed bag."

user_input = st.text_area("✍️ Enter a movie review", value=st.session_state.get("example_text", ""), height=150)

if st.button("🎯 Classify"):
    if not user_input.strip():
        st.warning("Please enter a review.")
    else:
        # Translate (if needed)
        translated = GoogleTranslator(source='auto', target='en').translate(user_input)

        # Predict
        sentiment, score = predict_sentiment(translated)

        # Save to DB
        insert_review(user_input, translated, sentiment, float(score))

        # Display
        st.success(f"**Sentiment**: {sentiment}")
        st.info(f"**Prediction Score**: {score:.4f}")
        st.caption(f"Translated Review: {translated}")

# View history
if st.checkbox("📜 Show Recent Reviews"):
    results = fetch_reviews(limit=5)
    for row in results:
        st.markdown(f"""
        **🕒 {row[4]}**  
        - Sentiment: `{row[2]}` ({row[3]:.2f})  
        - Original: {row[0]}  
        - Translated: {row[1]}
        ---
        """)