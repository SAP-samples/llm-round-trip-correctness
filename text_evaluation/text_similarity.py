from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer, util
import pandas as pd
import re
import numpy as np


model = SentenceTransformer('Alibaba-NLP/gte-large-en-v1.5', trust_remote_code=True)


""" this function returns the cosine similarity betweeen 2 documents using pre-trained BERT model """
def sts_bert(t1,t2):
    try:
        sentences = [t1, t2]
        embedding_1= model.encode(sentences[0], convert_to_tensor=True)
        embedding_2 = model.encode(sentences[1], convert_to_tensor=True)
        score = util.pytorch_cos_sim(embedding_1, embedding_2)
        score = score.tolist()
        score = round(score[0][0], 2)
    except:
        score = 0
    return score

import nltk
from nltk.metrics import edit_distance

nltk.download("punkt_tab")


def get_sentences(text_1):
    """
    tekoneizes text in sentences
    """
    return nltk.sent_tokenize(text_1)


def sequence_similarity(sentences_1, sentences_2):
    """
    Calculate a sequence similarity based on normalized edit distance on sentences
    """
    return 1 - (edit_distance(sentences_1, sentences_2) / max(len(sentences_1), len(sentences_2)))


def align_sentences(text1_sentences, text2_sentences, threshold=0.75):
    """
    Given two lists of sentences, adjusts list2 based on similarity to list1.

    Args:
        sentences_1 (list): List of sentences.
        sentences_2 (list): List of sentences.

    Returns:
        list: Adjusted second list of sentences.

    """
    # Adjust text2 sentences
    adjusted_text2_sentences = text2_sentences[:]

    for sentence_1 in text1_sentences:
        best_similarity = 0
        best_index = -1
        for j, sentence_2 in enumerate(text2_sentences):
            similarity = sts_bert(sentence_1, sentence_2)  # Use the custom similarity function
            if similarity > best_similarity:
                best_similarity = similarity
                best_index = j
        if best_similarity >= threshold:
            adjusted_text2_sentences[best_index] = sentence_1

    return adjusted_text2_sentences

def text_similarity_alternative(file_1, file_2, threshold=0.8):
    """
    Args:
        file_1, file_2:  2 input text files.
    Returns:
        float: an overall similarity score.
    """
    sentences_1 = get_sentences(file_1)
    sentences_2 = get_sentences(file_2)
    adjusted_sen2 = align_sentences(sentences_1, sentences_2, threshold=threshold)
    seq_similarity = sequence_similarity(sentences_1, adjusted_sen2)
    overall_sim = 0.5 * sts_bert(file_1, file_2) + 0.5 * seq_similarity
    return overall_sim

def calculate_precision_recall(groundt, generated):
    """
    Calculate precision and recall based on set similarity of aligned sentences.

    Args:
        ground_truth (list): List of sentences from the ground truth.
        generated (list): List of sentences from the generated text.

    Returns:
        tuple: (precision, recall)
    """
    intersection = set(groundt).intersection(set(generated))
    precision = len(intersection) / len(generated) if generated else 0
    recall = len(intersection) / len(groundt) if groundt else 0
    return precision, recall



