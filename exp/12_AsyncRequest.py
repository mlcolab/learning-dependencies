## This file uses asyncio to quickly annotate textbook contents with Wikipedia articles.

import aiohttp
import asyncio
import time
import pandas as pd
import numpy as np
import pickle

from dotenv import dotenv_values
config = dotenv_values("../.env")
userKey = config['WIKIFIER_USER_KEY']

start_time = time.time()
batch_size = 5000
next_delay = 10

async def get_annos(session, url, text, offset):
    global next_delay
    next_delay += delay
    await asyncio.sleep(next_delay)
    print("Request "+ str(offset))
    data={"userKey": userKey,
                "lang": "en",
                "text": text,
                "support": "true",
                "ranges": "true"}
    try:
        async with session.post(url, data=data) as response:
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
        

async def main():
    async with aiohttp.ClientSession() as session:
        data = pd.read_json("../dat/parsed_books/parsed_books.json")
        for i in range(3,10):
            title = data.index[i]
            print(title)
            text = " ".join(data.pages[i])
            print(len(text))
            
            tasks = []
            batches = int(np.floor(len(text)/batch_size))
            for i in range(batches):
                url = f'http://www.wikifier.org/annotate-article'
                tasks.append(asyncio.ensure_future(get_annos(session, url, text[i*batch_size:(i+1)*batch_size], i*batch_size)))
            annos = await asyncio.gather(*tasks)
            file = open("../dat/annotations/" + title + ".pkl", 'wb')
            pickle.dump([item for sublist in annos for item in sublist], file)
            file.close()

delay = 10
loop = asyncio.get_event_loop()
loop.run_until_complete(main())

print("--- %s seconds ---" % (time.time() - start_time))