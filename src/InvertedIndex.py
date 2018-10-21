import json


def create_inverted_index():
    file = open("../DISK/BLOCK1.json", "r")
    data = json.load(file)

    print(str(data["sorted_terms"]))
