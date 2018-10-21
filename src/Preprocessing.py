import os
from nltk.tokenize import word_tokenize


def create_token_stream():
    """
    Gets the token stream (term, doc_id) from all the reuters documents.
    :return list token_stream: List of (term, doc_id) tuples
    """
    token_stream = []

    # Loop through all files in reuters
    for filename in os.listdir("../reuters"):
        file = open(os.path.abspath(os.path.join(os.getcwd(), "../reuters", filename)), "r")
        lines = file.readlines()

        inside_body = False
        for line in lines:
            if "NEWID=" in line:
                index_new_id = line.index("NEWID=") + 7  # Add seven because seven characters in NEWID="
                index_end_id = line[index_new_id:].index('"')  # Get the index of the next "
                doc_id = line[index_new_id:(index_new_id + index_end_id)]  # Get the doc_id

            if "<BODY>" in line:
                index_body = line.index("<BODY>") + 6  # Add six because six characters in <BODY>
                inside_body = True  # We are inside the BODY tags
                tokenized_line = word_tokenize(line[index_body:])  # Tokenize the line after the tag
                for token in tokenized_line:
                    token_stream.append((token, doc_id))  # Add each term and doc_id to the token_stream

            elif "</BODY>" in line:
                index_body = line.index("</BODY>")
                inside_body = False  # We are at the end of the BODY tags
                tokenized_line = word_tokenize(line[:index_body])  # Tokenize the line before the tag
                for token in tokenized_line:
                    token_stream.append((token, doc_id))  # Add each term and doc_id to the token_stream

            elif inside_body:  # We are already inside the body
                tokenized_line = word_tokenize(line)  # Tokenize the entire line
                for token in tokenized_line:
                    token_stream.append((token, doc_id))  # Add each term and doc_id to the token_stream
    return token_stream


def make_blocks(block_size, token_stream):
    """
    Creates blocks from the token_stream
    :param block_size: Number of documents in the block
    :param token_stream: Tokens (term, doc_id) to separated into blocks
    :return: A list of all the blocks
    """
    blocks = []
    block = []
    in_new_doc = False
    for token in token_stream:
        term, doc_id = token
        if int(doc_id) % block_size == 0 and not in_new_doc:  # Reached the block_size
            blocks.append(block)
            block = []
            in_new_doc = True
        elif int(doc_id) % block_size == 1:
            in_new_doc = False
        block.append(token)
    blocks.append(block)

    return blocks
