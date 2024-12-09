# Article Summarizer

## Overview
This Python application allows you to summarize articles from web URLs using the Hugging Face BART large CNN model for text summarization.

## Features
- Extract article text from web URLs
- Summarize articles using state-of-the-art NLP model
- Support for multiple article URLs
- Chunked summarization for longer articles

## Prerequisites
- Python 3.8+
- Required Python libraries:
  - requests
  - beautifulsoup4
  - transformers
  - torch
  - tkinter (for GUI)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/barbercash/ArticleSummarizer.git
cd ArticleSummarizer
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

### Command Line
python main.py

## Configuration
- Adjust `max_chunk_size` in the `summarize_text()` function based on your model and hardware

## Limitations
- Summarization quality depends on article structure and complexity
- Some websites may block web scraping

## Contributing
Contributions are welcome! Please submit pull requests or open issues.

## License
MIT