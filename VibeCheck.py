from headline import Headline
import time
import re
import random


def loadWords():
    words = {}
    with open(r"WordData.txt") as file:
        
        for line in file:

            multiplier = 1 if line[5:9] == "weak" else 2

            index = line.find("polarity=") + 9
            polarity = 1 if line[index:index + 8] == "positive" else -1

            index = line.find("word1=") + 6
            words[line[index: line.find(" ", index)]] = multiplier * polarity
    return words

def loadHeadlines(maxLines, words):

    headlines = []
    with open("HeadlineData.txt") as file:

        count = 0
        for line in file:
            count += 1
            if count > maxLines and maxLines > 0:
                break

            index = line.find(":") + 2
            category = line[index: line.find(",")].capitalize()
            
            index = line.find(":", index) + 2
            headline = line[index: line.find("authors:", index) - 2]

            index = line.find("authors:", index) + 9
            authors = line[index: line.find("link:", index) - 2]

            index = line.find("link:", index) + 6
            link = line[index: line.find("short_", index) - 2]
            
            index = line.find("description:", index) + 13
            description = line[index: line.find("date:") - 2]

            index = line.find("date:", index) + 6
            date = line[index: line.find("\n")]
            
            
            headlines.append(Headline(category, headline, authors, link, description, date, words))
    return headlines

            
    

def main():

    print("\nWelcome to Vibe Check\n")

    print("Loading Words.")
    start_time = time.time()
    words = loadWords()
    print(f"{len(words)} words loaded in {time.time() - start_time} seconds\n")

    while True:
        try:
            print("How many headlines would you like to load? Enter -1 to load all 200k.")
            user = int(input())
            if user not in range(-1, 220000):
                print("Invalid number of headlines.")
                continue
            break
        except ValueError as e:
            print("Input must be an integer.")
            continue
    print("Loading Headlines.")
    start_time = time.time()
    headlines = loadHeadlines(user, words)
    print(f"{len(headlines)} headlines loaded in {time.time() - start_time} seconds\n")
    
    menu = [
        "Quit",
        "Display two of the most polar headlines",
        "Display the most positive headlines",
        "Display the most negative headlines",
        "Display information about a date",
        "Display all headlines from a date",
        "Input a string to find it's polarity",
        "Display all the information about a random headline"
    ]
    while True:

        print("\nMain Menu")
        for index, line in enumerate(menu):
            print(f"{index}. {line}")

        while True:
            try:
                print("\nMenu Selection: ", end='')
                user = int(input())
                if user not in range(0, len(menu)):
                    print("Input not in menu options")
                    continue
            except ValueError as e:
                print("Input must be an integer.")
                continue
            else:
                break

        if user == 0:
            print("\nThank you come again.\n")
            break

        if user == 1:
            
            most_pos = headlines[0]
            most_neg = headlines[0]
            for headline in headlines:
                if headline.polarity > most_pos.polarity:
                    most_pos = headline
                elif headline.polarity < most_neg.polarity:
                    most_neg = headline

            print("\nThe most positive headline is:")
            most_pos.print_()
            print("\nThe most negative headline is:")
            most_neg.print_()

        if user == 2:
            
            most_pos = []

            for headline in headlines:
                if len(most_pos) < 3:
                    most_pos.append(headline)
                else:
                    most_pos = sorted(most_pos, key=lambda x: x.polarity)
                    if most_pos[0].polarity < headline.polarity:
                        most_pos[0] = headline
                
            print("\nThe headlines with the lowest polarity are:\n")
            for headline in sorted(most_pos, key=lambda x: x.polarity):
                headline.print_()

        if user == 3:

            most_neg = []

            for headline in headlines:
                if len(most_neg) < 3:
                    most_neg.append(headline)
                else:
                    most_neg = sorted(most_neg, key=lambda x: x.polarity)
                    if most_neg[-1].polarity > headline.polarity:
                        most_neg[-1] = headline
                
            print("\nThe headlines with the lowest polarity are:\n")
            for headline in sorted(most_neg, key=lambda x: x.polarity):
                headline.print_()

        if user == 4:
            
            print("Input a date in format yyyy-mm-dd")
            user_date = input()


            num_headlines = 0
            total_polarity = 0
            most_pos = None
            most_neg = None
            for headline in headlines:
                if headline.date == user_date:
                    num_headlines += 1
                    total_polarity += headline.polarity

                    if most_pos == None:
                        most_pos = headline
                        most_neg = headline

                    if headline.polarity > most_pos.polarity:
                        most_pos = headline
                    elif headline.polarity < most_neg.polarity:
                        most_neg = headline

            if num_headlines:
                print(f"\nOn {user_date} there were {num_headlines} headlines.\nThe total polarity of this date was {total_polarity}.")
                print("\nThe most positive headline from this date was:\n")
                most_pos.print_()
                print("\nThe most negative headline from this date was:\n")
                most_neg.print_()
            else:
                print("There were no headlines on this date")

        if user == 5:
            
            print("Input a date in format yyyy-mm-dd")
            print(f"The date must be from {headlines[-1].date} to {headlines[0].date}")
            user_date = input()

            found = False
            for headline in headlines:
                if headline.date == user_date:
                    found = True
                    headline.print_()
            
            if not found:
                print("No Headlines from this date")

        if user == 6:

            print("\nPlease enter a string: ", end='')
            user_string = input()
            
            polarity = 0

            for word in user_string.split():
                regex = re.compile('[^a-zA-Z]')
                if regex.sub('', word).lower() in words:
                    polarity += words[regex.sub('', word).lower()]


            print(polarity)

        if user == 7:
            rand_num = random.randrange(0, len(headlines))

            print()
            headlines[rand_num].print_()
            print("Description: " + headlines[rand_num].description)
            print("Authors: " + headlines[rand_num].authors)
            print("Date: " + headlines[rand_num].date)
            print("Category: " + headlines[rand_num].category)
            print("Link: " + headlines[rand_num].link)


        



if __name__ == "__main__":
    main()