import json
import requests
from tqdm import tqdm


def top_ten_similar(word):
    print(word)
    if "  " in word:
        word = word.strip().replace(' ', '%20').lower()
        print(word)
    r = requests.get('https://relatedwords.org/api/related?term=' + word)
    json_data = json.dumps(r.json())
    data = json.loads(json_data)
    data = sorted(data, key=lambda k: k['score'] or 0, reverse=True)
    return [x['word'] for x in data[:6]]


def print_every_similar_word(file):
    sleep = 0
    with open("output.json", "w", encoding="utf-8") as file_object:
        file = open(file, encoding='utf8')
        arr = json.load(file)
        dict = {}
        for i in tqdm(range(len(arr))):
            list = arr[i].split(',')
            print(list)
            for j in list:
                if j.strip() != '':
                    a = top_ten_similar(j)
                    print("api answer================",a)
                    dict[j] = a
                else:
                    continue
        json.dump(dict, file_object)


print_every_similar_word('distinct_keywords.json')
