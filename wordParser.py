from textblob import TextBlob
import csv
import nltk


"""
Class that parses a email as a string and analyzes it for clearly
inappropriate language
"""
class WordParser:
    PROFANITY_LOCATION = "datasets/swearWords.csv"
    # source https://github.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words
    #creative commons license
    PROFANITY_FLAG_TEXT = "Your use of the word \"{}\" in the sentence \"{}\" may be inappropriate.\nWe recommend you reconsider your wording.\n"

    """
    Constructor fo WordParser class. Builds a list of sentences from email
    with TextBlob and loads the swearWords csv into the dictionary, profanity.

    email - String, to assign to TextBlob object
    response - String, the response message that will be built up from issues
               found by WordParser
    """
    def __init__(self, email):
        self.PROFANITY_LOCATION = "datasets/swearWords.csv"
        # source https://github.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words
        #creative commons license
        self.PROFANITY_FLAG_TEXT = "Your use of the word \"{}\" in the sentence \"{}\" may be inappropriate.\nWe recommend you reconsider your wording.\n\n"

        self.email = TextBlob(email).sentences
        #load csv to self.profanity
        self.profanity = self.csv_to_dict(self.PROFANITY_LOCATION)
        self.response = []

    """
    Reads the swearWords csv file found at PROFANITY_LOCATION into a dictionary
    from the swear word to the number 0. (the value doesnt matter, dict is used for
    fast lookup time)

    file - String, the file path for the csv data
    return assign_dict - the dict the csv data was put into
    """
    def csv_to_dict(self, csv_file):
        #open swearWords file
        with open(csv_file, mode='r') as infile:
            reader = csv.reader(infile)
            #assign values to dictionary
            assign_dict = {rows[0]:0 for rows in reader}
        return assign_dict

    """
    Iterate the email message words searching for profanity.
    If profanity is found, then helpful message for fixing text is appended
    to response.
    """
    def search_profanity(self):
        global PROFANITY_FLAG_TEXT
        #check if each word in the email is profane
        for sent in self.email:
            for word in sent.words:
                if word.lower() in self.profanity:
                    #flag profane word, add it to response
                    self.response.append(self.PROFANITY_FLAG_TEXT.format(word, sent))

    """
    Retrieve the response text. (should be called after search_profanity)

    return - response, the response text with recommended changes
    """
    def get_response(self):
        return self.response
