from wordParser import WordParser

def main():
    response = ""
    email = "Dear Client, I think that the Google stock is really awful, and \
    will fall soon. I personally would never invest in it since it's SHIT. I \
    strongly dislike google stock so you should never ever invest in it. Sincerely, Person"
    parse = WordParser(email, response)
    parse.search_profanity()
    print(parse.get_response())


if __name__ == '__main__':
    main()
