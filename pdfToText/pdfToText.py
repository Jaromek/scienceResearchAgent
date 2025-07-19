from pdfminer.high_level import extract_text
from typing import List
import re

class PDFToText:
    def __init__(self, pdf_path: str):
        """
        Initialize the PDFToText class with the path to the PDF file or directory.

        Args:
            pdf_path (str): The path to the PDF file or directory.
        """
        self.pdf_path = pdf_path

    def _path_to_pdfs(self) -> List[str]:
        """
        Get the paths to PDF files.

        Returns:
            List[str]: Paths to the PDF files.
        """
        pdfs = []
        
        # If it's a single file
        if os.path.isfile(self.pdf_path) and self.pdf_path.endswith('.pdf'):
            pdfs.append(self.pdf_path)
        
        # If it's a directory
        elif os.path.isdir(self.pdf_path):
            for file in os.listdir(self.pdf_path):  # TUTAJ BYŁA BŁĄD!
                if file.endswith('.pdf'):
                    full_path = os.path.join(self.pdf_path, file)
                    pdfs.append(full_path)
        
        return pdfs
    
    def _extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extract text from a PDF file starting from the Abstract section.

        Args:
            pdf_path (str): The path to the PDF file.

        Returns:
            str: The extracted text from the PDF file starting from Abstract.
        """
        try:
            full_text = extract_text(pdf_path)
            
            # Find the start of Abstract section (case insensitive)
            abstract_match = re.search(r'\babstract\b', full_text, re.IGNORECASE)
            
            if abstract_match:
                # Return text starting from "Abstract"
                return full_text[abstract_match.start():]
            else:
                # If no Abstract found, look for common alternatives
                alternatives = [r'\bsummary\b', r'\boverview\b', r'\bintroduction\b']
                
                for pattern in alternatives:
                    match = re.search(pattern, full_text, re.IGNORECASE)
                    if match:
                        print(f"Abstract not found, starting from: {match.group()}")
                        return full_text[match.start():]
                
                # If no section found, return full text but warn user
                print(f"Warning: No Abstract or alternative section found in {pdf_path}")
                return full_text
                
        except Exception as e:
            print(f"Error extracting text from {pdf_path}: {e}")
            return ""

    def convert_to_text(self) -> List[str]:
        """
        Convert the PDF file(s) to text.

        Returns:
            List[str]: List of extracted texts from the PDF files.
        """
        paths = self._path_to_pdfs()
        if not paths:
            raise ValueError("No PDF files found in the provided path.")
        
        texts = []
        for path in paths:
            print(f"Processing: {path}")
            text = self._extract_text_from_pdf(path)
            if text:  # Only add non-empty texts
                texts.append(text)

        return texts

if __name__ == "__main__":
    import os
    import sys

    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    os.chdir(parent_dir)
    sys.path.append(parent_dir)

    pdf_path = 'archive'  # Replace with your PDF file path
    pdf_to_text = PDFToText(pdf_path)
    
    try:
        extracted_texts = pdf_to_text.convert_to_text()
        
        for i, text in enumerate(extracted_texts, 1):
            print(f"=== PDF {i} ===")
            print(text[:1000])  # Print first 1000 characters
            print("=" * 80)
            print()
    except Exception as e:
        print(f"Error: {e}")