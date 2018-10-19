def spimi_invert(output_file, token_stream):
    dictionary = {}
    for token in token_stream:
        term, doc_id = token
        if term not in dictionary:
            postings_list = add_to_dictionary(dictionary, term)
        else:
            postings_list = get_postings_list(dictionary, term)
        add_to_postings_list(postings_list, doc_id)
    sorted_terms = sorted(dictionary, key=lambda x: x[0], reverse=True)
    write_block_to_disk(output_file, sorted_terms, dictionary)


def add_to_dictionary(dictionary, term):
    dictionary[term] = []
    return dictionary[term]


def get_postings_list(dictionary, term):
    return dictionary[term]


def add_to_postings_list(postings_list, doc_id):
    postings_list.insert(0, doc_id) if doc_id not in postings_list else postings_list


def write_block_to_disk(output_file, sorted_terms, dictionary):
    output_file.write(str(sorted_terms))
    output_file.write(str(dictionary))


def make_blocks(block_size, token_stream):
    blocks = []
    block = []
    in_new_doc = False
    for token in token_stream:
        term, doc_id = token
        if int(doc_id) % block_size == 0 and not in_new_doc:
            blocks.append(block)
            block = []
            in_new_doc = True
        elif int(doc_id) % block_size == 2:
            in_new_doc = False
        block.append(token)

    return blocks
