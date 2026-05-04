from fastapi import UploadFile
from pypdf import PdfReader


class PDFReader:

    def read(self, file: UploadFile) -> str:
        reader = PdfReader(file.file)

        text_parts = []

        for page in reader.pages:
            text = page.extract_text()
            if text:
                text_parts.append(text)

        return "\n".join(text_parts)