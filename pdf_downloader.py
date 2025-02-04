import PyPDF2
import requests
import re
import os
from urllib.parse import unquote

def extract_links_from_pdf(pdf_path):
    """Extract all links from a PDF file"""
    links = []
    
    # Open the PDF file
    with open(pdf_path, 'rb') as file:
        # Create PDF reader object
        pdf_reader = PyPDF2.PdfReader(file)
        
        # Iterate through all pages
        for page in pdf_reader.pages:
            # Get annotations (which include links)
            if '/Annots' in page:
                annotations = page['/Annots']
                for annotation in annotations:
                    annotation_object = annotation.get_object()
                    if annotation_object.get('/Subtype') == '/Link':
                        if '/A' in annotation_object:
                            uri = annotation_object['/A'].get('/URI')
                            if uri and uri.lower().endswith('.pdf'):
                                links.append(uri)
    
    return links

def download_pdf(url, output_folder):
    """Download a PDF file from a URL"""
    try:
        # Get filename from URL
        filename = unquote(url.split('/')[-1])
        output_path = os.path.join(output_folder, filename)
        
        # Skip if file already exists
        if os.path.exists(output_path):
            print(f"File already exists: {filename}")
            return
        
        # Download the file
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise exception for bad status codes
        
        # Save the file
        with open(output_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        
        print(f"Successfully downloaded: {filename}")
        
    except Exception as e:
        print(f"Error downloading {url}: {str(e)}")

def main():
    # Input PDF file path
    pdf_path = input("Enter the path to your PDF file: ").strip()
    
    # Remove any quotes and & from the path
    pdf_path = pdf_path.strip('"\'').replace('& ', '')
    
    # Verify file exists
    if not os.path.exists(pdf_path):
        print(f"Error: File not found at {pdf_path}")
        return
        
    # Create output folder
    output_folder = "downloaded_pdfs"
    os.makedirs(output_folder, exist_ok=True)
    print(f"Files will be downloaded to: {os.path.abspath(output_folder)}")
    
    # Extract links
    print("Extracting links from PDF...")
    pdf_links = extract_links_from_pdf(pdf_path)
    
    if not pdf_links:
        print("No PDF links found in the document.")
        return
    
    print(f"Found {len(pdf_links)} PDF links")
    
    # Download each PDF
    for i, link in enumerate(pdf_links, 1):
        print(f"\nDownloading PDF {i} of {len(pdf_links)}")
        download_pdf(link, output_folder)

if __name__ == "__main__":
    main()