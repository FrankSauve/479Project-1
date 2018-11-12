import os
import pickle
from Preprocessing import create_token_stream, make_blocks, get_corpus
from SPIMI import spimi_invert
from InvertedIndex import create_inverted_index
from LogColors import LogColors
from Query import query
from BM25 import BM25


while True:
    option = input(LogColors.HEADER + "\nWhich action do you want to execute?\n" + LogColors.ENDC +
                   "1. SPIMI\n"
                   "2. Inverted index without compression\n"
                   "3. Inverted index with compression\n"
                   "4. Execute a query\n"
                   "0. Exit program\n")

    if option == "1":
        block_size = int(input("Block size? "))
        print("Creating token stream...")
        token_stream = create_token_stream()
        print("Token stream created!\n")

        print("Processing SPIMI...")
        blocks = make_blocks(block_size, token_stream)
        for i, block in enumerate(blocks):
            if i < 9:
                index = "0" + str(i + 1)
            else:
                index = str(i + 1)
            output_file = open("../DISK/BLOCK" + index + ".json", "w+")
            spimi_invert(output_file, block)

        print("SPIMI done!\n")

    elif option == "2":
        print("Creating inverted index...")
        create_inverted_index(False)
        print("Inverted index created!\n")

    elif option == "3":
        print("Creating inverted index...")
        create_inverted_index(True)
        print("Inverted index created!\n")

    elif option == "4":
        compression_option = input(LogColors.HEADER + "Do you want to search in the compressed or uncompressed inverted "
                                                    "index?" + LogColors.ENDC + "\n1. Uncompressed\n2. Compressed\n")

        query_text = input("Enter your query separated by " + LogColors.BOLD + "AND " + LogColors.ENDC + "or" +
                           LogColors.BOLD + " OR" + LogColors.ENDC + ":\n")

        if compression_option == "1":
            filename = "no_compression.json"
            query(query_text, filename, False)
        elif compression_option == "2":
            filename = "with_compression.json"
            query(query_text, filename, True)

    elif option == "5":
        print("Creating corpus...")
        corpus = get_corpus()
        print("Corpus created!")
        print("Creating BM25...")
        bm25 = BM25(corpus[:10])
        with open(os.path.abspath(os.path.join(os.getcwd(), "../pickles/bm25.pkl")), "wb") as pickle_file:
            pickle.dump(bm25, pickle_file)
        print("BM25 created!")

    elif option == "6":
        with open(os.path.abspath(os.path.join(os.getcwd(), "../pickles/bm25.pkl")), "rb") as pickle_file:
            bm25 = pickle.load(pickle_file)
        bm25.ranked(["the"], 10)

    elif option == "0":
        exit(0)
