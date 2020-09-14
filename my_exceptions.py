import sys

class Usage(Exception):
    
    def __init__(self, stage="train", extra=""):
        if "./" in sys.argv[0]:
            sys.exit(f"Example usage: {sys.argv[0]} datasets/dataset_{stage}.csv{extra}")
        else:
            sys.exit(f"Example usage: ./{sys.argv[0]} datasets/dataset_{stage}.csv{extra}")

class Header(Exception):
    
    def __init__(self):
        sys.exit(f"Header is incorrect for your dataset file '{sys.argv[1]}'")

class File(Exception):
    
    def __init__(self):
        sys.exit(f"Dataset file '{sys.argv[1]}' doesn't exist, is empty or incorrect")

class Dataset(Exception):
    
    def __init__(self):
        sys.exit("Check that your downloaded dataset is correct and hasn't been altered")

class Weights(Exception):
    
    def __init__(self):
        sys.exit(f"Something went wrong with your '{sys.argv[2]}' file. Double check it's correct.")
