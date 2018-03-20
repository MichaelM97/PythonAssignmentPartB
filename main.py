# Name: Assignment Project Part B
# Author: Michael McCormick (15012271)

import csv
import os
import sys
import string


def main():
    fileInfo = FileInformation() # Create object to access class

    fileInfo.get_file_names() # Get file names from user

    while True:  # Loop allows for entry of additional tournaments

        score_input_menu(fileInfo, 1)  # User chooses if scores entered manually or via file

        # Store information from selected files
        fileInfo.store_ranking_info()
        fileInfo.store_prize_info()
        fileInfo.store_player_names()

        # Check for tempfiles containing pre-existing data
        global tempFiles
        if tempMaleFile:
            tempFiles = True
        else:
            tempFiles = False

        # Process round 1 scores
        count = 1
        if scoreChoice == '1':
            fileInfo.process_file_scores()
        else:
            fileInfo.get_score_input(count, tempFiles)
            fileInfo.process_user_scores()

        fileInfo.display_round_winners(count)
        count += 1

        # Get file selection from user, and loop through to calculate top 16 players scores
        while count < 6 and maleRankingPosition > 1 and femaleRankingPosition > 1:
            score_input_menu(fileInfo, count)  # User chooses if scores entered manually or via file

            # Get score input from FILE
            if scoreChoice == '1':
                count += 1
                fileInfo.process_file_scores()
                fileInfo.display_round_winners(count)

            # Get score input from USER
            elif scoreChoice == '2':
                count += 1
                fileInfo.reset_player_names()
                fileInfo.get_score_input(count, tempFiles)
                fileInfo.process_user_scores()

        # Calculate players winnings and display results
        fileInfo.process_winnings()
        if len(prevMaleRankings) > 0 or len(prevFemaleRankings) > 0:  # Adds previous tournament results (if they exist)
            fileInfo.add_previous_results()
        fileInfo.display_results()

        # Store results in a file (if users chooses to)
        while True:
            print("Would you like to store these results in a file? [Y/N]: ")
            userInput = get_valid_input().upper()
            if userInput == 'Y':
                fileInfo.store_result_file()
                break
            elif userInput == 'N':
                print("Scores will not be saved.")
                break
            else:
                print("Invalid Input!!!\n")

        # Deletes temp files
        if tempMaleFile:
            os.remove(directoryPath + "\\" + "TEMPMALE.csv")
        if tempFemaleFile:
            os.remove(directoryPath + "\\" + "TEMPFEMALE.csv")

        # Allows user to add more scores for more tournaments
        while True:
            print("Would you like add results for another tournament? [Y/N]: ")
            userInput = get_valid_input().upper()
            if userInput == 'Y':
                fileInfo.store_previous_results()
                # Clear arrays for further use
                global malePlayerRankings
                malePlayerRankings = []
                global femalePlayerRankings
                femalePlayerRankings = []
                global prizeMoneyInfo
                prizeMoneyInfo = []
                extraTournament = True
                break
            elif userInput == 'N':
                print("No further tournament scores will be added.")
                extraTournament = False
                break
            else:
                print("Invalid Input!!!\n")

        if not extraTournament:
            print("Thank you for using the system.")
            break


"""Allows user to choose to enter scores manually or from files"""
def score_input_menu(fileInfo, roundNum):
    clear_screen()
    global scoreChoice

    #  Get valid user input
    while True:
        print("Please select an option:\n\n1 - Read players score from file\n2 - Enter players score manually\n")
        scoreChoice = get_valid_input()
        if scoreChoice == '1':
            fileInfo.get_score_files(roundNum)
            fileInfo.set_difficulty(maleScoresFile)  # Attempt to pull difficulty from file name
            break
        elif scoreChoice == '2':
            if not tempMaleFile and roundNum == 1:
                fileInfo.set_difficulty("")  # Set difficulty using user input
            break
        else:
            print("Invalid Input!\n\n")


"""Informs user on how to use system"""
def initial_menu():
    clear_screen()

    #  Get valid user input
    while True:
        print(
            "\nWelcome to the tennis score calculation system!\n\nInstructions:\n"
            "Please ensure that you have files containing the: Ranking Points, Prize Money, Male Player Names,"
            "\nand Female Player Names placed with in the same project folder as this program;"
            " along with any files containing player scores that you may wish to process.\n"
            "If the program previously closed whilst data was being processed, this"
            " information will be automatically re-added for you.\n")
        print("Please select an option:\n1 - Run Program\n2 - Close Program")
        userInput = get_valid_input()
        if userInput == '1':
            break
        elif userInput == '2':
            print("Thank you for using the system.")
            sys.exit()
        else:
            print("Invalid Input!!\n")


"""Validates user inputs (Only used for single character or integer entries)"""
def get_valid_input():
    while True:
        try:  # Validates against blank entries
            userInput = input("::")
        except SyntaxError:
            userInput = None
        if len(userInput) > 1:
            try:  # Validates against number and character mixed entries
                int(userInput)
            except ValueError:
                userInput = None
        if userInput:
            return userInput
            break
        else:
            print("Invalid input! Please enter again.")


"""Clears display screen (checks if Windows or Linux as command differs)"""
def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


"""Class holds all information and functions related to storing and manipulating file data"""
class FileInformation:

    # Degree's of difficulty
    global TAC1_DIFFICULTY
    TAC1_DIFFICULTY = 2.7
    global TAE21_DIFFICULTY
    TAE21_DIFFICULTY = 2.3
    global TAW11_DIFFICULTY
    TAW11_DIFFICULTY = 3.1
    global TBS2_DIFFICULTY
    TBS2_DIFFICULTY = 3.25

    # Allow global access to root directoryPath file list, removes irrelevant files (if they exist)
    global fileList
    fileList = os.listdir()
    if '.idea' in fileList:
        fileList.remove('.idea')
    if 'main.py' in fileList:
        fileList.remove('main.py')
    if '.git' in fileList:
        fileList.remove('.git')
    if 'README.md' in fileList:
        fileList.remove('README.md')

    # Retrieves directory path
    global directoryPath
    directoryPath = str(os.path.dirname(os.path.realpath(__file__)))

    # Check for presence of temp files, if not create file with headers
    global tempMaleFile
    tempMaleFile = False
    global tempFemaleFile
    tempFemaleFile = False
    if 'TEMPMALE.csv' in fileList:
        tempMaleFile = True
        fileList.remove('TEMPMALE.csv')
    else:
        csvFile = open((directoryPath + "\\" + "TEMPMALE.csv"), 'a', newline="\n")
        writer = csv.writer(csvFile, dialect='excel')
        writer.writerow(["Round Number"] + ["Player A"] + ["Score"] + ["Player B"] + ["Score"] + ["Tournament Name"])
        csvFile.close()
    if 'TEMPFEMALE.csv' in fileList:
        tempFemaleFile = True
        fileList.remove('TEMPFEMALE.csv')
    else:
        csvFile = open((directoryPath + "\\" + "TEMPFEMALE.csv"), 'a', newline="\n")
        writer = csv.writer(csvFile, dialect='excel')
        writer.writerow(["Round Number"] + ["Player A"] + ["Score"] + ["Player B"] + ["Score"] + ["Tournament Name"])
        csvFile.close()

    # Arrays used to store file information
    global maleScoresInfo
    maleScoresInfo = []
    global femaleScoresInfo
    femaleScoresInfo = []
    global rankingPointsInfo
    rankingPointsInfo = []
    global malePlayerNames
    malePlayerNames = []
    global femalePlayerNames
    femalePlayerNames = []
    global prizeMoneyInfo
    prizeMoneyInfo = []
    global malePlayerRankings
    malePlayerRankings = []
    global femalePlayerRankings
    femalePlayerRankings = []
    global prevMaleRankings
    prevMaleRankings = []
    global prevFemaleRankings
    prevFemaleRankings = []
    global malePlayerWinners
    malePlayerWinners = []
    global femalePlayerWinners
    femalePlayerWinners = []
    global maleUserScores
    maleUserScores = []
    global femaleUserScores
    femaleUserScores = []

    """Get names of files containing player scores"""
    def get_score_files(self, roundNum):
        clear_screen()
        # Get MALE SCORES File Name
        while True:
            for f, fileName in enumerate(fileList):
                print(f, "-", fileName)
            print("\nPlease select the file containing the MALE PLAYERS scores for round %d: " % roundNum)
            userInput = get_valid_input()
            if (int(userInput) < 0) or (int(userInput) > len(fileList)):
                print("Invalid Input!!!\n")
            else:
                break
        global maleScoresFile
        maleScoresFile = fileList[int(userInput)]  # Stores male file name globally
        fileList.remove(maleScoresFile)  # Removes file from list so it cannot be selected again

        clear_screen()
        # Get FEMALE SCORES File Name
        while True:
            for f, fileName in enumerate(fileList):
                print(f, "-", fileName)
            print("\nPlease select the file containing the FEMALE PLAYERS scores for round %d: " % roundNum)
            userInput = get_valid_input()
            if (int(userInput) < 0) or (int(userInput) > len(fileList)):
                print("Invalid Input!!!\n")
            else:
                break
        global femaleScoresFile
        femaleScoresFile = fileList[int(userInput)]  # Stores female file name globally
        fileList.remove(femaleScoresFile)  # Removes file from list so it cannot be selected again

    """Allows user to input scores"""
    def get_score_input(self, roundNum, tempFilesExist):
        global maleUserScores
        maleUserScores = []
        global femaleUserScores
        femaleUserScores = []

        # Process temp file information (if it exists)
        if tempFilesExist:
            FileInformation.process_temp_user_input_files(self, roundNum)

        # Get MALE PLAYER scores as input
        while len(malePlayerNames) > 1:  # While there are still male players left without a score
            clear_screen()
            print("Entering MALE PLAYER scores for round %d: \n" % roundNum)
            row = []
            # User selects first player in match
            for i, name in enumerate(malePlayerNames):  # List all available players
                print(i + 1, "-", name)
            while True:
                print("\nPlease select the first player: ")
                userInput = get_valid_input()
                if int(userInput) < 1 or int(userInput) > len(malePlayerNames):
                    print("Invalid Input!\n")
                else:
                    break
            row.append(malePlayerNames[int(userInput) - 1])
            malePlayerNames.remove(malePlayerNames[int(userInput) - 1])
            # User enters the first players score
            while True:
                print("\nPlease enter the first players score[0-3]: ")
                firstScore = get_valid_input()
                if int(firstScore) < 0 or int(firstScore) > 3:
                    print("Invalid Input!\n")
                else:
                    break
            row.append(firstScore)

            # User selects second player in match
            for i, name in enumerate(malePlayerNames):  # List all available players
                print(i + 1, "-", name)
            while True:
                print("\nPlease select the second player: ")
                userInput = get_valid_input()
                if int(userInput) < 1 or int(userInput) > len(malePlayerNames):
                    print("Invalid Input!\n")
                else:
                    break
            row.append(malePlayerNames[int(userInput) - 1])
            malePlayerNames.remove(malePlayerNames[int(userInput) - 1])
            # User enters the second players score
            while True:
                print("\nPlease enter the second players score[0-3]: ")
                secondScore = get_valid_input()
                if int(secondScore) < 0 or int(secondScore) > 3:
                    print("Invalid Input!\n")
                elif (int(firstScore) + int(secondScore)) > 5:
                    print("Invalid Input! There can only be a total of 5 games per pair.\n")
                elif int(firstScore) != 3 and int(secondScore) != 3:
                    print("Invalid Input! One player must win 3 games, or there is no winner.\n")
                else:
                    break
            row.append(secondScore)
            maleUserScores.append(row)  # Store data entered into global array for later processing

            # Adds most recent male match entry to temp file
            maleWrite = [roundNum] + row + [tournamentName]
            FileInformation.update_temp_user_input_files(self, maleWrite, 0)

        # Get FEMALE PLAYER scores as input
        while len(femalePlayerNames) > 1:  # While there are still female players left without a score
            clear_screen()
            print("Entering FEMALE PLAYER scores for round %d: \n" % roundNum)
            row = []
            # User selects first player in match
            for i, name in enumerate(femalePlayerNames):  # List all available players
                print(i + 1, "-", name)
            while True:
                print("\nPlease select the first player: ")
                userInput = get_valid_input()
                if int(userInput) < 1 or int(userInput) > len(femalePlayerNames):
                    print("Invalid Input!\n")
                else:
                    break
            row.append(femalePlayerNames[int(userInput) - 1])
            femalePlayerNames.remove(femalePlayerNames[int(userInput) - 1])
            # User enters the first players score
            while True:
                print("\nPlease enter the first players score[0-2]: ")
                firstScore = get_valid_input()
                if int(firstScore) < 0 or int(firstScore) > 2:
                    print("Invalid Input!\n")
                else:
                    break
            row.append(firstScore)
            # User selects second player in match
            for i, name in enumerate(femalePlayerNames):  # List all available players
                print(i + 1, "-", name)
            while True:
                print("\nPlease select the second player: ")
                userInput = get_valid_input()
                if int(userInput) < 1 or int(userInput) > len(femalePlayerNames):
                    print("Invalid Input!\n")
                else:
                    break
            row.append(femalePlayerNames[int(userInput) - 1])
            femalePlayerNames.remove(femalePlayerNames[int(userInput) - 1])
            # User enters the second players score
            while True:
                print("\nPlease enter the second players score[0-2]: ")
                secondScore = get_valid_input()
                if int(secondScore) < 0 or int(secondScore) > 2:
                    print("Invalid Input!\n")
                elif (int(firstScore) + int(secondScore)) > 3:
                    print("Invalid Input! There can only be a total of 3 games per pair.\n")
                elif int(firstScore) != 2 and int(secondScore) != 2:
                    print("Invalid Input! One player must win 2 games, or there is no winner.\n")
                else:
                    break
            row.append(secondScore)
            femaleUserScores.append(row)  # Store data entered into global array for later processing

            # Adds most recent male match entry to temp file
            femaleWrite = [roundNum] + row + [tournamentName]
            FileInformation.update_temp_user_input_files(self, 0, femaleWrite)

        return roundNum  # Returns in-case it was updated by files

    """Sets the tournament name and difficulty based on file name, or user input"""
    def set_difficulty(self, tournament):
        global tournamentName
        global tournamentDifficulty

        if 'TAC1' in tournament:
            tournamentName = 'TAC1'
            tournamentDifficulty = TAC1_DIFFICULTY
        elif 'TAE21' in tournament:
            tournamentName = 'TAE21'
            tournamentDifficulty = TAE21_DIFFICULTY
        elif 'TAW11' in tournament:
            tournamentName = 'TAW11'
            tournamentDifficulty = TAW11_DIFFICULTY
        elif 'TBS2' in tournament:
            tournamentName = 'TBS2'
            tournamentDifficulty = TBS2_DIFFICULTY
        else:
            print("Could not find difficulty, please enter Tournament Name -\nTAC1\nTAE21\nTAW11\nTBS2")
            while True:  # Avoids invalid user inputs such as 'TAC19'
                try:  # Validates against blank entries
                    userInput = input("::").upper()
                except SyntaxError:
                    userInput = 'q'  # Invalid placeholder
                if 'TAC1' or 'TBS2' in userInput and len(userInput) == 4:
                    break
                elif 'TAE21' or 'TAW11' in userInput and len(userInput) == 5:
                    break
                else:
                    print("Invalid input! Please enter again.")
            FileInformation.set_difficulty(self, userInput)

    """Allows user to select files containing required information"""
    def get_file_names(self):
        clear_screen()
        # Get RANKING POINTS File Name
        while True:
            for f, fileName in enumerate(fileList):
                print(f, "-", fileName)
            print("\nPlease select the file containing RANKING POINTS information: ")
            userInput = get_valid_input()
            if (int(userInput) < 0) or (int(userInput) > len(fileList)):
                print("Invalid Input!!!\n")
            else:
                break
        global rankingPointsFile
        rankingPointsFile = fileList[int(userInput)]  # Stores ranking points file name globally
        fileList.remove(rankingPointsFile)  # Removes file from list so it cannot be selected again

        clear_screen()
        # Get PRIZE MONEY File Name
        while True:
            for f, fileName in enumerate(fileList):
                print(f, "-", fileName)
            print("\nPlease select the file containing PRIZE MONEY information: ")
            userInput = get_valid_input()
            if (int(userInput) < 0) or (int(userInput) > len(fileList)):
                print("Invalid Input!!!\n")
            else:
                break
        global prizeMoneyFile
        prizeMoneyFile = fileList[int(userInput)]  # Stores prize money file name globally
        fileList.remove(prizeMoneyFile)  # Removes file from list so it cannot be selected again

        clear_screen()
        # Get MALE PLAYERS File Name
        while True:
            for f, fileName in enumerate(fileList):
                print(f, "-", fileName)
            print("\nPlease select the file containing MALE PLAYERS information: ")
            userInput = get_valid_input()
            if (int(userInput) < 0) or (int(userInput) > len(fileList)):
                print("Invalid Input!!!\n")
            else:
                break
        global malePlayersFile
        malePlayersFile = fileList[int(userInput)]  # Stores male players file name globally
        fileList.remove(malePlayersFile)  # Removes file from list so it cannot be selected again

        clear_screen()
        # Get FEMALE PLAYERS File Name
        while True:
            for f, fileName in enumerate(fileList):
                print(f, "-", fileName)
            print("\nPlease select the file containing FEMALE PLAYERS information: ")
            userInput = get_valid_input()
            if (int(userInput) < 0) or (int(userInput) > len(fileList)):
                print("Invalid Input!!!\n")
            else:
                break
        global femalePlayersFile
        femalePlayersFile = fileList[int(userInput)]  # Stores female players file name globally
        fileList.remove(femalePlayersFile)  # Removes file from list so it cannot be selected again

    """Store player names provided from file"""
    def store_player_names(self):
        # Store MALE PLAYERS FILE information in array
        with open(malePlayersFile) as csvFile:
            readCsv = csv.reader(csvFile, delimiter=',')
            for i, row in enumerate(readCsv):
                malePlayerNames.append(row[0])

        # Store FEMALE PLAYERS FILE information in array
        with open(femalePlayersFile) as csvFile:
            readCsv = csv.reader(csvFile, delimiter=',')
            for i, row in enumerate(readCsv):
                femalePlayerNames.append(row[0])

    """Adds back all winners to the player name arrays, allowing further processing of winners"""
    def reset_player_names(self):
        # Clear lists
        global malePlayerNames
        malePlayerNames = []
        global femalePlayerNames
        femalePlayerNames = []
        maleLosers = []
        maleNames = []
        femaleLosers = []
        femaleNames = []

        # Reset MALE PLAYER scores
        # Get MALE losers
        for losers in malePlayerRankings:
            loser = losers.split('-')
            maleLosers.append(loser[0])

        # Get MALE names and create winner list
        with open(malePlayersFile) as csvFile:
            readCsv = csv.reader(csvFile, delimiter=',')
            for row in readCsv:
                maleNames.append(row[0])
        maleWinners = [n for n in maleNames if n not in maleLosers]

        # Add winners back to list
        for row in maleWinners:
            malePlayerNames.append(row)

        # Reset FEMALE PLAYER scores
        # Get FEMALE losers
        for losers in femalePlayerRankings:
            loser = losers.split('-')
            femaleLosers.append(loser[0])

        # Get FEMALE names and create winner list
        with open(femalePlayersFile) as csvFile:
            readCsv = csv.reader(csvFile, delimiter=',')
            for row in readCsv:
                femaleNames.append(row[0])
        femaleWinners = [n for n in femaleNames if n not in femaleLosers]

        # Add winners back to list
        for row in femaleWinners:
            femalePlayerNames.append(row)

    """Stores required ranking points information from file provided by user"""
    def store_ranking_info(self):
        # Store RANKING POINTS FILE information in array
        with open(rankingPointsFile) as csvFile:
            readCsv = csv.reader(csvFile, delimiter=',')
            for i, row in enumerate(readCsv):
                rankingPointsInfo.append(row[0])
            # Set male and female ranking position counters
            global maleRankingPosition
            maleRankingPosition = i
            global femaleRankingPosition
            femaleRankingPosition = i

    """Stores required prize money information from file provided by user"""
    def store_prize_info(self):
        # Store PRIZE MONEY FILE information in array
        with open(prizeMoneyFile) as csvFile:
            readCsv = csv.reader(csvFile, delimiter=',')
            found = False
            previous = 0
            for row in readCsv:
                if tournamentName in row[0]:
                    found = True
                if found is True:
                    if int(row[1]) < int(previous):  # Prevents storing other tournament values
                        break
                    else:
                        prizeMoneyInfo.append(row[2])
                        previous = row[1]

    """Stores players in order of their scores given in a file"""
    def process_file_scores(self):
        global maleRankingPosition
        global femaleRankingPosition

        # Process MALE PLAYER scores
        with open(maleScoresFile) as csvFile:
            readCsv = csv.reader(csvFile, delimiter=',')
            # Calculate ranking points and assign them to losing player
            if len(list(readCsv)) > 9:
                rankingPoints = 0  # No points for round 1 winners
                maleRankingPosition += maleRankingPosition  # Size doubled to allow for round 1
            else:
                rankingPoints = int(rankingPointsInfo[maleRankingPosition]) * tournamentDifficulty
            csvFile.seek(0)  # Reset file iterator pos
            next(readCsv)  # Skip headers in file
            for row in readCsv:
                gameTotal = int(row[1]) + int(row[3])  # Check if too many games played
                if row[1] > row[3] and int(row[1]) == 3 and 6 > gameTotal >= 3:
                    malePlayerRankings.append(row[2] + '-' + str(rankingPoints))
                elif row[1] < row[3] and int(row[3]) == 3 and 6 > gameTotal >= 3:
                    malePlayerRankings.append(row[0] + '-' + str(rankingPoints))
                else:  # If no winner is found, display error and get appended scores
                    while True:
                        print("\nERROR IN SCORE ENTRY!!!\n"
                              "Please append the below score:\n"
                              + row[0] + "-" + row[1] + " v " + row[2] + "-" + row[3])
                        # Get a new valid score
                        print("\nEnter new score for " + row[0] + ":")
                        while True:
                            firstScore = get_valid_input()
                            if (int(firstScore) > 3) or (int(firstScore) < 0):
                                print("Score invalid.")
                            else:
                                break
                        print("\n\nEnter new score for " + row[2])
                        while True:
                            secondScore = get_valid_input()
                            if (int(secondScore) > 3) or (int(secondScore) < 0):
                                print("Score invalid.")
                            else:
                                break
                        # Check input
                        if firstScore > secondScore:
                            malePlayerRankings.append(row[2] + '-' + str(rankingPoints))
                            break
                        elif firstScore < secondScore:
                            malePlayerRankings.append(row[0] + '-' + str(rankingPoints))
                            break
                maleRankingPosition += -1
                # If this is the last player, assign them the highest ranking points
                if maleRankingPosition == 1:
                    rankingPoints = int(rankingPointsInfo[maleRankingPosition]) * tournamentDifficulty
                    if row[1] > row[3]:
                        malePlayerRankings.append(row[0] + '-' + str(rankingPoints))
                    elif row[1] < row[3]:
                        malePlayerRankings.append(row[2] + '-' + str(rankingPoints))

        # Process FEMALE PLAYER scores
        with open(femaleScoresFile) as csvFile:
            readCsv = csv.reader(csvFile, delimiter=',')
            # Calculate ranking points and assign them to losing player
            if len(list(readCsv)) > 9:
                rankingPoints = 0  # No points for round 1 winners
                femaleRankingPosition += femaleRankingPosition  # Size doubled to allow for round 1
            else:
                rankingPoints = int(rankingPointsInfo[femaleRankingPosition]) * tournamentDifficulty
            csvFile.seek(0)  # Reset file iterator pos
            next(readCsv)  # Skip headers in file
            for row in readCsv:
                gameTotal = int(row[1]) + int(row[3])  # Check if too many games played
                if row[1] > row[3] and int(row[1]) == 2 and 4 > gameTotal >= 2:
                    femalePlayerRankings.append(row[2] + '-' + str(rankingPoints))
                elif row[1] < row[3] and int(row[3]) == 2 and 4 > gameTotal >= 2:
                    femalePlayerRankings.append(row[0] + '-' + str(rankingPoints))
                else:  # If no winner is found, display error and get appended scores
                    while True:
                        print("\nERROR IN SCORE ENTRY!!!\n"
                              "Please append the below score:\n"
                              + row[0] + "-" + row[1] + " v " + row[2] + "-" + row[3])
                        # Get a new valid score
                        print("\nEnter new score for " + row[0] + ":")
                        while True:
                            firstScore = get_valid_input()
                            if (int(firstScore) > 2) or (int(firstScore) < 0):
                                print("Score invalid.")
                            else:
                                break
                        print("\n\nEnter new score for " + row[2])
                        while True:
                            secondScore = get_valid_input()
                            if (int(secondScore) > 2) or (int(secondScore) < 0):
                                print("Score invalid.")
                            else:
                                break
                        # Check input
                        if firstScore > secondScore:
                            femalePlayerRankings.append(row[2] + '-' + str(rankingPoints))
                            break
                        elif firstScore < secondScore:
                            femalePlayerRankings.append(row[0] + '-' + str(rankingPoints))
                            break
                femaleRankingPosition += -1
                # If this is the last player, assign them the highest ranking points
                if femaleRankingPosition == 1:
                    rankingPoints = int(rankingPointsInfo[femaleRankingPosition]) * tournamentDifficulty
                    if row[1] > row[3]:
                        femalePlayerRankings.append(row[0] + '-' + str(rankingPoints))
                    elif row[1] < row[3]:
                        femalePlayerRankings.append(row[2] + '-' + str(rankingPoints))

    """Stores players in order of their scores given by the user"""
    def process_user_scores(self):
        global maleRankingPosition
        global femaleRankingPosition

        # Process MALE PLAYER scores
        # Calculate ranking points and assign them to losing player
        rankingPoints = int(rankingPointsInfo[maleRankingPosition]) * tournamentDifficulty
        for row in maleUserScores:
            if row[1] > row[3]:
                malePlayerRankings.append(row[2] + '-' + str(rankingPoints))
            elif row[1] < row[3]:
                malePlayerRankings.append(row[0] + '-' + str(rankingPoints))
            else:  # If no winner is found, display error and get appended scores
                    while True:
                        print("\nERROR IN SCORE ENTRY!!!\n"
                              "Please append the below score:\n"
                              + row[0] + "-" + row[1] + " v " + row[2] + "-" + row[3])
                        # Get a new valid score
                        print("\n\nEnter new score for " + row[0])
                        while True:
                            firstScore = get_valid_input()
                            if (int(firstScore) > 3) or (int(firstScore) < 0):
                                print("Score invalid.")
                            else:
                                break
                        print("\n\nEnter new score for " + row[2])
                        while True:
                            secondScore = get_valid_input()
                            if (int(secondScore) > 3) or (int(secondScore) < 0):
                                print("Score invalid.")
                            else:
                                break
                        # Check input
                        if firstScore > secondScore:
                            malePlayerRankings.append(row[2] + '-' + str(rankingPoints))
                            break
                        elif firstScore < secondScore:
                            malePlayerRankings.append(row[0] + '-' + str(rankingPoints))
                            break
            maleRankingPosition += -1
            # If this is the last player, assign them the highest ranking points
            if maleRankingPosition == 1:
                rankingPoints = int(rankingPointsInfo[maleRankingPosition]) * tournamentDifficulty
                if row[1] > row[3]:
                    malePlayerRankings.append(row[0] + '-' + str(rankingPoints))
                elif row[1] < row[3]:
                    malePlayerRankings.append(row[2] + '-' + str(rankingPoints))

        # Process FEMALE PLAYER scores
        # Calculate ranking points and assign them to losing player
        rankingPoints = int(rankingPointsInfo[femaleRankingPosition]) * tournamentDifficulty
        for row in femaleUserScores:
            if row[1] > row[3]:
                femalePlayerRankings.append(row[2] + '-' + str(rankingPoints))
            elif row[1] < row[3]:
                femalePlayerRankings.append(row[0] + '-' + str(rankingPoints))
            else:  # If no winner is found, display error and get appended scores
                    while True:
                        print("\nERROR IN SCORE ENTRY!!!\n"
                              "Please append the below score:\n"
                              + row[0] + "-" + row[1] + " v " + row[2] + "-" + row[3])
                        # Get a new valid score
                        print("\n\nEnter new score for " + row[0])
                        while True:
                            firstScore = get_valid_input()
                            if (int(firstScore) > 2) or (int(firstScore) < 0):
                                print("Score invalid.")
                            else:
                                break
                        print("\n\nEnter new score for " + row[2])
                        while True:
                            secondScore = get_valid_input()
                            if (int(secondScore) > 2) or (int(secondScore) < 0):
                                print("Score invalid.")
                            else:
                                break
                        # Check input
                        if firstScore > secondScore:
                            femalePlayerRankings.append(row[2] + '-' + str(rankingPoints))
                            break
                        elif firstScore < secondScore:
                            femalePlayerRankings.append(row[0] + '-' + str(rankingPoints))
                            break
            femaleRankingPosition += -1
            # If this is the last player, assign them the highest ranking points
            if femaleRankingPosition == 1:
                rankingPoints = int(rankingPointsInfo[femaleRankingPosition]) * tournamentDifficulty
                if row[1] > row[3]:
                    femalePlayerRankings.append(row[0] + '-' + str(rankingPoints))
                elif row[1] < row[3]:
                    femalePlayerRankings.append(row[2] + '-' + str(rankingPoints))

    """Assign prize money to top players"""
    def process_winnings(selfs):
        # Assign MALE PLAYERS winnings
        count = len(malePlayerRankings) - 1
        for prize in prizeMoneyInfo:
            prize = float(prize.replace(',', ''))
            malePlayerRankings[count] += ("-" + str(prize))
            count += -1

        # Assign FEMALE PLAYERS winnings
        count = len(femalePlayerRankings) - 1
        for prize in prizeMoneyInfo:
            prize = float(prize.replace(',', ''))
            femalePlayerRankings[count] += ("-" + str(prize))
            count += -1

    """Processes information from previously interrupted user inputted scores"""
    def process_temp_user_input_files(self, roundNum):
        global maleUserScores
        global femaleUserScores

        with open(directoryPath + "\\" + "TEMPMALE.csv") as csvFile:
            readCsv = csv.reader(csvFile, delimiter=',')
            next(readCsv)  # Skip headers in file
            # Adds matches from current round and removes them from selection
            for row in readCsv:
                if int(row[0]) == roundNum:
                    match = [row[1]] + [row[2]] + [row[3]] + [row[4]]
                    maleUserScores.append(match)
                    if row[1] in malePlayerNames:
                        malePlayerNames.remove(row[1])
                    if row[3] in malePlayerNames:
                        malePlayerNames.remove(row[3])
        # Set tournament name and difficulty
        if row[5]:
            tournament = row[5]
        FileInformation.set_difficulty(self, tournament)

        # Process FEMALE PLAYER temp file
        if tempFemaleFile:
            with open(directoryPath + "\\" + "TEMPFEMALE.csv") as csvFile:
                readCsv = csv.reader(csvFile, delimiter=',')
                next(readCsv)  # Skip headers in file
                # Adds matches from current round and removes them from selection
                for row in readCsv:
                    if int(row[0]) == roundNum:
                        match = [row[1]] + [row[2]] + [row[3]] + [row[4]]
                        femaleUserScores.append(match)
                        if row[1] in femalePlayerNames:
                            femalePlayerNames.remove(row[1])
                        if row[3] in femalePlayerNames:
                            femalePlayerNames.remove(row[3])

    """Adds data to the temp user input files"""
    def update_temp_user_input_files(self, maleWrite, femaleWrite):
        # Adds to MALE temp file
        if maleWrite != 0:
            csvFile = open((directoryPath + "\\" + "TEMPMALE.csv"), 'a', newline="\n")
            writer = csv.writer(csvFile, dialect='excel')
            writer.writerow(maleWrite)
            csvFile.close()
        # Adds to FEMALE temp file
        if femaleWrite != 0:
            csvFile = open((directoryPath + "\\" + "TEMPFEMALE.csv"), 'a', newline="\n")
            writer = csv.writer(csvFile, dialect='excel')
            writer.writerow(femaleWrite)
            csvFile.close()

    """Stores results from previously calculated tournaments"""
    def store_previous_results(self):
        global prevMaleRankings
        global prevFemaleRankings

        # Save MALE PLAYER data from previous calculation
        for prevPlayer in prevMaleRankings:  # Avoids double entry of players
            if prevPlayer[0] in malePlayerRankings:
                prevMaleRankings.remove(prevPlayer)
        prevMaleRankings.extend(malePlayerRankings)

        # Save FEMALE PLAYER data from previous calculation
        for prevPlayer in prevFemaleRankings:  # Avoids double entry of players
            if prevPlayer[0] in femalePlayerRankings:
                prevFemaleRankings.remove(prevPlayer)
        prevFemaleRankings.extend(femalePlayerRankings)

    """Adds the prize money and rankings points to players (if they were previously awarded any)"""
    def add_previous_results(self):
        # Add previous MALE PLAYER data
        for i, x in enumerate(malePlayerRankings):
            player = x.split('-')  # Splits current player information
            for y in prevMaleRankings:
                prevPlayer = y.split('-')  # Splits previous player information
                # If player names match then add previous data
                if player[0] in prevPlayer[0]:
                    # Adds previous RANKING POINTS
                    if len(prevPlayer) > 1 and len(player) > 1:  # Adds previous points to current amount
                        player[1] = (float(player[1]) + float(prevPlayer[1]))
                    elif len(prevPlayer) > 1 >= len(player):  # Adds previous points to empty amount
                        malePlayerRankings[i] += ("-" + str(prevPlayer[1]))
                    # Adds previous PRIZE MONEY
                    if len(prevPlayer) > 3 and len(player) > 2:  # Adds previous money to current amount
                        total = (float(player[2]) + float(prevPlayer[2]))
                        # Stores updated total in array
                        malePlayerRankings[i] = (player[0] + '-' + str(player[1]) + '-' + str(total))
                    elif len(prevPlayer) > 3 >= len(player):  # Adds previous money to empty amount
                        malePlayerRankings[i] += ("-" + str(prevPlayer[2]))
                    break  # Ends loop once player is found

        # Add previous FEMALE PLAYER data
        for i, x in enumerate(femalePlayerRankings):
            player = x.split('-')  # Splits current player information
            for y in prevFemaleRankings:
                prevPlayer = y.split('-')  # Splits previous player information
                # If player names match then add previous data
                if player[0] in prevPlayer[0]:
                    # Adds previous RANKING POINTS
                    if len(prevPlayer) > 1 and len(player) > 1:  # Adds previous points to current amount
                        player[1] = (float(player[1]) + float(prevPlayer[1]))
                    elif len(prevPlayer) > 1 >= len(player):  # Adds previous points to empty amount
                        femalePlayerRankings[i] += ("-" + str(prevPlayer[1]))
                    # Adds previous PRIZE MONEY
                    if len(prevPlayer) > 3 and len(player) > 2:  # Adds previous money to current amount
                        # Removes commas for addition
                        playerMoney = player[2].replace(',', '')
                        prevPlayerMoney = prevPlayer[2].replace(',', '')
                        total = (int(playerMoney) + int(prevPlayerMoney))
                        total = format(total, ",d")  # Adds commas back
                        # Stores updated total in array
                        femalePlayerRankings[i] = (player[0] + '-' + str(player[1]) + '-' + total)
                    elif len(prevPlayer) > 3 >= len(player):  # Adds previous money to empty amount
                        femalePlayerRankings[i] += ("-" + str(prevPlayer[2]))

    """Displays results of the current round"""
    def display_round_winners(self, roundNum):
        clear_screen()
        print("\nThe following results for round " + str(roundNum) + " have been calculated:")

        maleLosers = []
        maleNames = []
        femaleLosers = []
        femaleNames = []

        # Get MALE losers
        for losers in malePlayerRankings:
            loser = losers.split('-')
            maleLosers.append(loser[0])

        # Get MALE names and create winner list
        with open(malePlayersFile) as csvFile:
            readCsv = csv.reader(csvFile, delimiter=',')
            for row in readCsv:
                maleNames.append(row[0])
        maleWinners = [n for n in maleNames if n not in maleLosers]

        # Prints all MALE winners
        print("\nMale Winners:")
        for winnerName in maleWinners:
            print("Player Name - " + str(winnerName))

        # Get FEMALE losers
        for losers in femalePlayerRankings:
            loser = losers.split('-')
            femaleLosers.append(loser[0])

        # Get FEMALE names and create winner list
        with open(femalePlayersFile) as csvFile:
            readCsv = csv.reader(csvFile, delimiter=',')
            for row in readCsv:
                femaleNames.append(row[0])
        femaleWinners = [n for n in femaleNames if n not in femaleLosers]

        # Prints all FEMALE winners
        print("\nFemale Winners:")
        for winnerName in femaleWinners:
            print("Player Name - " + str(winnerName))

    """Displays results to the user via the prompt"""
    def display_results(self):
        clear_screen()
        print("The following results for tournament " + tournamentName + " have been calculated:")

        # Displays the MALE PLAYER results
        tempPrizeArray = []
        print("\nMale Players in order of prize money:")
        for place, players in enumerate(malePlayerRankings[::-1]):  # Loops in descending order
            player = players.split('-')  # Splits player information
            # Adds players position in tournament to array
            malePlayerRankings[(len(malePlayerRankings) - (place + 1))] += ('-' + str(place + 1))
            if len(player) > 2:  # Adds money amount to temp array, if player has any
                tempPrizeArray.append(float(player[2]))
        # Print in order of prize money won
        tempPrizeArray.sort()
        tempPrizeArray.reverse()
        while len(tempPrizeArray) > 1:
            for rankings in malePlayerRankings[::-1]:
                result = rankings.split('-')  # Splits player information
                if len(result) > 3:
                    if float(result[2]) == tempPrizeArray[0]:
                        tempPrizeArray.remove(tempPrizeArray[0])
                        money = "%.2f" % float(result[2])
                        print("Player Name - " + result[0] + ", Ranking Points - " + result[1]
                              + ", Prize Money - $" + money + ", Place - " + result[3])
        # Displays players who didn't win money
        for rankings in malePlayerRankings[::-1]:
            result = rankings.split('-')  # Splits player information
            if len(result) <= 3:
                print("Player Name - " + result[0] + ", Ranking Points - " + result[1] + ", Place - " + result[2])

        # Displays the FEMALE PLAYER results
        tempPrizeArray = []
        print("\nFemale Players in order of prize money:")
        for place, players in enumerate(femalePlayerRankings[::-1]):  # Loops in descending order
            player = players.split('-')  # Splits player information
            # Adds players position in tournament to array
            femalePlayerRankings[(len(femalePlayerRankings) - (place + 1))] += ('-' + str(place + 1))
            if len(player) > 2:  # Adds money amount to temp array, if player has any
                tempPrizeArray.append(float(player[2]))
        # Print in order of prize money won
        tempPrizeArray.sort()
        tempPrizeArray.reverse()
        while len(tempPrizeArray) > 1:
            for rankings in femalePlayerRankings[::-1]:
                result = rankings.split('-')  # Splits player information
                if len(result) > 3:
                    if float(result[2]) == tempPrizeArray[0]:
                        tempPrizeArray.remove(tempPrizeArray[0])
                        money = "%.2f" % float(result[2])
                        print("Player Name - " + result[0] + ", Ranking Points - " + result[1]
                              + ", Prize Money - $" + money + ", Place - " + result[3])
        # Displays players who didn't win money
        for rankings in femalePlayerRankings[::-1]:
            result = rankings.split('-')  # Splits player information
            if len(result) <= 3:
                print(
                    "Player Name - " + result[0] + ", Ranking Points - " + result[1] + ", Place - " + result[2])

    """Stores results in files named by the user"""
    def store_result_file(self):
        invalidChars = set(string.punctuation.replace("_", ""))  # Allows set symbols in fileName
        # Stores MALE PLAYER results in a file
        # Gets valid file name
        print("\nPlease enter the desired file name to store the MALE PLAYER results: ")
        while True:
            try:  # Validates against blank entries
                fileName = input("::")
            except SyntaxError:
                fileName = None
            if any(char in invalidChars for char in fileName):
                print("Invalid character entered!")
            elif fileName is None:
                print("Please enter something!")
            elif (fileName + ".csv") in os.listdir():
                print("That name is taken by another file!")
            else:
                break
        # Creates file using chosen name in root directory
        with open((directoryPath + "\\" + fileName + ".csv"), 'w', newline="\n", encoding="utf-8") as csvFile:
            writer = csv.writer(csvFile, dialect='excel')
            header = ['Place', 'Player Name', 'Ranking Points', 'Prize Money($)']  # Sets file headers
            writer.writerow(header)
            # Fill tempPrizeArray
            tempPrizeArray = []
            for players in malePlayerRankings[::-1]:  # Loops in descending order
                player = players.split('-')  # Splits player information
                if len(player) > 3:  # Adds money amount to temp array, if player has any
                    tempPrizeArray.append(float(player[2]))
            tempPrizeArray.sort()
            tempPrizeArray.reverse()

            # Writes player information in order of prize money to file
            while len(tempPrizeArray) > 1:
                for row in malePlayerRankings[::-1]:
                    data = row.split('-')  # Splits player information
                    if len(data) > 3:
                        if float(data[2]) == tempPrizeArray[0]:
                            tempPrizeArray.remove(tempPrizeArray[0])
                            line = [str(data[3]), str(data[0]), str(data[1]), str(data[2])]
                            writer.writerow(line)
            # Displays players who didn't win money
            for row in malePlayerRankings[::-1]:
                data = row.split('-')  # Splits player information
                if len(data) <= 3:
                    line = [str(data[2]), str(data[0]), str(data[1]), 'N/A']
                    writer.writerow(line)

        # Stores FEMALE PLAYER results in a file
        # Gets valid file name
        print("\nPlease enter the desired file name to store the FEMALE PLAYER results: ")
        while True:
            try:  # Validates against blank entries
                fileName = input("::")
            except SyntaxError:
                fileName = None
            if any(char in invalidChars for char in fileName):
                print("Invalid character entered!")
            elif fileName is None:
                print("Please enter something!")
            elif (fileName + ".csv") in os.listdir():
                print("That name is taken by another file!")
            else:
                break
        # Creates file using chosen name in root directoryPath
        with open((directoryPath + "\\" + fileName + ".csv"), 'w', newline="\n", encoding="utf-8") as csvFile:
            writer = csv.writer(csvFile, dialect='excel')
            header = ['Place', 'Player Name', 'Ranking Points', 'Prize Money($)']  # Sets file headers
            writer.writerow(header)

            # Fill tempPrizeArray
            tempPrizeArray = []
            for players in femalePlayerRankings[::-1]:  # Loops in descending order
                player = players.split('-')  # Splits player information
                if len(player) > 3:  # Adds money amount to temp array, if player has any
                    tempPrizeArray.append(float(player[2]))
            tempPrizeArray.sort()
            tempPrizeArray.reverse()

            # Writes player information in order of prize money to file
            while len(tempPrizeArray) > 1:
                for row in femalePlayerRankings[::-1]:
                    data = row.split('-')  # Splits player information
                    if len(data) > 3:
                        if float(data[2]) == tempPrizeArray[0]:
                            tempPrizeArray.remove(tempPrizeArray[0])
                            line = [str(data[3]), str(data[0]), str(data[1]), str(data[2])]
                            writer.writerow(line)
            # Displays players who didn't win money
            for row in femalePlayerRankings[::-1]:
                data = row.split('-')  # Splits player information
                if len(data) <= 3:
                    line = [str(data[2]), str(data[0]), str(data[1]), 'N/A']
                    writer.writerow(line)

initial_menu()
if __name__ == "__main__": main()