from Preprocessing import create_token_stream, make_blocks
from SPIMI import spimi_invert
from InvertedIndex import create_inverted_index

option = input("Which action do you want to execute?\n1. SPIMI\n2. Inverted index without compression\n")

# TODO: Not used for now, maybe uncomment for release if I understand what its used for
# memory_size = int(input("Memory size? "))
block_size = int(input("Block size? "))

print("Creating token stream...")
token_stream = create_token_stream()
print("Token stream created!\n")

if option == "1":
    print("Processing SPIMI...")
    blocks = make_blocks(block_size, token_stream)
    for i, block in enumerate(blocks):
        print(str(i + 1))
        output_file = open("../DISK/BLOCK" + str(i + 1) + ".json", "w+")
        spimi_invert(output_file, block)

    print("SPIMI done!\n")

elif option == "2":
    print("Creating inverted index...")
    create_inverted_index()
    print("Inverted index created!\n")

