from os import listdir
from os.path import splitext
from sklearn.model_selection import train_test_split
from os import makedirs
from os.path import exists
import shutil

wikidata_files = listdir('./wikidata/')

items = set()

for file in wikidata_files:
    name, ext = splitext(file)
    items.add(name)

train_set, test_set = train_test_split(list(items), train_size=0.8)


def copy_items_to_folder(itemset, folder_name):
    if not exists('./' + folder_name + '/'):
        makedirs('./' + folder_name + '/')
    for item in itemset:
        shutil.copyfile('./wikidata/' + item + '.txt', './' + folder_name + '/' + item + '.txt')
        shutil.copyfile('./wikidata/' + item + '.jpg', './' + folder_name + '/' + item + '.jpg')


copy_items_to_folder(train_set, 'wikidata_train')
copy_items_to_folder(test_set, 'wikidata_test')
