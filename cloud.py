from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

from textblob import TextBlob
#import argparse

SUBJECTIVE_CUTOFF_POS_SENT = 0.31
SUBJECTIVE_CUTOFF_NEG_SENT = -0.31
MAGNITUDE_CUTOFF_SENTENCE = 0.81

SUBJECTIVE_CUTOFF_POS_TEXT = 0.41
SUBJECTIVE_CUTOFF_NEG_TEXT = -0.41
MAGNITUDE_CUTOFF_TEXT = 2.1

client = language.LanguageServiceClient()

SENTIMENT_FLAG = "The use of word(s) \"{}\" in the sentence: \n \"{}\" \n was found questionable by our \
super smart machine! Reconsider your life choices. \n"

RESPONSE_SENT = ""
IMPER_FLAG = " The use of imperative verb(s) \"{}\" in the sentence: \n \"{}\" \nis discouraged"

'''
IF THE TEXT IS WITHING SUBJECTIVE BOUNDS,
CHECK PASSED. IF THE TEXT IS NOT WITHIN
THE BOUNDS, CHECK MAGNITUDE.
'''



def analyze_syntax(doc):
    tokens = client.analyze_syntax(doc).tokens
    suspicious_verbs = []
    moods = ["UNKNOWN","CONDITIONAL","IMPERATIVE",'INDICATIVE',"INTERROGATIVE","JUSSIVE", "SUBJUNTIVE"]
    for token in tokens:
        try:
            verb_mood = moods[token.part_of_speech.mood]
            if verb_mood == "IMPERATIVE":
                verb = token.text.content
                suspicious_verbs.append(verb)
        except:
            print("nothign")
    print("got verbs:",suspicious_verbs)
    return suspicious_verbs

def analyze_words(doc):
    result = client.analyze_entity_sentiment(doc)
    entity_type = ('UNKNOWN', 'PERSON', 'LOCATION', 'ORGANIZATION',
        'EVENT', 'WORK_OF_ART', 'CONSUMER_GOOD', 'OTHER')
    suspicious_words = []
    for entity in result.entities:
        print('Mentions: ')
        print(u'Name: "{}"'.format(entity.name))
        for mention in entity.mentions:
            print(u'  Begin Offset : {}'.format(mention.text.begin_offset))
            print(u'  Content : {}'.format(mention.text.content))
            print(u'  Magnitude : {}'.format(mention.sentiment.magnitude))
            print(u'  Sentiment : {}'.format(mention.sentiment.score))
            print(u'  Type : {}'.format(entity_type[entity.type]))
            if (mention.sentiment.score-0.01 > 0 or mention.sentiment.score + 0.01 < 0) and abs(mention.sentiment.magnitude) > 0.01 and entity.salience > 0.01:
                suspicious_words.append(mention.text.content)

        print(u'Salience: {}'.format(entity.salience))
        print(u'Sentiment: {}\n'.format(entity.sentiment))
    print("Suspicious words:",suspicious_words)
    return suspicious_words
            

    

#that fishes out the topic of the text
def check_for_topic(document,verbose=True):
    response = client.classify_text(document)
    categories = response.categories
    result = {}
    

    for category in categories:
        # Turn the categories into a dictionary of the form:
        # {category.name: category.confidence}, so that they can
        # be treated as a sparse vector.
        result[category.name] = category.confidence
    
    if verbose:
        
        for category in categories:
            '''
            print(u'=' * 20)
            print(u'{:<16}: {}'.format('category', category.name))
            print(u'{:<16}: {}'.format('confidence', category.confidence))
            '''
            print(category.confidence)
            print(category.name)
            if category.confidence > 0.8 and ('/Finance' in category.name or '/Investing' in category.name ):
                return True

    return False




#initialize the client and do the handle_result
def analyze_text(email_text):
    global IMPER_FLAG
    global RESPONSE_SENT
    """Run a sentiment analysis request on text within a string ."""
    #client = language.LanguageServiceClient()
    print("analyze text")
    document = types.Document(
        content=email_text,
        type=enums.Document.Type.PLAIN_TEXT)
    annotations = client.analyze_sentiment(document=document)
    
    #sentiment analysis of the entire thing
    score = annotations.document_sentiment.score
    magnitude = annotations.document_sentiment.magnitude
    print("score:",score)
    print("magnitude",magnitude)

    #this passes if the topic is investment related
    if check_for_topic(document):
        for index, sentence in enumerate(annotations.sentences):
            doc = types.Document(
                content=sentence.text.content,
                type=enums.Document.Type.PLAIN_TEXT)
            suspicious_words = analyze_words(doc)
            if suspicious_words != []:
                resp = SENTIMENT_FLAG.format(",".join(suspicious_words), sentence.text.content)
                RESPONSE_SENT += resp #check that
            suspicious_verbs = analyze_syntax(doc)
            if suspicious_verbs != []:
                resp = IMPER_FLAG.format(",".join(suspicious_verbs), sentence.text.content)
                RESPONSE_SENT += resp #check that
    print(RESPONSE_SENT)

    


 




if __name__ == '__main__':

    # ignore parsing for now
    email = u"If you invest in my fund you will get 10% monthly returns. I guarantee ten percent annual returns. TSLA will fall 20% tomorrow. Everyone will be short selling APPL next month. I can guarantee your principal. I know that Netflix will go up this month. Tomorrow 3pm, go all in. Absolute Confidence."
    analyze_text(email)



   
