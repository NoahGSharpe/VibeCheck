import re

class Headline():
    def __init__(self, category, headline, authors, link, description, date, words):

        self.category = category
        self.headline = headline
        self.authors = authors
        self.link = link
        self.description = description
        self.date = date
        self.polarity = 0
        for word in self.headline.split():
            regex = re.compile('[^a-zA-Z]')
            if regex.sub('', word).lower() in words:
                self.polarity += words[regex.sub('', word).lower()]

    def print_(self):
        print(f"{self.headline}\nPolarity: {self.polarity}")