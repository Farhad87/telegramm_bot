from flask import Flask
from flask import request
import requests

app = Flask(__name__)


def get_photo(photo_id, token):
    url = 'https://api.telegram.org/bot' + token + '/' + 'getFile?file_id=' + str(photo_id)
    r = requests.get(url).json()
    path_to_photo = r['result']['file_path']
    file_url = 'https://api.telegram.org/file/bot' + token + '/' + str(path_to_photo)
    return requests.get(file_url)


def send_message(token, chat_id, text='text'):
    url = 'https://api.telegram.org/bot' + token + '/' + 'sendMessage' + '?chat_id=' + str(chat_id) + '&text=' + text
    return requests.get(url)


@app.route('/<token>/', methods=['GET', 'POST'])
def index(token):
    token = str(token)
    if request.method == 'POST':
        r = request.get_json()
        chat_id = r['message']['chat']['id']
        try:
            message = r['message']['text']
        except:
            message = False
        try:
            photo_id = r['message']['photo'][-1]['file_id']
        except:
            photo_id = False
        if message:
            send_message(token, chat_id, text='I can classify cats and dogs, send me a photo, please (not a document)')
        elif photo_id:
            get_photo(photo_id, token)
        else:
            send_message(token, chat_id, text='I can classify cats and dogs, send me a photo, please (not a document)')
    return '<h1>test server</h1>'


if __name__ == '__main__':
    app.run()
