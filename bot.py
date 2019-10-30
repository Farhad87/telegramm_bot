import requests
import config


token = config.token
URL = 'https://api.telegram.org/bot' + token + '/'

def get_updates():
    url = URL + 'getupdates'
    print(url)
    r = requests.get(url)
    return r

def main():
    print(get_updates())


if __name__ == '__main__':
    main()