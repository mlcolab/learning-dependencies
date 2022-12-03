import aiohttp
import asyncio
import time
import pandas as pd
import numpy as np
import unicodedata
import pickle

from dotenv import dotenv_values
config = dotenv_values("../.env")
userKey = config['WIKIFIER_USER_KEY']

start_time = time.time()
batch_size = 5000
next_delay = 7

async def get_annos(session, url, text, offset):
    global next_delay
    next_delay += delay
    await asyncio.sleep(next_delay)
    print(offset)
    data={"userKey": userKey,
                "lang": "en",
                "text": text,
                "support": "true",
                "ranges": "true"}
           
    async with session.post(url, data=data) as response:
        print(response.status)
        try:
            annos = await response.json()
            for a in annos['annotations']:
                for s in a['support']:
                    s['chFrom'] += offset
                    s['chTo'] += offset
            print("Received "+ str(offset))
            return annos['annotations']
        except Exception as e:
            print("Error in "+ str(offset))
            print(str(e))
            return []
        

async def main(text):
    async with aiohttp.ClientSession() as session:
        tasks = []
        batches = int(np.floor(len(text)/batch_size))
        for i in range(batches):
            url = f'http://www.wikifier.org/annotate-article'
            tasks.append(asyncio.ensure_future(get_annos(session, url, text[i*batch_size:(i+1)*batch_size], i*batch_size)))
        annos = await asyncio.gather(*tasks)
        file = open("../dat/annotations/Beezer_First_Course.pkl", 'wb')
        pickle.dump([item for sublist in annos for item in sublist], file)
        file.close()

delay = 7
data = pd.read_json("../dat/parsed_books/parsed_books.json")
text = unicodedata.normalize("NFKD", " ".join(data.pages[0]))
#print(text)
asyncio.run(main(text))
print("--- %s seconds ---" % (time.time() - start_time))