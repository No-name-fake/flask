from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
import os
import whisper
from datetime import datetime
from werkzeug.utils import secure_filename

whisper_bp = Blueprint("whisper", __name__, template_folder="templates")

# Whisperモデルの読み込み
model = whisper.load_model("base")

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@whisper_bp.route("/whisper", methods=["GET", "POST"])
@login_required
def upload_audio():
    if request.method == "POST":
        file = request.files["file"]
        if file and file.filename:
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            result = model.transcribe(filepath)
            return render_template("whisper/result.html", text=result["text"], filename=filename)


    return render_template("whisper/upload.html")

from flask import send_from_directory

@whisper_bp.route("/uploads/<filename>")
@login_required
def uploaded_file(filename):
    upload_dir = os.path.join(os.path.dirname(__file__), "uploads")
    return send_from_directory(upload_dir, filename)