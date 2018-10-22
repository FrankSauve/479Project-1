from nltk.tokenize import word_tokenize

def query(query):
    query = word_tokenize(query)
    print(query)
