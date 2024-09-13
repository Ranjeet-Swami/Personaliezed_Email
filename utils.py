import re

def clean_text(text):
    """
    Cleans the input text by removing unnecessary whitespace and special characters.
    
    Parameters:
    - text (str): The raw text input to be cleaned.
    
    Returns:
    - str: The cleaned text.
    """
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    # Remove special characters (optional, depending on your needs)
    text = re.sub(r'[^\w\s]', '', text)
    
    # Optional: convert text to lowercase if needed
    # text = text.lower()
    
    return text

# You can add more utility functions here if needed.
