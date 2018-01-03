import nltk
import numpy
import collections
from os import listdir
from nltk.stem import WordNetLemmatizer

wikidata_files = listdir('./wikidata/')

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
        with open('./wikidata/' + wikidata_file, 'r', encoding='utf-8') as text_file:
            text = text_file.read()
        tokens = nltk.word_tokenize(text)
        # tokens = map(lemmatizer.lemmatize())
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
        bags.append(bag_of_words)
        # print(sorted(bag_of_words.items(), key=lambda pair: pair[1], reverse=True))

# sets = list()
# for bag in bags:
#     word_set = set()
#     for key, value in bag:
#         if value > 1:
#             set.add(key)
#     sets.append(word_set)
#
# all_words = frozenset().union(*sets)
# print(len(all_words))
# print(all_words)

combined_bag = dict()
for bag in bags:
    for word, count in bag.items():
        combined_count = combined_bag.get(word)
        if combined_count is None:
            combined_bag[word] = count
        else:
            combined_bag[word] = combined_count + count

print(sum(count > 1 for count in combined_bag.values()))
print(sorted(combined_bag.items(), key=lambda pair: pair[1], reverse=True))


occurence_in_doc = dict()
for word in combined_bag:
    count = 0
    for bag in bags:
        if word in bag:
            count = count + 1
    occurence_in_doc[word] = count


print()
print()
print("Occurences")
print(occurence_in_doc)


