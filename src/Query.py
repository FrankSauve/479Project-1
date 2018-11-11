from nltk.tokenize import word_tokenize
import os
import json
from LogColors import LogColors
from nltk.stem import PorterStemmer


def query(query_text, filename, using_compression):
    """
    Handles the the various types of query (AND, OR)
    :param query_text: The query string
    :param filename: The name of the file of the inverted index
    :param using_compression: True = With compression, False = No compression
    """
    query_tokens = word_tokenize(query_text)
    using = ""

    if using_compression:
        ps = PorterStemmer()
        query_stemmed = []
        for term in query_tokens:
            stemmed_term = ps.stem(term)
            query_stemmed.append(stemmed_term)
        query_tokens = query_stemmed

    file = open(os.path.abspath(os.path.join(os.getcwd(), "../inverted_index_output", filename)), "r")
    inverted_index = json.load(file)

    for word in query_tokens:
        if word == "AND":
            using = "AND"
            query_tokens.remove("AND")
        elif word == "and":
            using = "AND"
            query_tokens.remove("and")
        elif word == "OR":
            using = "OR"
            query_tokens.remove("OR")
        elif word == "or":
            using = "OR"
            query_tokens.remove("or")

    if using == "AND":
        query_and(query_tokens, inverted_index)
    elif using == "OR":
        query_or(query_tokens, inverted_index)
    # Single word query
    else:
        print(inverted_index[query_tokens[0]])


def query_and(query_tokens, inverted_index):
    """
    Handle queries with the AND keyword
    :param query_tokens: List of query tokens
    :param inverted_index: The compressed or uncompressed inverted index
    """
    postings = []

    for term in query_tokens:
        if term in inverted_index:
            postings.append(set(inverted_index[term]))

    # If there is results
    if len(postings) != 0:
        # Intersect all the postings list
        result_set = set.intersection(*postings)
        result_list = []
        for r in result_set:
            result_list.append(r)

        result_list.sort()

        print(result_list)

    # If there is no result
    else:
        print(LogColors.FAIL + "\nNo results found" + LogColors.ENDC)


def query_or(query_tokens, inverted_index):
    """
    Handle queries with the OR keyword
    :param query_tokens: List of query tokens
    :param inverted_index: The compressed or uncompressed inverted index
    """
    postings = []

    for term in query_tokens:
        if term in inverted_index:
            postings += inverted_index[term]

    # If there is results
    if len(postings) != 0:
        results_tuples = []
        for posting in postings:
            # To avoid repetition in the results
            if (postings.count(posting), posting) not in results_tuples:
                results_tuples.append((postings.count(posting), posting))

        # Sort by count
        results_tuples.sort(reverse=True)

        results = []
        for r in results_tuples:
            count, doc_id = r
            results.append(doc_id)

        print(results)

    # If there is no result
    else:
        print(LogColors.FAIL + "\nNo results found" + LogColors.ENDC)
