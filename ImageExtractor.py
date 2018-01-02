from wptools import *
import requests
from os.path import splitext
import os
import mwparserfromhell

landscape_category = category('Category:Landscape paintings', silent=True)

landscape_category.get_members()

if not os.path.exists('./wikidata/'):
    os.makedirs('./wikidata/')

if not os.path.exists('./wikidata_no_image/'):
    os.makedirs('./wikidata_no_image/')

for item in landscape_category.data['members']:
    pageid = item['pageid']
    p = page(pageid=pageid, silent=True)
    # p.get_parse()
    # p.get_wikidata()
    p.get()
    image = p.data.get('image')
    if image:
        image_url = image[0]['url']
        image = requests.get(image_url)
        with open('./wikidata/' + str(p.params['pageid']) + '.txt', 'w', encoding='utf-8') as text_file:
            article_wikitext = str(p.data['wikitext'])
            parsed_text = mwparserfromhell.parse(article_wikitext)
            article_text = parsed_text.strip_code()
            text_file.write(article_text)
        _, extension = splitext(image_url)
        with open('./wikidata/' + str(p.params['pageid']) + extension, 'wb') as image_file:
            image_file.write(image.content)
        print(image_url)
    else:
        with open('./wikidata_no_image/' + str(p.params['pageid']) + '.txt', 'w', encoding='utf-8') as text_file:
            article_text = str(p.data.get('extext'))
            if article_text is not None:
                article_text = article_text.replace('_', '').replace('*', '')
                text_file.write(article_text)
            else:
                print('No text for ' + p.params['title'])
        print('No image for ' + p.params['title'])
