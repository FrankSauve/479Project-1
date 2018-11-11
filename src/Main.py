from Preprocessing import create_token_stream, make_blocks
from SPIMI import spimi_invert
from InvertedIndex import create_inverted_index
from LogColors import LogColors
from Query import query

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

    elif option == "0":
        exit(0)
