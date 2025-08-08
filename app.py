from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from test_backend import ask_bot, build_query_engine
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'data'
ALLOWED_EXTENSIONS = {'txt', 'pdf'}

# Ensure data directory exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def index():
    answer = ""
    message = ""

    if request.method == "POST":
        # Handle File Upload
        if "file" in request.files and request.files["file"].filename != "":
            file = request.files["file"]
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                build_query_engine()
                message = f"✅ '{filename}' uploaded and processed successfully! You can now ask questions."
            else:
                message = "❌ Invalid file type. Only .txt and .pdf are allowed."

        # Handle Question
        elif "question" in request.form:
            question = request.form["question"]
            if question.strip():
                answer = ask_bot(question)
            else:
                answer = "Please enter a valid question."

    return render_template("index.html", answer=answer, message=message)

if __name__ == "__main__":
    app.run(debug=True)
