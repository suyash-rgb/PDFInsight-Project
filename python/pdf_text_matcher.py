import fitz  # PyMuPDF
import nltk
import pandas as pd
from nltk.tokenize import word_tokenize
from collections import Counter

# Download NLTK resources if not already present
nltk.download('punkt')

def read_pdf(file_path):
    # Extract text from PDF
    doc = fitz.open(file_path)
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text()
    return text

def tokenize_text(text):
    # Tokenize the extracted text
    tokens = word_tokenize(text)
    return tokens

def match_values(tokens, reference_list):
    # Compare tokens with reference list
    token_counter = Counter(tokens)
    reference_counter = Counter(reference_list)
    matches = sum((token_counter & reference_counter).values())
    return matches

def calculate_match_percentage(matches, reference_list_length):
    # Calculate match percentage
    match_percentage = (matches / reference_list_length) * 100
    return match_percentage

def output_result(match_percentage, output_format='console'):
    # Display result
    if output_format == 'console':
        print(f"Match Percentage: {match_percentage:.2f}%")
    elif output_format == 'csv':
        pd.DataFrame({'Match Percentage': [match_percentage]}).to_csv('match_percentage.csv', index=False)

def main(file_path, reference_list, output_format='console'):
    text = read_pdf(file_path)
    tokens = tokenize_text(text)
    matches = match_values(tokens, reference_list)
    match_percentage = calculate_match_percentage(matches, len(reference_list))
    output_result(match_percentage, output_format)

# Example usage
reference_list = ['SOAP', 'Swagger', 'Java']
main('BrianMason_Using_Rest_API-2.pdf', reference_list, 'console')
