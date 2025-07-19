from pdfminer.high_level import extract_text
from typing import List
import re
import os

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
            for file in os.listdir(self.pdf_path):
                if file.endswith('.pdf'):
                    full_path = os.path.join(self.pdf_path, file)
                    pdfs.append(full_path)
        
        return pdfs
    
    def _find_bibliography_start(self, text: str) -> int:
        """
        Find the starting position of bibliography/references section.
        
        Args:
            text (str): The full text from PDF
            
        Returns:
            int: Starting position of bibliography, or len(text) if not found
        """
        # Common patterns for bibliography/references section
        patterns = [
            r'\bReferences\b',
            r'\bREFERENCES\b',
            r'\bBibliography\b',
            r'\bBIBLIOGRAPHY\b',
            r'\bLiterature\s+Cited\b',
            r'\bWorks\s+Cited\b',
            r'\bCitations\b',
            r'^\s*References\s*$',  # References on its own line
            r'^\s*REFERENCES\s*$',  # REFERENCES on its own line
            r'^\s*Bibliography\s*$'  # Bibliography on its own line
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.MULTILINE | re.IGNORECASE)
            if match:
                return match.start()
        
        return len(text)  # Return full text length if no bibliography found
    
    def _extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extract text from a PDF file starting from Abstract and ending before Bibliography.

        Args:
            pdf_path (str): The path to the PDF file.

        Returns:
            str: The extracted text from Abstract to before Bibliography.
        """
        try:
            full_text = extract_text(pdf_path)
            
            # Find the start of Abstract section (case insensitive)
            abstract_match = re.search(r'\babstract\b', full_text, re.IGNORECASE)
            
            start_pos = 0
            if abstract_match:
                start_pos = abstract_match.start()
                print(f"Found Abstract section")
            else:
                # If no Abstract found, look for common alternatives
                alternatives = [r'\boverview\b', r'\bintroduction\b']
                
                for pattern in alternatives:
                    match = re.search(pattern, full_text, re.IGNORECASE)
                    if match:
                        print(f"Abstract not found, starting from: {match.group()}")
                        start_pos = match.start()
                        break
                
                if start_pos == 0:
                    print(f"Warning: No Abstract or alternative section found in {pdf_path}")
            
            # Find the end position (before bibliography)
            end_pos = self._find_bibliography_start(full_text)
            
            if end_pos < len(full_text):
                print(f"Found bibliography section, text truncated")
            else:
                print(f"No bibliography found, using full text from start position")
            
            # Extract text between start and end positions
            extracted_text = full_text[start_pos:end_pos].strip()
            
            return extracted_text
            
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
                print(f"Extracted {len(text)} characters")
            else:
                print(f"No text extracted from {path}")

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
            print(f"\n=== PDF {i} ===")
            print(f"Text length: {len(text)} characters")
            print("First 500 characters:")
            print(text[:500])
            print("\nLast 500 characters:")
            print(text[-500:])
            print("=" * 80)
            print()
    except Exception as e:
        print(f"Error: {e}")