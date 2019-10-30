import requests
import config


token = config.token
URL = 'https://api.telegram.org/bot' + token + '/'


def get_updates():
    url = URL + 'getupdates'
    print(url)
    r = requests.get(url)
    return r.json()


def get_message():
    data = get_updates()
    chat_id = data['result'][-1]['message']['chat']['id']
    message_text = data['result'][-1]['message']['text']
    message = {'chat_id': chat_id,
               'text': message_text}
    return message


def main():
    print(get_updates())


if __name__ == '__main__':
    main()
