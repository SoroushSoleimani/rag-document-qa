import docx

def extract_text_from_docx(file_path):
    try:
        doc = docx.Document(file_path)
        full_text = []
        for para in doc.paragraphs:
            if para.text.strip():
                full_text.append(para.text.strip())
        return '\n'.join(full_text)
    except Exception as e:
        print(f"Error reading docx file: {e}")
        return ""