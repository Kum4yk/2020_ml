import os
from flask import Flask, request
from werkzeug.utils import secure_filename
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np


upload_folder = os.path.abspath(os.getcwd()) + os.path.sep + 'uploads'
allowed_extension = {"mp3", }
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = upload_folder


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extension


# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'],
#                                filename)


def get_freq_from_music(file):
    y, _ = librosa.load(file)
    y_db_max = librosa.amplitude_to_db(
        librosa.stft(y),
        ref=np.max
    )
    return y_db_max


def save_music_ft_picture(y, file_name):
    figure = plt.figure()

    librosa.display.specshow(
        y,
        y_axis='log',
        x_axis='time'
    )

    plt.title(f'Power spectrogram of {file_name}')
    plt.colorbar(format='%+2.0f dB')
    plt.tight_layout()
    result_path = upload_folder + os.path.sep + file_name
    figure.savefig(result_path)


def set_picture_format(filename: str, frmt: str):
    return filename.rsplit(".")[0] + "." + frmt


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            # because librosa.load(FileStorage) - error
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            y = get_freq_from_music(filepath)

            picture_name = set_picture_format(filename, "png")
            save_music_ft_picture(y, picture_name)
            return f'''
<!doctype html>
<head>
<meta charset="utf-8">
    <title>Picture</title>
</head>
<body>
    <img src="uploads/{picture_name}" />
</body>
</html>
 '''

        return "<h1>Try again, *.mp3 file pls</h1>"
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new *.mp3 File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''


if __name__ == "__main__":
    app.run(debug=True)
