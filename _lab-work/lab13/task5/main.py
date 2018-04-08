from flask import Flask, render_template, flash, send_from_directory
import os
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.secret_key = "asdhiqwekhukh2397y1238oyt786atp0-vy9awer"

ALLOW_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']


class UploadForm(FlaskForm):
    """ Construct the upload form """
    upload = FileField("image", validators=[FileAllowed(ALLOW_EXTENSIONS,
                                                        'Please upload image files: the extension should be "{}".'
                                                        .format(ALLOW_EXTENSIONS)), FileRequired()])


# list uploaded files and upload form
@app.route('/', methods=['GET', 'POST'])
def main():
    error = None
    form =UploadForm()
    if form.validate_on_submit():
        # get a secure file name, such as removing the space and adding underscore
        file = form.upload.data
        filename = secure_filename(file.filename)
        # save the file to the upload folder
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('Image "{}" is uploaded.'.format(file.filename))

    # retrieve the files and validate the file extension at the same time
    files = [os.path.join(app.config['UPLOAD_FOLDER'], f) for f in os.listdir(app.config['UPLOAD_FOLDER']) if
             validate_filename(f)]

    return render_template('main.html', form=form, files=files, error=error)


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
