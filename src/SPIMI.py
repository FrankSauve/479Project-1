
def spimi_invert(token_stream):
    dictionary = {}
    for token in token_stream:
        term, doc_id = token
        if term not in dictionary:
            postings_list = add_to_dictionary(dictionary, term)
        else:
            postings_list = get_postings_list(dictionary, term)
        add_to_postings_list(postings_list, doc_id)
        sorted_terms = sorted(dictionary, key=lambda tup: tup[0], reverse=True)
        write_block_to_disk(sorted_terms, dictionary)

def add_to_dictionary(dictionary, term):
    dictionary[term] = []
    return dictionary[term]

def get_postings_list(dictionary, term):
    return dictionary[term]

def add_to_postings_list(postings_list, doc_id):
    if doc_id not in postings_list:
        postings_list.insert(0, doc_id)

def write_block_to_disk(sorted_terms, dictionary):
    output_file = open("output.txt", "w+")
    output_file.write(str(sorted_terms))
    output_file.write(str(dictionary))



