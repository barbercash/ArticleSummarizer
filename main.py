import os
import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog
import requests
from bs4 import BeautifulSoup
from transformers import pipeline
import threading

class ArticleSummarizerApp:
    def __init__(self, master):
        self.master = master
        master.title("Article Summarizer")
        master.geometry("800x600")

        # URL Input
        self.url_label = tk.Label(master, text="Enter Article URL:")
        self.url_label.pack(pady=(10, 0))

        self.url_entry = tk.Entry(master, width=70)
        self.url_entry.pack(pady=5)

        # Add URL Button
        self.add_url_button = tk.Button(master, text="Add URL", command=self.add_url)
        self.add_url_button.pack(pady=5)

        # URL Listbox
        self.url_listbox = tk.Listbox(master, width=70, height=5)
        self.url_listbox.pack(pady=5)

        # Remove URL Button
        self.remove_url_button = tk.Button(master, text="Remove Selected URL", command=self.remove_url)
        self.remove_url_button.pack(pady=5)

        # Summarize Button
        self.summarize_button = tk.Button(master, text="Summarize Articles", command=self.start_summarization)
        self.summarize_button.pack(pady=10)

        # Results Text Area
        self.results_text = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=70, height=15)
        self.results_text.pack(pady=10)

        # Initialize summarizer
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    def add_url(self):
        url = self.url_entry.get().strip()
        if url:
            self.url_listbox.insert(tk.END, url)
            self.url_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Invalid URL", "Please enter a valid URL")

    def remove_url(self):
        selected_indices = self.url_listbox.curselection()
        if selected_indices:
            for index in reversed(selected_indices):
                self.url_listbox.delete(index)

    def extract_article_from_url(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            paragraphs = soup.find_all('p')
            article_text = "\n".join([para.get_text() for para in paragraphs])
            return article_text
        except Exception as e:
            self.update_results(f"Error extracting article from {url}: {e}\n")
            return ""

    def summarize_text(self, text):
        max_chunk_size = 1024
        text_chunks = [text[i:i + max_chunk_size] for i in range(0, len(text), max_chunk_size)]

        summaries = []
        for chunk in text_chunks:
            input_length = len(chunk)
            max_length = min(150, max(9, input_length // 2))
            min_length = max(5, max_length // 2)

            try:
                summary = self.summarizer(chunk, max_length=max_length, min_length=min_length, do_sample=False)
                summaries.append(summary[0]['summary_text'])
            except Exception as e:
                self.update_results(f"Error summarizing chunk: {e}\n")

        return " ".join(summaries)

    def update_results(self, text):
        self.results_text.insert(tk.END, text)
        self.results_text.see(tk.END)

    def summarize_articles(self):
        urls = list(self.url_listbox.get(0, tk.END))
        self.results_text.delete(1.0, tk.END)

        for url in urls:
            self.update_results(f"Processing article from {url}...\n")
            article_text = self.extract_article_from_url(url)
            if article_text:
                summary = self.summarize_text(article_text)
                self.update_results(f"Summary:\n{summary}\n\n")
            else:
                self.update_results(f"Failed to extract or summarize article from {url}\n\n")

    def start_summarization(self):
        if not self.url_listbox.get(0, tk.END):
            messagebox.showwarning("No URLs", "Please add some URLs to summarize")
            return

        # Run summarization in a separate thread to keep GUI responsive
        thread = threading.Thread(target=self.summarize_articles)
        thread.start()

def main():
    root = tk.Tk()
    app = ArticleSummarizerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()