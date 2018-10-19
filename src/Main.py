from Preprocessing import get_token_stream
from SPIMI import spimi_invert, make_blocks

# No used for now
# memory_size = int(input("Memory size? "))
block_size = int(input("Block size? "))

print("Pre-processing...")
token_stream = get_token_stream()
print("Done pre-processing.\n")

print("Processing SPIMI...")
blocks = make_blocks(block_size, token_stream)
for i, block in enumerate(blocks):
    print(i)
    output_file = open("../DISK/BLOCK" + str(i+1) + ".txt", "w+")
    spimi_invert(output_file, block)

print("Done SPIMI.\n")
