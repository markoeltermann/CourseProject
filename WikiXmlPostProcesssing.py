import json
import os.path

with open('./text/AA/wiki_00', encoding='utf-8') as file:
    file_contents = file.read()

json_objects = json.loads(file_contents)

for item in json_objects:
    item_id = item['id']
    if os.path.isfile('./wikidata/' + str(item_id) + '.jpg'):
        with open('./wikidata/' + str(item_id) + '.txt', 'w', encoding='utf-8') as text_file:
            text_file.write(item['text'])
    else:
        with open('./wikidata_no_image/' + str(item_id) + '.txt', 'w', encoding='utf-8') as text_file:
            text_file.write(item['text'])
