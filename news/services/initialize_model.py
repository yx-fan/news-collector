import os
from transformers import AutoTokenizer, AutoModelForSequenceClassification

MODEL_NAME = "ProsusAI/finbert"
CACHE_DIR = "./models" 

def initialize_model():
    """
    Initialize the FinBERT model and tokenizer.
    """
    os.makedirs(CACHE_DIR, exist_ok=True)

    # Load the pre-trained model and tokenizer, automatically download the model from Hugging Face
    try:
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, cache_dir=CACHE_DIR)
        model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, cache_dir=CACHE_DIR)
        print(f"✅ FinBERT model initialized successfully!")
    except Exception as e:
        print("❌ Error initializing FinBERT model")
        print(e)

if __name__ == "__main__":
    initialize_model()
