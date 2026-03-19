import re  # Regular expressions for text cleaning

def clean_text(text: str) -> str:
    # Replace multiple spaces/newlines with a single space
    text = re.sub(r'\s+', ' ', text)

    # Remove leading and trailing whitespace
    return text.strip()