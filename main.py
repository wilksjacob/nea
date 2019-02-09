# Import the necessary modules
import csv       # For parsing csv
import datetime  # For dealing with timestamps
import random    # For dice-roll
import time      # For waiting during gameplay


class User(object):
    """User Object, used for indexing and accessing  user info."""
    def __init__(self, id: int, lname: str, fname: str, username: str, password: str, birthdate: int):
        self.id = int(id)
        self.lname = lname
        self.fname = fname
        self.username = username
        self.password = password
        self.birthdate = int(birthdate)

    def birth_info(self):
        """Potential feature involving age categories?."""
        day = datetime.datetime.fromtimestamp(self.birthdate).strftime('%d')
        month = datetime.datetime.fromtimestamp(self.birthdate).strftime('%m')
        year = datetime.datetime.fromtimestamp(self.birthdate).strftime('%Y')
        return [day, month, year]

    def info(self):
        """Return user info as array."""
        return [self.id,self.lname, self.fname, self.username, self.password, self.birthdate]

class Result(object):
    """Result Object, for importing and sorting result instances."""
    def __init__(self, user_id: int,score: int, timestamp: int):
        self.user_id = int(user_id)
        self.score = score
        self.timestamp = int(timestamp)


    def info(self):
        """Return result info as array."""
        return [self.user_id, self.score, self.timestamp]

def index_users():
    """Return an array of instances of User class."""
    with open('users.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        users = []
        for row in csv_reader:
            user = User(row[0],row[1],row[2],row[3],row[4],row[5])
            users.append(user)
        return users

def index_results():
    """Return an array of instances of Result class."""
    with open('results.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        results = []
        for row in csv_reader:
            result = Result(row[0],row[1],row[2])
            results.append(result)
        return results

def user_exists(username: str):
    """Lookup username to see if user exists."""
    users = index_users()
    for i in range(len(users)):
        if users[i].info()[3] == username:
            return users[i].info()[0]
    return False

def user_exists_from_id(idno: int):
    """Lookup id to see if user exists."""
    users = index_users()
    for i in range(len(users)):
        if users[i].info()[0] == idno:
            return users[i].info()[3]
    return False

def id_exists(id: int):
    """Check if id exists."""
    users = index_users()
    for i in range(len(users)):
        if users[i].info()[0] == id:
            return True
        else:
            return False

def next_free_id():
    """Find out next free User ID - for future registration feature."""
    users = index_users()
    greatest_id = users[-1].info()[0]
    return greatest_id + 1


def roll(n: int):
    """Generate random number between 1 and n."""
    return random.randint(1,n)

def write_result(user_id, score):
    """Append result data to file as csv row."""
    with open('results.csv', mode='a') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        writer.writerow([user_id, score, int(time.time())])

        return True

def auth():
    """Authenticate users."""
    users = index_users()
    ## Authenticate User 1 ##
    exists = False
    password_correct = False
    username_input = str(input("User 1, please enter your username: "))
    count = 0
    user1_id = 0
    while exists == False:
        if count < 1:
            pass
        else:
            username_input = input("Sorry, that username does not exist. Please try again: ")
        if user_exists(username_input):
            user1_id = user_exists(username_input)
            exists = True
        else:
            count += 1
            pass
    password_input = input("Please enter your password ")
    while password_correct == False:
        if count < 1:
            pass
        else:
            password_input = input("Sorry, your password is incorrect. Please try again: ")
        if index_users()[user1_id - 1].info()[4] == password_input:
            print("Welcome, " + str(users[user_exists(username_input)-1].info()[2]))
            password_correct = True
        else:
            count += 1
            pass

    print("","")
    ## Authenticate User 2 ##
    exists = False
    password_correct = False
    username_input = str(input("User 2, please enter your username: "))
    count = 0
    user2_id = 0
    while exists == False:
        if username_input == users[user1_id - 1].info()[3]:
            username_input =  input("That user is already logged in! Please enter another username: ")
        if count < 1:
            pass
        else:
            username_input = input("Sorry, that username does not exist. Please try again: ")
        if user_exists(username_input):
            user2_id = user_exists(username_input)
            exists = True
        else:
            count += 1
            pass
    password_input = input("Please enter your password ")
    while password_correct == False:
        if count < 1:
            pass
        else:
            password_input = input("Sorry, your password is incorrect. Please try again: ")
        if index_users()[user2_id - 1].info()[4] == password_input:
            print("Welcome, " + str(users[user_exists(username_input)-1].info()[2]))
            password_correct = True
        else:
            count += 1
            pass

    return [user1_id,user2_id]


def gameplay(p1_id, p2_id):
    """Once authenticated, run through actual gameplay. Return winning user's id and score as an array."""
    users = index_users()

    ## Get Users' names ##
    p1_name = users[p1_id - 1].info()[2]
    p2_name = users[p2_id - 1].info()[2]

    p1_nos = []
    p2_nos = []

    p1_score= 0
    p2_score = 0

    ## Pre-generate all the dice rolls ##
    for i in range(5):
        array1 = [roll(6), roll(6), roll(6)]
        p1_nos.append(array1)
        array2 = [roll(6), roll(6), roll(6)]
        p2_nos.append(array2)

    print(p1_nos)
    print(p2_nos)

    for i in range(5):
        print()
        print("- - - - - - - - - - - - - - - - - - - - - - - - - - - -")
        print()
        ## Player 1 ##
        print("**** " + p1_name + " - Turn " + str(i + 1) + " ****")
        print("First dice = " + str(p1_nos[i][0]))
        time.sleep(0.5)
        print("Second dice = " + str(p1_nos[i][1]))

        time.sleep(0.5)

        if ((p1_nos[i][0] + p1_nos[i][1]) % 2) == 0:
            print("An even total :) - 10 points added to " + p1_name + "'s score!")
            p1_score += 10
        else:
            print("An odd total :( - 5 points deducted from " + p1_name + "'s score!")

        time.sleep(0.5)

        if p1_nos[i][0] == p1_nos[i][1]:
            print("A DOUBLE! - " + p1_name +" gets to roll again.")
            print(str(p1_nos[i][2]) + " points added to " + p1_name + "'s score!")
            p1_score += p1_nos[i][2]

        print()

        ## Player 2 ##
        print("**** " + p2_name + " - Turn " + str(i + 1) + " ****")
        print("First dice = " + str(p2_nos[i][0]))
        time.sleep(0.5)
        print("Second dice = " + str(p2_nos[i][1]))

        time.sleep(0.5)

        if ((p2_nos[i][0] + p2_nos[i][1]) % 2) == 0:
            print("An even total :) - 10 points added to " + p2_name + "'s score!")
            p2_score += 10
        else:
            print("An odd total :( - 5 points deducted from " + p2_name + "'s score!")

        time.sleep(0.5)

        if p2_nos[i][0] == p2_nos[i][1]:
            print("A DOUBLE! - " + p2_name +" gets to roll again.")
            print(str(p2_nos[i][2]) + " points added to " + p2_name + "'s score!")
            p2_score += p2_nos[i][2]

        print()

        print("At the end of turn " + str(i) + ":")
        print(p1_name + " = " + str(p1_score))
        print(p2_name + " = " + str(p2_score))
        input("PRESS ENTER TO CONTINUE")

    if p1_score > p2_score:
        print(p1_name + " wins with " + str(p1_score) + " points!")
        return [p1_id, p1_score]
    elif p2_score > p1_score:
        print(p2_name + " wins with " + str(p2_score) + " points!")
        return [p2_id, p2_score]

    print("Its a draw! Both players have " + p1_score + " points.")
    print("Each player will now roll - whoever gets the higher number wins...")

    while p1_score == p2_score:
        p1 = roll(6)
        p2 = roll(6)

        print(p1_name + " rolled a " + p1 + ".")
        print(p2_name + " rolled a " + p2 + ".")

        p1_score += p1
        p2_score += p2

    if p1_score > p2_score:
        print(p1_name + " wins with " + str(p1_score) + " points!")
        return [p1_id, p1_score]
    elif p2_score > p1_score:
        print(p2_name + " wins with " + str(p2_score) + " points!")
        return [p2_id, p2_score]


def board():
    """Fetch and display 5 highest scores and corresponding usernames."""
    results = index_results()
    simple_list = []
    for result in results:
        simple_list.append([result.info()[0], result.info()[1]])
    simple_list.sort(key=lambda x: int(x[1]), reverse=True)

    print("---------[ LEADERBOARD ]---------")
    if len(simple_list) < 5:
        for i in range(len(simple_list)):
            print(str(i + 1) + ") " + user_exists_from_id(int(simple_list[i][0])) + "  -  " + simple_list[i][1])




def main():
    p1_id = False
    p2_id = False

    print("Welcome!")

    vals = auth()

    p1_id = vals[0]
    p2_id = vals[1]

    result = gameplay(p1_id, p2_id)
    write_result(result[0], result[1])
    print()
    print()
    board()

main()
