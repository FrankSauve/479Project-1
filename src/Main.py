from Preprocessing import create_token_stream, make_blocks
from SPIMI import spimi_invert
from InvertedIndex import create_inverted_index
from Helpers import BColors

while True:
    option = input(BColors.HEADER + "Which action do you want to execute?\n" + BColors.ENDC +
               "1. SPIMI\n"
               "2. Inverted index without compression\n"
               "3. Inverted index with compression\n"
               "0. Exit program\n")

# TODO: Not used for now, maybe uncomment for release if I understand what its used for
# memory_size = int(input("Memory size? "))

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

    elif option == "0":
        exit(0)

