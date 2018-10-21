import json
import os
import re
from nltk.corpus import stopwords
from Helpers import BColors
from nltk.stem import PorterStemmer


def create_inverted_index(with_compression):
    """
    Creates the inverted index without compression
    Output is found in /inverted_index_output/no_compression.json
    :param with_compression: Boolean to determine if the lossy compression should be used
    """
    if with_compression:
        output_file = open("../inverted_index_output/with_compression.json", "w+")
    else:
        output_file = open("../inverted_index_output/no_compression.json", "w+")

    inverted_index = {}
    for filename in os.listdir("../DISK"):  # Loop through all the blocks
        file = open(os.path.abspath(os.path.join(os.getcwd(), "../DISK", filename)), "r")
        data = json.load(file)
        dictionary = data["dictionary"]

        for term in dictionary:
            add_term_to_inverted_index(term, dictionary, inverted_index)  # Merge the blocks

    if with_compression:
        print("Uncompressed length:", BColors.OKBLUE, len(inverted_index), BColors.ENDC)
        remove_numbers(inverted_index)
        print("Length after removing numbers:", BColors.OKBLUE, len(inverted_index), BColors.ENDC)
        case_fold(inverted_index)
        print("Length after case folding:", BColors.OKBLUE, len(inverted_index), BColors.ENDC)
        remove_stop_words(inverted_index)
        print("Length after removing stop words:", BColors.OKBLUE, len(inverted_index), BColors.ENDC)
        stem_words(inverted_index)
        print("Length after stemming", BColors.OKBLUE, len(inverted_index), BColors.ENDC)

    json.dump(inverted_index, output_file, indent=4)


def add_term_to_inverted_index(term, dictionary, inverted_index):
    """
    Adds the postings_list to the inverted_index
    :param term: The term to add
    :param dictionary: The dictionary containing the term
    :param inverted_index: The inverted_index that the postings_list will be added
    """
    if term in inverted_index:
        for doc_id in dictionary[term]:
            inverted_index[term].append(doc_id)
    else:
        inverted_index[term] = []
        for doc_id in dictionary[term]:
            inverted_index[term].append(doc_id)


def remove_numbers(dictionary):
    """
    Removes numbers from the dictionary
    :param dictionary: Dictionary of postings list
    """
    to_remove = []
    for term in dictionary:
        if re.match(r'\d+', term):
            to_remove.append(term)

    for term in to_remove:
        del dictionary[term]


def case_fold(dictionary):
    to_remove = []
    for term in dictionary:
        if term.lower() in dictionary:
            if term != term.lower():
                to_remove.append(term)
                for doc_id in dictionary[term]:
                    if doc_id not in dictionary[term.lower()]:
                        dictionary[term.lower()].append(doc_id)
                        dictionary[term.lower()].sort()

    for term in to_remove:
        del dictionary[term]


def remove_stop_words(dictionary):
    """
    Removes stop words from the dictionary using nltk stopwords
    :param dictionary:
    :return:
    """
    to_remove = []
    stop_words = set(stopwords.words("english"))
    for term in dictionary:
        if term in stop_words:
            to_remove.append(term)

    for term in to_remove:
        del dictionary[term]


def stem_words(dictionary):
    ps = PorterStemmer()
    to_remove = []
    to_add = {}
    for term in dictionary:
        stemmed_term = ps.stem(term)
        if stemmed_term in to_add:
            if term != stemmed_term:
                to_remove.append(term)
                for doc_id in dictionary[term]:
                    if doc_id not in to_add[stemmed_term]:
                        to_add[stemmed_term].append(doc_id)
                        to_add[stemmed_term].sort()
        else:
            for doc_id in dictionary[term]:
                to_add[stemmed_term] = []
                to_add[stemmed_term].append(doc_id)

    # TODO: Continue here: Problem is that terms are not getting deleted from the dictionary
    # TODO: Also when the stemmed_terms are added they become a list inside of a list
    for term in to_add:
        if term not in dictionary:
            dictionary[term] = []
        dictionary[term].append(to_add[term])
        # dictionary[term].sort()

    for term in to_remove:
        del dictionary[term]





