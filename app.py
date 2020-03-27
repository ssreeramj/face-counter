import os

from flask import Flask, render_template, request
from werkzeug import secure_filename

from main import get_faces

app = Flask(__name__, static_url_path="", static_folder="static/img")

app.secret_key = 'thisisasecretekey'    
app.config['UPLOAD_FOLDER'] = 'static/img'

@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        f = request.files['photo']
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
        no_of_faces = get_faces(f.filename)
        res_img = os.path.join(os.getcwd(), f'/res_{f.filename}')
        return render_template('result.html', no_of_faces=no_of_faces, img_name=res_img)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)

