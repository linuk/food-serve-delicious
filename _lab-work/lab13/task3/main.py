from flask import Flask, render_template, request, flash, redirect, send_from_directory
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.secret_key = "asdhiqwekhukh2397y1238oyt786atp0-vy9awer"

ALLOW_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']


# list uploaded files and upload form
@app.route('/', methods=['GET', 'POST'])
def main():
    error = ''

    if request.method == 'POST':

        # if there is no image file
        if 'image' not in request.files:
            error = 'The file is not attached'
            return redirect(request.url)

        # if the file extension is not correct
        file = request.files['image']
        if not validate_filename(file.filename):
            error = 'The file is not attached'
            return redirect(request.url)

        # if the file validated and okay to upload

        # get a secure file name, such as removing the space and adding underscore
        filename = secure_filename(file.filename)

        # save the file to the upload foloer
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print('Image "{}" is uploaded.'.format(file.filename))
        print(file.filename)
        flash('Image "{}" is uploaded.'.format(file.filename))

    # retrieve the files and validate the file extension at the same time
    files = [os.path.join(app.config['UPLOAD_FOLDER'], f) for f in os.listdir(app.config['UPLOAD_FOLDER']) if validate_filename(f)]
    return render_template('main.html', files=files, error=error)


# download file
@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# Private methods

def validate_filename(filename):
    validateDot = '.' in filename
    validateExt = filename.split('.')[1].lower() in ALLOW_EXTENSIONS

    return validateDot and validateExt


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)
