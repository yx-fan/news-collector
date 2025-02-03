import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch.nn.functional as F
import os

# Load the pre-trained model and tokenizer, automatically download the model from Hugging Face
# if it's not already downloaded. The model is cached in the `./models` directory.
MODEL_NAME = "ProsusAI/finbert"
CACHE_DIR = "./models"
os.makedirs(CACHE_DIR, exist_ok=True)
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, cache_dir=CACHE_DIR)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, cache_dir=CACHE_DIR)
model.eval() # Set the model to evaluation mode, disable dropout and batch normalization layers for inference

def analyze_sentiment(text):
    """
    Analyze the sentiment of the given text.
    """
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)

    with torch.no_grad():
        outputs = model(**inputs)
        probs = F.softmax(outputs.logits, dim=-1) # Convert logits to probabilities
    
    # Get the predicted sentiment
    positive, negative, neutral = probs[0].tolist() # Convert the tensor to a list
    # print(probs)
    # print(model.config.id2label)
    # print(probs[0].tolist())

    print(f"Negative: {negative}, Neutral: {neutral}, Positive: {positive}")


    # Calculate the sentiment score
    sentiment_score = (positive - negative) * (1 - neutral) # mulitply by 1-neutral to give more weight to positive/negative sentiment
    print(f"Sentiment score: {sentiment_score}")

    return sentiment_score