import pdf2image
import os, sys
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract

# Initialize the path of your documents
PATH = 'Enter your path'

# Initialize the counter for document processing
i = 1

def delete_ppms():
    """Delete temporary ppm and unwanted files."""
    for file in os.listdir(PATH):
        if '.ppm' in file or '.DS_Store' in file:
            try:
                os.remove(os.path.join(PATH, file))
            except FileNotFoundError:
                pass

# Sort files into lists based on their extensions
pdf_files = []
docx_files = []

for f in os.listdir(PATH):
    full_name = os.path.join(PATH, f)
    if os.path.isfile(full_name):
        filename, ext = os.path.splitext(f)
        if ext == '.pdf':
            pdf_files.append(f)
        elif ext == '.docx':
            docx_files.append(f)

def pdf_extract(file, i):
    """Extract text from PDF using OCR."""
    print("Extracting from file:", file)
    delete_ppms()
    images = pdf2image.convert_from_path(os.path.join(PATH, file), output_folder=PATH)
    
    # Rename and process images
    j = 0
    for file in sorted(os.listdir(PATH)):
        if '.ppm' in file and 'image' not in file:
            os.rename(os.path.join(PATH, file), os.path.join(PATH, f'image{i}-{j}.ppm'))
            j += 1
    
    j = 0
    output_file = os.path.join(PATH, f'result{i}.txt')
    with open(output_file, 'w') as f:
        files = [f for f in os.listdir(PATH) if '.ppm' in f]
        
        for file in sorted(files, key=lambda x: int(x[x.index('-') + 1: x.index('.')])):
            temp = pytesseract.image_to_string(Image.open(os.path.join(PATH, file)))
            f.write(temp)

# Execute extraction for all PDF files
for i, pdf_file in enumerate(pdf_files):
    pdf_extract(pdf_file, i)
