import os
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np


allowed_extension = {"mp3", }
upload_folder = "uploads"
image_folfer = os.path.join("static", "images")
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = upload_folder


def allowed_file(filename: str):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extension


def set_picture_format(filename: str, frmt: str):
    return filename.rsplit(".")[0] + "." + frmt


def get_freq_from_music(filepath: str):
    y, _ = librosa.load(filepath)
    y_db_max = librosa.amplitude_to_db(
        librosa.stft(y),
        ref=np.max
    )
    return y_db_max


def handle_picture(y: np.ndarray, file_name: str, frmt: str):
    figure = plt.figure()

    librosa.display.specshow(
        y,
        y_axis='log',
        x_axis='time'
    )

    plt.title(f'Power spectrogram of {file_name}')
    plt.colorbar(format='%+2.0f dB')
    plt.tight_layout()

    file_name = set_picture_format(file_name, frmt)
    result_path = os.path.join(image_folfer, file_name)
    figure.savefig(result_path)

    return result_path


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        try:
            file = request.files['file']
        # Bad practice
        except:
            return "<h1>Try again, *.mp3 file pls</h1>"

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(upload_folder, filename)

            file.save(filepath)
            y = get_freq_from_music(filepath)
            picture_path = handle_picture(y, filename, "svg")

            return render_template("image.html", user_image=picture_path)

    return render_template("main.html")


if __name__ == "__main__":
    app.run(debug=True, port=8080)
