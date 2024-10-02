import os
import re
import PyPDF2
from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Define the path to the Books folder inside the Documents directory
books_path = os.path.expanduser('~/Documents/Coding/Github/BookSummarizer/SummarizeBook')

# Create the Books folder if it doesn't exist
if not os.path.exists(books_path):
    os.makedirs(books_path)
    print(f"Created folder: {books_path}")
else:
    print(f"Folder already exists: {books_path}")

# Function to extract text from a PDF
def extract_text_from_pdf(pdf_file):
    try:
        with open(pdf_file, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ''
            for page in reader.pages:
                text += page.extract_text() or ''  # Ensure non-None values
        return text
    except Exception as e:
        print(f"Error extracting text from {pdf_file}: {e}")
        return ""

# Function to split text into chapters
def split_into_chapters(text):
    chapters = re.split(r'Chapter \d+', text, flags=re.IGNORECASE)
    return chapters[1:]  # The first split element might be before Chapter 1

# Function to summarize text using Hugging Face with chunking
def summarize_text(text):
    max_chunk_size = 1024  # Adjust based on the model's input size
    text_chunks = [text[i:i + max_chunk_size] for i in range(0, len(text), max_chunk_size)]

    summaries = []
    for chunk in text_chunks:
        input_length = len(chunk)
        max_length = min(150, max(9, input_length // 2))
        min_length = max(5, max_length // 2)

        try:
            # Remove use_auth_token from here
            summary = summarizer(chunk, max_length=max_length, min_length=min_length, do_sample=False)
            summaries.append(summary[0]['summary_text'])
        except Exception as e:
            print(f"Error summarizing chunk: {e}")

    return " ".join(summaries)

# Function to summarize all chapters from a PDF
def summarize_pdf_chapters(pdf_file):
    text = extract_text_from_pdf(pdf_file)
    if not text:
        return {}

    chapters = split_into_chapters(text)
    summaries = {}

    for i, chapter in enumerate(chapters):
        summary = summarize_text(chapter)
        print(summary)
        summaries[f'Chapter {i + 1}'] = summary
        print(f"Summarized Chapter {i + 1}")

    return summaries

# Example usage: Summarize all PDFs in the Books folder
if __name__ == "__main__":
    pdf_files = [file for file in os.listdir(books_path) if file.endswith('.pdf')]

    if not pdf_files:
        print("No PDF files found in the Books folder.")
    else:
        for pdf_file in pdf_files:
            pdf_file_path = os.path.join(books_path, pdf_file)
            print(f"Summarizing {pdf_file}...")
            summaries = summarize_pdf_chapters(pdf_file_path)

            for chapter, summary in summaries.items():
                print(f"{chapter} Summary:\n{summary}\n")
