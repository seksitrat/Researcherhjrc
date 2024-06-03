from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Folder to store uploaded PDF files
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def load_papers():
    if 'papers' not in session:
        session['papers'] = []
    return session['papers']

def save_papers(papers):
    session['papers'] = papers

@app.route('/')
def index():
    papers = load_papers()
    return render_template('index.html', papers=papers)

@app.route('/add_paper', methods=['POST'])
def add_paper():
    papers = load_papers()
    topic = request.form['topic']
    abstract = request.form['abstract']
    conclusion = request.form['conclusion']
    link = request.form['link']

    # Handle file upload
    pdf_file = request.files['pdf']
    if pdf_file:
        # Save file to upload folder
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_file.filename)
        pdf_file.save(pdf_path)
        print("PDF saved at:", pdf_path)  # Add this line to check file path
    else:
        print("No PDF file uploaded")  # Add this line to check if a file was uploaded

    # Add paper to list
    paper = {'topic': topic, 'abstract': abstract, 'conclusion': conclusion, 'link': link, 'pdf_path': pdf_path}
    papers.append(paper)
    save_papers(papers)
    
    return redirect(url_for('index'))

@app.route('/download_pdf/<path:filename>')
def download_pdf(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/delete_paper/<int:index>', methods=['POST'])
def delete_paper(index):
    papers = load_papers()
    if 0 <= index < len(papers):
        del papers[index]
        save_papers(papers)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
