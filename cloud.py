from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

from textblob import TextBlob
#import argparse

#SUBJECTIVE_CUTOFF_POS_SENT = 0.31
#SUBJECTIVE_CUTOFF_NEG_SENT = -0.31
#MAGNITUDE_CUTOFF_SENTENCE = 0.81

#SUBJECTIVE_CUTOFF_POS_TEXT = 0.41
#SUBJECTIVE_CUTOFF_NEG_TEXT = -0.41
#MAGNITUDE_CUTOFF_TEXT = 2.1




'''
IF THE TEXT IS WITHING SUBJECTIVE BOUNDS,
CHECK PASSED. IF THE TEXT IS NOT WITHIN
THE BOUNDS, CHECK MAGNITUDE.
'''



class SentimentParse:
    client = language.LanguageServiceClient()
    SENTIMENT_FLAG = "The sentence: \n \"{}\" \n may be an issue."
    IMPER_FLAG = "The use of imperative verb(s) \"{}\" in the financial sentence: \n \"{}\" \nis discouraged"

    def __init__(self):
        self.RESPONSE_SENT = []

    def analyzeSyntax(self,doc):
        tokens = self.client.analyze_syntax(doc).tokens
        suspicious_verbs = []
        moods = ["UNKNOWN","CONDITIONAL","IMPERATIVE",'INDICATIVE',"INTERROGATIVE","JUSSIVE", "SUBJUNTIVE"]
        for token in tokens:
            try:
                verb_mood = moods[token.part_of_speech.mood]
                if verb_mood == "IMPERATIVE":
                    verb = token.text.content
                    suspicious_verbs.append(verb)
            except:
                print("PANIC!")

        return suspicious_verbs

    def analyze_words(self,doc):
        result = self.client.analyze_entity_sentiment(doc)
        suspicious_words = []
        for entity in result.entities:
            for mention in entity.mentions:
                if (mention.sentiment.score-0.01 > 0.1 or mention.sentiment.score + 0.01 < -0.1) and abs(mention.sentiment.magnitude) > 0.01 and entity.salience > 0.01:
                    suspicious_words.append(mention.text.content)

        return suspicious_words




    #that fishes out the topic of the text
    def check_for_topic(self,document,verbose=True):
        try:
            response = self.client.classify_text(document)
        except:
            return False
        categories = response.categories
        result = {}


        for category in categories:
            # Turn the categories into a dictionary of the form:
            # {category.name: category.confidence}, so that they can
            # be treated as a sparse vector.
            result[category.name] = category.confidence

        if verbose:
            for category in categories:

                if category.confidence > 0.6 and ('/Finance' in category.name or '/Investing' in category.name ):
                    return True

        return False




    #initialize the client and do the handle_result
    def analyze_text(self,email_text):
        """Run a sentiment analysis request on text within a string ."""
        document = types.Document(
            content=email_text,
            type=enums.Document.Type.PLAIN_TEXT)
        annotations = self.client.analyze_sentiment(document=document)
        #sentiment analysis of the entire thing
        #score = annotations.document_sentiment.score
        #magnitude = annotations.document_sentiment.magnitude

        #this passes if the topic is investment related
        if self.check_for_topic(document):
            for index, sentence in enumerate(annotations.sentences):
                doc = types.Document(
                    content=sentence.text.content,
                    type=enums.Document.Type.PLAIN_TEXT)
                suspicious_words = self.analyze_words(doc)
                if suspicious_words != []:
                    resp = self.SENTIMENT_FLAG.format(sentence.text.content)
                    self.RESPONSE_SENT.append(resp) #check that
                suspicious_verbs = self.analyzeSyntax(doc)
                if suspicious_verbs != []:
                    resp = self.IMPER_FLAG.format(", ".join(suspicious_verbs), sentence.text.content)
                    self.RESPONSE_SENT.append(resp) #check that
        return self.RESPONSE_SENT
