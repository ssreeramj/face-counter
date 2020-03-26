import os

from flask import Flask, render_template, url_for, redirect, request, flash
from flask_uploads import configure_uploads, UploadSet, IMAGES

from main import get_faces

app = Flask(__name__, static_url_path = "", static_folder = "static/img")

app.secret_key = 'thisisasecretekey'    

photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
configure_uploads(app, photos)

@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        no_of_faces = get_faces(filename)
        res_img = os.path.join(os.getcwd(), f'/res_{filename}')
        return render_template('result.html', no_of_faces=no_of_faces, img_name=res_img)
    return render_template('index.html')

# @app.route('/photo/<id>')
# def show(id):
#     photo = Photo.load(id)
#     if photo is None:
#         abort(404)
#     url = photos.url(photo.filename)
#     return render_template('show.html', url=url, photo=photo)

if __name__ == '__main__':
    app.run(debug=True)

