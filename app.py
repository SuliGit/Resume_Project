from flask import Flask, render_template, request
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Make sure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'resume' not in request.files:
        return 'No file part'

    file = request.files['resume']
    if file.filename == '':
        return 'No selected file'

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # Extract text from the resume
    if file.filename.endswith('.pdf'):
        from pdfplumber import open as pdf_open
        with pdf_open(file_path) as pdf:
            text = ''.join(page.extract_text() for page in pdf.pages)
    elif file.filename.endswith('.docx'):
        import docx
        doc = docx.Document(file_path)
        text = '\n'.join([para.text for para in doc.paragraphs])
    else:
        return 'Unsupported file format'

    return f"<h3>Extracted Resume Text:</h3><pre>{text}</pre>"

if __name__ == '__main__':
    app.run(debug=True)
