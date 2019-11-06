from flask import Flask
from flask_sslify import SSLify
from flask import request
import requests
import numpy as np
from keras.models import load_model
from keras.preprocessing import image
from PIL import Image
from io import BytesIO


app = Flask(__name__)
ssl = SSLify(app)
model = load_model('model_VGG16.h5')


def get_photo(photo_id, token):
    size = (224, 224)
    url = 'https://api.telegram.org/bot' + token + '/' + 'getFile?file_id=' + str(photo_id)
    r = requests.get(url).json()
    path_to_photo = r['result']['file_path']
    file_url = 'https://api.telegram.org/file/bot' + token + '/' + str(path_to_photo)
    response = requests.get(file_url)
    img = Image.open(BytesIO(response.content))
    img = img.resize(size)
    return img


def send_message(token, chat_id, text='text'):
    url = 'https://api.telegram.org/bot' + token + '/' + 'sendMessage' + '?chat_id=' + str(chat_id) + '&text=' + text
    return requests.get(url)


def image_classifier(token, photo_id):
    img = get_photo(photo_id, token)
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    classes = model.predict(x)
    if classes[0] > 0.5:
        return 'It is a dog'
    else:
        return 'It is a cat'


@app.route('/')
def test():
    return '<h1>Ok</h1>'


@app.route('/<token>', methods=['GET', 'POST'])
def index(token):
    token = str(token)
    if request.method == 'POST':
        r = request.get_json()
        chat_id = r['message']['chat']['id']
        try:
            message = r['message']['text']
        except Exception:
            message = False
        try:
            photo_id = r['message']['photo'][-1]['file_id']
        except Exception:
            photo_id = False
        if message:
            send_message(token,
                         chat_id,
                         text='Hi, I can classify cats and dogs, send me a photo, please (not a document)')
        elif photo_id:
            answer = image_classifier(token, photo_id)
            send_message(token, chat_id, text=str(answer))
        else:
            send_message(token,
                         chat_id,
                         text='Hi. I can classify cats and dogs, send me a photo, please (not a document)')
    return '<h1>test server</h1>'


if __name__ == '__main__':
    app.run()
