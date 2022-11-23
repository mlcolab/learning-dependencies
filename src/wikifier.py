import requests
from dotenv import dotenv_values
config = dotenv_values("../.env")
userKey = config['WIKIFIER_USER_KEY']

def get_annotations(text, offset=0):
    print(offset)
    try:
        response = requests.post("http://www.wikifier.org/annotate-article",
            data={"userKey": userKey,
                "lang": "en",
                "text": text,
                "support": "true",
                "ranges": "true"},
        )
        response = response.json()

        for a in response['annotations']:
            for s in a['support']:
                s['chFrom'] += offset
                s['chTo'] += offset

        return response['annotations']
    except Exception:
        print(Exception)
        return []