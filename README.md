# PDF Link Downloader

A Python script that extracts PDF links from a PDF file and downloads all referenced PDFs.

## Features

- Extracts all PDF links from a source PDF file
- Downloads PDFs to a specified folder
- Skips already downloaded files
- Shows download progress
- Handles errors gracefully

## Requirements

- Python 3.x
- PyPDF2
- requests

## Installation

1. Clone this repository
2. Install required packages:

pip install PyPDF2 requests

## Usage

1. Run the script:
   python pdf_downloader.py

2. When prompted, enter the path to your source PDF file
3. The script will create a `downloaded_pdfs` folder and save all downloaded PDFs there

## Notes

- The script only downloads links that end with `.pdf`
- Downloaded files are saved in the `downloaded_pdfs` folder with their original filenames
- If a file already exists, it will be skipped
