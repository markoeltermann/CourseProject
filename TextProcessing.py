import nltk
import numpy
import collections
from os import listdir
from nltk.stem import WordNetLemmatizer

wikidata_files = listdir('./wikidata_train/')

i = 0

lemmatizer = WordNetLemmatizer()


def universal_word_type_to_wordnet(word_type):
    if word_type == 'NOUN':
        return 'n'
    elif word_type == 'ADJ':
        return 'a'
    else:
        raise Exception()


bags = list()

for wikidata_file in wikidata_files:
    if wikidata_file.endswith('.txt'):
        with open('./wikidata_train/' + wikidata_file, 'r', encoding='utf-8') as text_file:
            text = text_file.read()
        tokens = nltk.word_tokenize(text)
        pos_tags = nltk.pos_tag(tokens, 'universal')
        lemmatized_nouns_and_adverbs = map(
            lambda pair: lemmatizer.lemmatize(pair[0], universal_word_type_to_wordnet(pair[1])),
            filter(lambda pair: (pair[1] == 'NOUN' or pair[1] == 'ADJ') and len(pair[0]) > 1, pos_tags))
        bag_of_words = dict()
        for word in lemmatized_nouns_and_adverbs:
            word = word.lower()
            count = bag_of_words.get(word)
            if count is None:
                bag_of_words[word] = 1
            else:
                bag_of_words[word] = count + 1

        new_bag_of_words = dict()
        for word, count in bag_of_words.items():
            new_bag_of_words[word] = count / len(tokens)


        bags.append(new_bag_of_words)



combined_bag = dict()
occurences = dict()
for bag in bags:
    for word, count in bag.items():
        combined_count = combined_bag.get(word)
        if combined_count is None:
            combined_bag[word] = count
            occurences[word] = 1
        else:
            combined_bag[word] = combined_count + count
            occurences[word] = occurences[word] + 1

print(sum(count > 1 for count in combined_bag.values()))
print(sorted(combined_bag.items(), key=lambda pair: pair[1], reverse=False))



word_list = []
for word in combined_bag:
    if occurences[word] > 2 and occurences[word] < 51:
        word_list.append(word)



allowed_words = set()
for word in word_list:
    allowed_words.add(word)


for wikidata_file in wikidata_files:
    if wikidata_file.endswith('.txt'):
        with open('./wikidata_train/' + wikidata_file, 'r', encoding='utf-8') as text_file:
            text = text_file.read()
        tokens = nltk.word_tokenize(text)
        pos_tags = nltk.pos_tag(tokens, 'universal')
        lemmatized_nouns_and_adverbs = map(
            lambda pair: lemmatizer.lemmatize(pair[0], universal_word_type_to_wordnet(pair[1])),
            filter(lambda pair: (pair[1] == 'NOUN' or pair[1] == 'ADJ') and len(pair[0]) > 1, pos_tags))
        bag_of_words = dict()
        words_to_write = []
        for word in lemmatized_nouns_and_adverbs:
            if word in allowed_words:
                words_to_write.append(word)
        with open('./mallet_train/' + wikidata_file, 'w', encoding='utf-8') as out_file:
            for word in words_to_write:
                out_file.write(" " + word)