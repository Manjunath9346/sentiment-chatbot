# Sentiment-Aware Chatbot

A sentiment-aware chatbot built using Streamlit and Hugging Face Transformers.

## Features
- User Login & Registration
- Multiple Chat History
- Sentiment Analysis using CardiffNLP RoBERTa
- AI Responses using Qwen2.5-1.5B-Instruct
- Runs completely locally (No API required)

## Requirements
- Python 3.10+
- Streamlit
- Transformers
- Torch

## Run

pip install -r requirements.txt
streamlit run app.py

## Tech Stack

- Python
- Streamlit
- Hugging Face Transformers
- PyTorch
- Qwen2.5-1.5B-Instruct
- CardiffNLP RoBERTa (Sentiment Analysis)



## Problem Statement
Develop an AI chatbot capable of understanding user sentiment and generating appropriate responses.

## Dataset
- Sentiment Analysis Model:
  CardiffNLP Twitter RoBERTa pretrained model.
- Response Generation:
  Qwen2.5-1.5B-Instruct (local Hugging Face model).

## Methodology
1. User authentication
2. User enters a message
3. Sentiment prediction
4. Response generation
5. Save conversation history

## Results
- Detects Positive, Negative and Neutral sentiment.
- Generates contextual AI responses.
- Maintains multiple chat histories.
- Runs completely offline.


## Screenshots

### Login Page

![Login Page](screenshots/login.png)

### Chat Interface

![Chat Interface](screenshots/chat.png)

### Dashboard

![Dashboard](screenshots/dashboard.png)
