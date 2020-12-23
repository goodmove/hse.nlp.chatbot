import sys

import logging
import pathlib

import razdel
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, AutoModel
import numpy as np


model_name = "DeepPavlov/rubert-base-cased-sentence"
DEFAULT_TOKENIZER = AutoTokenizer.from_pretrained(model_name)
DEFAULT_MODEL = AutoModel.from_pretrained(model_name)


def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0] #First element of model_output contains all token embeddings
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
    sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
    return sum_embeddings / sum_mask


def sentences_to_embeddings(sentences, tokenizer = None, model = None):
    #Tokenize sentences
    if not tokenizer:
        tokenizer = DEFAULT_TOKENIZER
    if not model:
        model = DEFAULT_MODEL

    encoded_input = tokenizer(sentences, padding=True, truncation=True, max_length=128, return_tensors='pt')
    #Compute token embeddings
    with torch.no_grad():
        model_output = model(**encoded_input)
    sentence_embeddings = mean_pooling(model_output, encoded_input['attention_mask'])
    return sentence_embeddings


def _razdel_split_into_sentences(text):
    return razdel.sentenize(text)


def split_text_to_sentences(text):
    return [x.text for x in _razdel_split_into_sentences(text)]

def preprocess_input(text_sample):
    text_sample = text_sample.replace('\n', '').lower()
    return np.array([x.numpy() for x in sentences_to_embeddings([text_sample])[0]])