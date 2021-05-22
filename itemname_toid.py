import json
import os


def createnew():
    file = open('compress.json', encoding="utf-8")
    db = json.load(file)
    file.close()

    if os.path.exists('itemname_toid.json'):
        os.remove('itemname_toid.json')

    id_mapping = open('itemname_toid.json', 'w', encoding="utf-8")
    id_mapping.write('{\n')
    for i in range(len(db['items'])):
        print(f'writing: {db["items"][i]["name"]}')

        if 'remapID' in db['items'][i]:
            id_mapping.write(f'"{db["items"][i]["name"]}": {db["items"][i]["remapID"]}')
        else:
            id_mapping.write(f'"{db["items"][i]["name"]}": {db["items"][i]["id"]}')
        if i != len(db['items']) - 1:
            id_mapping.write(',\n')
    id_mapping.write('\n}')
    id_mapping.close()
