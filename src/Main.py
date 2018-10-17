from Preprocessing import get_token_stream
from SPIMI import spimi_invert

print("Starting preprocessing...")
token_stream = get_token_stream()
print("Done preprocessing.\n")

print("Starting SPIMI...")
spimi_invert(token_stream)
print("Done preprocessing.\n")
