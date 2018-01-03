#!/bin/bash

source env.sh

rm -rf mallet_train
mkdir mallet_train

cp wikidata_train/*.txt mallet_train/

$MALLET_HOME/bin/mallet import-dir \
	--input mallet_train/ \
	--output mallet-topic-input.mallet \
	--keep-sequence \
	--remove-stopwords

echo Starting training

$MALLET_HOME/bin/mallet train-topics \
	--input mallet-topic-input.mallet \
	--num-topics 10 \
	--inferencer-filename mallet-inferencer.mallet \
	--output-topic-keys mallet-topics.txt \
	--output-doc-topics mallet-topic-composition.txt \
	--output-state mallet-topic-state.gz


