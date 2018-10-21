import json


def spimi_invert(output_file, token_stream):
    """
    Performs the single-pass in-memory indexing algorithm
    Output is found in /DISK/BLOCKXX.json
    :param output_file: The file where the output will be written to disk
    :param token_stream: The token (term, doc_id) stream
    """
    dictionary = {}  # Create empty dictionary
    for token in token_stream:  # Loop through tokens
        term, doc_id = token
        doc_id = int(doc_id)
        if term not in dictionary:
            postings_list = add_to_dictionary(dictionary, term)  # Add to dictionary if the term is not in it
        else:
            postings_list = get_postings_list(dictionary, term)  # Fetch the postings list if the term is in the dict
        add_to_postings_list(postings_list, doc_id)  # Add doc_id to postings_list
    sorted_terms = sorted(dictionary, key=lambda x: x[0])  # Sort terms in ascending order
    write_block_to_disk(output_file, sorted_terms, dictionary)  # Store sorted_terms and dictionary to disk


def add_to_dictionary(dictionary, term):
    """
    Add a term to the dictionary and returns the postings_list of the term
    :param dictionary: Dictionary of postings lists
    :param term: The term to add to dictionary
    :return: The postings list of the term
    """
    dictionary[term] = []
    return dictionary[term]


def get_postings_list(dictionary, term):
    """
    Returns the postings list of the term
    :param dictionary: Dictionary of postings lists
    :param term: The term to fetch
    :return: The postings list of the term
    """
    return dictionary[term]


def add_to_postings_list(postings_list, doc_id):
    """
    Adds a doc_id to the postings_list if it is not already there
    :param postings_list: Postings list of a term
    :param doc_id: The doc_id where the term was found
    """
    if doc_id not in postings_list:
        postings_list.append(doc_id)


def write_block_to_disk(output_file, sorted_terms, dictionary):
    """
    Writes the sorted_terms and dictionary to a json file
    :param output_file: A json file
    :param sorted_terms: List of sorted terms
    :param dictionary: Dictionary of all the postings list
    """
    data = {"sorted_terms": sorted_terms, "dictionary": dictionary}
    json.dump(data, output_file, indent=4)



