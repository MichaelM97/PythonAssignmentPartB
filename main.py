# Name: Assignment Project Part B
# Author: Michael McCormick (15012271)

import csv
import os
import sys
import string


def main():
    fileInfo = FileInformation() # Create object to access class

    fileInfo.get_file_names() # Get file names from user

    tournamentCount = fileInfo.get_tournament_count()  # Keep track of number of tournaments processed

    # Add previous tournament data to season ranking list
    if tournamentCount != 0:
        fileInfo.process_temp_tournament_data()

    while tournamentCount <= 4:  # Loop allows for entry of additional tournaments

        tournamentCount += 1

        # Create temp files or process information
        count = fileInfo.create_temp_info_file()

        if count == 1:  # Only do for round 1
            score_input_menu(fileInfo, count)  # User chooses if scores entered manually or via file
            # Store information from selected files
            fileInfo.store_ranking_info()
            fileInfo.store_prize_info()
            fileInfo.store_player_names()

        # Process round 1 scores
        if count == 1:
            if scoreChoice == '1':
                fileInfo.process_file_scores(count)
            else:
                fileInfo.get_score_input(count)
                fileInfo.process_user_scores(count)
            fileInfo.display_round_winners(count)
            count += 1

        # Get file selection from user, and loop through to calculate players scores
        while count < 6 and maleRankingPosition > 1 and femaleRankingPosition > 1:
            score_input_menu(fileInfo, count)  # User chooses if scores entered manually or via file
            fileInfo.reset_player_names()  # Fills player name list with losers for user input

            # Get score input from FILE
            if scoreChoice == '1':
                fileInfo.process_file_scores(count)
                fileInfo.display_round_winners(count)
                count += 1

            # Get score input from USER
            elif scoreChoice == '2':
                fileInfo.reset_player_names()
                fileInfo.get_score_input(count)
                fileInfo.process_user_scores(count)
                fileInfo.display_round_winners(count)
                count += 1

        # Calculate players ranking points and add to season results
        fileInfo.multiply_ranking_points()
        fileInfo.add_season_results()

        # Display results
        clear_screen()
        while True:
            print("\nHow would you like to view the tournament data?: \n1 - Prize Money Order\n2 - Ranking Point Order"
                  "\n3 - Overall Season Ranking\n4 - Exit program\n")
            userInput = get_valid_input().upper()
            if userInput == '1':
                fileInfo.display_results_prize_order()
                break
            elif userInput == '2':
                fileInfo.display_results_points_order()
                break
            elif userInput == '3':
                fileInfo.display_season_results()
                break
            elif userInput == '4':
                sys.exit("Thank you for using the system.")
            else:
                print("Invalid Input!!!\n")

        if tournamentCount < 4:
            # Prepare system for additional tournament entries
            clear_screen()
            while True:
                print("Would you like to process another tournament for this season?[Y/N]\n")
                userInput = get_valid_input().upper()
                if userInput == 'Y':
                    fileInfo.create_temp_tournament_files(tournamentCount)
                    fileInfo.delete_temp_files()
                    fileInfo.add_season_results()
                    global malePlayerRankings
                    malePlayerRankings = []
                    global femalePlayerRankings
                    femalePlayerRankings = []
                    global malePrizeMoneyInfo
                    malePrizeMoneyInfo = []
                    global femalePrizeMoneyInfo
                    femalePrizeMoneyInfo = []
                    break
                elif userInput == 'N':
                    sys.exit("Thank you for using the system.")
                    break
                else:
                    print("Invalid Input!!!\n")

    clear_screen()
    print("The season is complete. Please view the results below.\n")
    fileInfo.display_season_results()
    sys.exit("Thank you for using the system.")


"""Allows user to choose to enter scores manually or from files"""
def score_input_menu(fileInfo, roundNum):
    clear_screen()
    global scoreChoice

    #  Get valid user input
    while True:
        print("Please select an option for round %d:\n\n1 - Read players score from file\n"
              "2 - Enter players score manually\n3 - Exit system\n" % roundNum)
        scoreChoice = get_valid_input()
        if scoreChoice == '1':
            fileInfo.get_score_files(roundNum)
            fileInfo.set_difficulty(maleScoresFile)  # Attempt to pull difficulty from file name
            break
        elif scoreChoice == '2':
            if roundNum == 1:
                fileInfo.set_difficulty("")  # Set difficulty using user input
            break
        elif scoreChoice == '3':
            sys.exit("Thank you for using the system.")
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
            "\nand Female Player Names placed within the 'data' folder;"
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

    # Ranking point modifiers
    global HIGHEST_MODIFIER
    HIGHEST_MODIFIER = 2.5
    global MIDDLE_MODIFIER
    MIDDLE_MODIFIER = 1.5
    global LOWEST_MODIFIER
    LOWEST_MODIFIER = 1

    # Retrieves directory path to data folder
    global directoryPath
    directoryPath = str(os.path.dirname(os.path.realpath(__file__))) + "\\data"

    # Allow global access to the data folder file list
    global fileList
    fileList = os.listdir(directoryPath)

    # Check for presence of temp files
    global tempFilesExist
    tempFilesExist = False
    global tournamentFilesExist
    tournamentFilesExist = False
    if 'TEMPINFO.csv' in fileList:
        tempFilesExist = True
        fileList.remove('TEMPINFO.csv')
    if 'TEMPAMENDED.csv' in fileList:
        tempFilesExist = True
        fileList.remove('TEMPAMENDED.csv')
    if 'TEMP_PREVIOUS_TOURNAMENT.csv' in fileList:
        tournamentFilesExist = True
        fileList.remove('TEMP_PREVIOUS_TOURNAMENT.csv')
    if 'TEMP_PREVIOUS_WINS.csv' in fileList:
        tournamentFilesExist = True
        fileList.remove('TEMP_PREVIOUS_WINS.csv')


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
    global malePrizeMoneyInfo
    malePrizeMoneyInfo = []
    global femalePrizeMoneyInfo
    femalePrizeMoneyInfo = []
    global malePlayerRankings
    malePlayerRankings = []
    global femalePlayerRankings
    femalePlayerRankings = []
    global maleSeasonRankings
    maleSeasonRankings = []
    global femaleSeasonRankings
    femaleSeasonRankings = []
    global malePlayerWinners
    malePlayerWinners = []
    global femalePlayerWinners
    femalePlayerWinners = []
    global maleUserScores
    maleUserScores = []
    global femaleUserScores
    femaleUserScores = []
    global maleWinCount
    maleWinCount = []
    global femaleWinCount
    femaleWinCount = []

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
        FileInformation.update_temp_info_file(self, roundNum, "File", maleScoresFile)
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
        FileInformation.update_temp_info_file(self, roundNum, "File", femaleScoresFile)
        fileList.remove(femaleScoresFile)  # Removes file from list so it cannot be selected again

    """Allows user to input scores"""
    def get_score_input(self, roundNum):
        global maleUserScores
        maleUserScores = []
        global femaleUserScores
        femaleUserScores = []

        # Get MALE PLAYER scores as input
        fileCreated = False
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

            # Add MALE temp file to main temp info file if it isn't already
            if fileCreated is False:
                fileCreated = True
                maleFileName = "TEMP_MALE_" + str(roundNum) + str(tournamentName) + ".csv"
                FileInformation.update_temp_info_file(self, roundNum, "User", maleFileName)

            # Adds most recent MALE match entry to temp file
            FileInformation.update_temp_male_file(self, roundNum, row)

        # Get FEMALE PLAYER scores as input
        fileCreated = False
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

            # Add FEMALE temp file to main temp info file if it isn't already
            if fileCreated is False:
                fileCreated = True
                femaleFileName = "TEMP_FEMALE_" + str(roundNum) + str(tournamentName) + ".csv"
                FileInformation.update_temp_info_file(self, roundNum, "User", femaleFileName)

            # Adds most recent FEMALE match entry to temp file
            FileInformation.update_temp_female_file(self, roundNum, row)

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

    """Store player names provided from file, and adds them to the ranking point counter list"""
    def store_player_names(self):
        # Store MALE PLAYERS FILE information in array
        with open(directoryPath + "\\" + malePlayersFile) as csvFile:
            readCsv = csv.reader(csvFile, delimiter=',')
            for row in readCsv:
                malePlayerNames.append(row[0])
                FileInformation.update_players_points(self, True, 0.0, row[0], 0)

        # Store FEMALE PLAYERS FILE information in array
        with open(directoryPath + "\\" + femalePlayersFile) as csvFile:
            readCsv = csv.reader(csvFile, delimiter=',')
            for row in readCsv:
                femalePlayerNames.append(row[0])
                FileInformation.update_players_points(self, False, 0.0, row[0], 0)

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
        with open(directoryPath + "\\" + malePlayersFile) as csvFile:
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
        with open(directoryPath + "\\" + femalePlayersFile) as csvFile:
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
        with open(directoryPath + "\\" + rankingPointsFile) as csvFile:
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
        global malePrizeMoneyInfo
        global femalePrizeMoneyInfo

        # Store PRIZE MONEY FILE information in array
        with open(directoryPath + "\\" + prizeMoneyFile) as csvFile:
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
                        malePrizeMoneyInfo.append(row[1] + '-' + row[2])  # Add money and associated place to list
                        femalePrizeMoneyInfo.append(row[1] + '-' + row[2])  # Add money and associated place to list
                        previous = row[1]

    """Stores players in order of their scores given in a file"""
    def process_file_scores(self, roundNum):
        global maleRankingPosition
        global femaleRankingPosition

        # Double rankingPos list sizes to allow for round 1
        if int(roundNum) == 1:
            maleRankingPosition += maleRankingPosition
            femaleRankingPosition += femaleRankingPosition

        # Process MALE PLAYER scores
        with open(directoryPath + "\\" + maleScoresFile) as csvFile:
            readCsv = csv.reader(csvFile, delimiter=',')
            next(readCsv)  # Skip headers in file
            for row in readCsv:
                gameTotal = int(row[1]) + int(row[3])  # Check if too many games played
                if row[1] > row[3] and int(row[1]) == 3 and 6 > gameTotal >= 3:  # Player A wins
                    losingScore = row[3]
                    winningPlayer = row[0]
                    losingPlayer = row[2]
                elif row[1] < row[3] and int(row[3]) == 3 and 6 > gameTotal >= 3:  # Player B wins
                    losingScore = row[1]
                    winningPlayer = row[2]
                    losingPlayer = row[0]
                else:  # If no winner is found
                    # Check if game is in temp appended file
                    amendedGame = FileInformation.find_amended_score(self, roundNum, row[0], row[2])
                    if amendedGame != 0:
                        # Get winning player and losing score
                        if amendedGame[1] > amendedGame[3]:
                            winningPlayer = amendedGame[0]
                            losingPlayer = row[2]
                            losingScore = amendedGame[3]
                        else:
                            winningPlayer = amendedGame[2]
                            losingPlayer = row[0]
                            losingScore = amendedGame[1]
                    else:  # If appended score not in file, display error and get appended scores
                        amendedGame = FileInformation.handle_invalid_score(self, True, row[0], row[1], row[2], row[3])
                        # Process winning player
                        if amendedGame[1] > amendedGame[3]:
                            losingScore = amendedGame[3]
                            losingPlayer = row[2]
                            winningPlayer = row[0]
                        elif amendedGame[1] < amendedGame[3]:
                            losingScore = amendedGame[1]
                            losingPlayer = row[0]
                            winningPlayer = row[2]
                        # Add amended score to file
                        FileInformation.update_amended_file(
                            self, roundNum, row[0], amendedGame[1], row[2], amendedGame[3])
                        break
                # Calculate ranking points and assign to player
                if int(roundNum) != 5:
                    # Handle loser
                    rankingPoints = FileInformation.calculate_ranking_points(  # Assign runner up points
                        self, True, maleRankingPosition, losingScore, roundNum)
                    FileInformation.update_players_points(self, True, rankingPoints, losingPlayer, maleRankingPosition)
                    if int(roundNum) >= 3:  # Assigns losing players money from round 3 onwards
                        FileInformation.update_players_money(self, True, losingPlayer)
                    # Handle winner
                    rankingPoints = FileInformation.calculate_ranking_points(
                        self, True, maleRankingPosition, losingScore, roundNum)
                    FileInformation.update_players_points(self, True, rankingPoints, winningPlayer, maleRankingPosition)
                    FileInformation.update_players_wins(self, True, winningPlayer, losingScore, roundNum)
                else:  # If it's the final round
                    # Handle runner up
                    rankingPoints = FileInformation.calculate_ranking_points(  # Assign runner up points
                        self, True, maleRankingPosition, 2, roundNum)
                    FileInformation.update_players_points(self, True, rankingPoints, losingPlayer, maleRankingPosition)
                    FileInformation.update_players_money(self, True, losingPlayer)
                    maleRankingPosition += -1
                    # Handle winner
                    rankingPoints = FileInformation.calculate_ranking_points(
                        self, True, maleRankingPosition, losingScore, roundNum)
                    FileInformation.update_players_points(self, True, rankingPoints, winningPlayer, maleRankingPosition)
                    FileInformation.update_players_wins(self, True, winningPlayer, losingScore, roundNum)
                    FileInformation.update_players_money(self, True, winningPlayer)
                    break
                maleRankingPosition += -1

        # Process FEMALE PLAYER scores
        with open(directoryPath + "\\" + femaleScoresFile) as csvFile:
            readCsv = csv.reader(csvFile, delimiter=',')
            next(readCsv)  # Skip headers in file
            for row in readCsv:
                gameTotal = int(row[1]) + int(row[3])  # Check if too many games played
                if row[1] > row[3] and int(row[1]) == 2 and 4 > gameTotal >= 2:  # Player A wins
                    losingScore = row[3]
                    winningPlayer = row[0]
                    losingPlayer = row[2]
                elif row[1] < row[3] and int(row[3]) == 2 and 4 > gameTotal >= 2:  # Player B wins
                    losingScore = row[1]
                    winningPlayer = row[2]
                    losingPlayer = row[0]
                else:  # If no winner is found
                    # Check if game is in temp appended file
                    amendedGame = FileInformation.find_amended_score(self, roundNum, row[0], row[2])
                    if amendedGame != 0:
                        # Get winning player and losing score
                        if amendedGame[1] > amendedGame[3]:
                            winningPlayer = amendedGame[0]
                            losingPlayer = row[2]
                            losingScore = amendedGame[3]
                        else:
                            winningPlayer = amendedGame[2]
                            losingPlayer = row[0]
                            losingScore = amendedGame[1]
                    else:  # If appended score not in file, display error and get appended scores
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
                            # Process winning player
                            if firstScore > secondScore:
                                losingScore = secondScore
                                losingPlayer = row[2]
                                winningPlayer = row[0]
                            elif firstScore < secondScore:
                                losingScore = firstScore
                                losingPlayer = row[0]
                                winningPlayer = row[2]
                            # Add amended score to file
                            FileInformation.update_amended_file(
                                self, roundNum, row[0], firstScore, row[2], secondScore)
                            break
                # Calculate ranking points and assign to player
                if int(roundNum) != 5:
                    # Handle loser
                    rankingPoints = FileInformation.calculate_ranking_points(  # Assign runner up points
                        self, False, femaleRankingPosition, losingScore, roundNum)
                    FileInformation.update_players_points(
                        self, False, rankingPoints, losingPlayer, femaleRankingPosition)
                    if int(roundNum) >= 3:  # Assigns losing players money from round 3 onwards
                        FileInformation.update_players_money(self, False, losingPlayer)
                    # Handle winner
                    rankingPoints = FileInformation.calculate_ranking_points(
                        self, False, femaleRankingPosition, losingScore, roundNum)
                    FileInformation.update_players_points(
                        self, False, rankingPoints, winningPlayer, femaleRankingPosition)
                    FileInformation.update_players_wins(self, False, winningPlayer, losingScore, roundNum)
                else:  # If it's the final round
                    # Handle runner up
                    rankingPoints = FileInformation.calculate_ranking_points(  # Assign runner up points
                        self, False, femaleRankingPosition, 2, roundNum)
                    FileInformation.update_players_points(
                        self, False, rankingPoints, losingPlayer, femaleRankingPosition)
                    FileInformation.update_players_money(self, False, losingPlayer)
                    femaleRankingPosition += -1
                    # Handle winner
                    rankingPoints = FileInformation.calculate_ranking_points(
                        self, False, femaleRankingPosition, losingScore, roundNum)
                    FileInformation.update_players_points(
                        self, False, rankingPoints, winningPlayer, femaleRankingPosition)
                    FileInformation.update_players_wins(self, False, winningPlayer, losingScore, roundNum)
                    FileInformation.update_players_money(self, False, winningPlayer)
                    break
                femaleRankingPosition += -1

    """Stores players in order of their scores given by the user"""
    def process_user_scores(self, roundNum):
        global maleRankingPosition
        global femaleRankingPosition

        # Double rankingPos list sizes to allow for round 1
        if int(roundNum) == 1:
            maleRankingPosition += maleRankingPosition
            femaleRankingPosition += femaleRankingPosition

        # Process MALE PLAYER scores
        for row in maleUserScores:
            gameTotal = int(row[1]) + int(row[3])  # Check if too many games played
            if row[1] > row[3] and int(row[1]) == 3 and 6 > gameTotal >= 3:  # Player A wins
                losingScore = row[3]
                winningPlayer = row[0]
                losingPlayer = row[2]
            elif row[1] < row[3] and int(row[3]) == 3 and 6 > gameTotal >= 3:  # Player B wins
                losingScore = row[1]
                winningPlayer = row[2]
                losingPlayer = row[0]
            else:  # If no winner is found
                # Check if game is in temp appended file
                amendedGame = FileInformation.find_amended_score(self, roundNum, row[0], row[2])
                if amendedGame != 0:
                    # Get winning player and losing score
                    if amendedGame[1] > amendedGame[3]:
                        winningPlayer = amendedGame[0]
                        losingPlayer = row[2]
                        losingScore = amendedGame[3]
                    else:
                        winningPlayer = amendedGame[2]
                        losingPlayer = row[0]
                        losingScore = amendedGame[1]
                else:  # If appended score not in file, display error and get appended scores
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
                        # Process winning player
                        if firstScore > secondScore:
                            losingScore = secondScore
                            losingPlayer = row[2]
                            winningPlayer = row[0]
                        elif firstScore < secondScore:
                            losingScore = firstScore
                            losingPlayer = row[0]
                            winningPlayer = row[2]
                        # Add amended score to file
                        FileInformation.update_amended_file(
                            self, roundNum, row[0], firstScore, row[2], secondScore)
                        break
            # Calculate ranking points and assign to player
            if int(roundNum) != 5:
                # Handle loser
                rankingPoints = FileInformation.calculate_ranking_points(  # Assign runner up points
                    self, True, maleRankingPosition, losingScore, roundNum)
                FileInformation.update_players_points(self, True, rankingPoints, losingPlayer, maleRankingPosition)
                if int(roundNum) >= 3:  # Assigns losing players money from round 3 onwards
                    FileInformation.update_players_money(self, True, losingPlayer)
                # Handle winner
                rankingPoints = FileInformation.calculate_ranking_points(
                    self, True, maleRankingPosition, losingScore, roundNum)
                FileInformation.update_players_points(self, True, rankingPoints, winningPlayer, maleRankingPosition)
                FileInformation.update_players_wins(self, True, winningPlayer, losingScore, roundNum)
            else:  # If it's the final round
                # Handle runner up
                rankingPoints = FileInformation.calculate_ranking_points(  # Assign runner up points
                    self, True, maleRankingPosition, 2, roundNum)
                FileInformation.update_players_points(self, True, rankingPoints, losingPlayer, maleRankingPosition)
                FileInformation.update_players_money(self, True, losingPlayer)
                maleRankingPosition += -1
                # Handle winner
                rankingPoints = FileInformation.calculate_ranking_points(
                    self, True, maleRankingPosition, losingScore, roundNum)
                FileInformation.update_players_points(self, True, rankingPoints, winningPlayer, maleRankingPosition)
                FileInformation.update_players_wins(self, True, winningPlayer, losingScore, roundNum)
                FileInformation.update_players_money(self, True, winningPlayer)
                break
            maleRankingPosition += -1

        # Process FEMALE PLAYER scores
        for row in femaleUserScores:
            gameTotal = int(row[1]) + int(row[3])  # Check if too many games played
            if row[1] > row[3] and int(row[1]) == 2 and 4 > gameTotal >= 2:  # Player A wins
                losingScore = row[3]
                winningPlayer = row[0]
                losingPlayer = row[2]
            elif row[1] < row[3] and int(row[3]) == 2 and 4 > gameTotal >= 2:  # Player B wins
                losingScore = row[1]
                winningPlayer = row[2]
                losingPlayer = row[0]
            else:  # If no winner is found
                # Check if game is in temp appended file
                amendedGame = FileInformation.find_amended_score(self, roundNum, row[0], row[2])
                if amendedGame != 0:
                    # Get winning player and losing score
                    if amendedGame[1] > amendedGame[3]:
                        winningPlayer = amendedGame[0]
                        losingPlayer = row[2]
                        losingScore = amendedGame[3]
                    else:
                        winningPlayer = amendedGame[2]
                        losingPlayer = row[0]
                        losingScore = amendedGame[1]
                else:  # If appended score not in file, display error and get appended scores
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
                        # Process winning player
                        if firstScore > secondScore:
                            losingScore = secondScore
                            losingPlayer = row[2]
                            winningPlayer = row[0]
                        elif firstScore < secondScore:
                            losingScore = firstScore
                            losingPlayer = row[0]
                            winningPlayer = row[2]
                        # Add amended score to file
                        FileInformation.update_amended_file(
                            self, roundNum, row[0], firstScore, row[2], secondScore)
                        break
            # Calculate ranking points and assign to player
            if int(roundNum) != 5:
                # Handle loser
                rankingPoints = FileInformation.calculate_ranking_points(  # Assign runner up points
                    self, False, femaleRankingPosition, losingScore, roundNum)
                FileInformation.update_players_points(
                    self, False, rankingPoints, losingPlayer, femaleRankingPosition)
                if int(roundNum) >= 3:  # Assigns losing players money from round 3 onwards
                    FileInformation.update_players_money(self, False, losingPlayer)
                # Handle winner
                rankingPoints = FileInformation.calculate_ranking_points(
                    self, False, femaleRankingPosition, losingScore, roundNum)
                FileInformation.update_players_points(
                    self, False, rankingPoints, winningPlayer, femaleRankingPosition)
                FileInformation.update_players_wins(self, False, winningPlayer, losingScore, roundNum)
            else:  # If it's the final round
                # Handle runner up
                rankingPoints = FileInformation.calculate_ranking_points(  # Assign runner up points
                    self, False, femaleRankingPosition, 2, roundNum)
                FileInformation.update_players_points(
                    self, False, rankingPoints, losingPlayer, femaleRankingPosition)
                FileInformation.update_players_money(self, False, losingPlayer)
                femaleRankingPosition += -1
                # Handle winner
                rankingPoints = FileInformation.calculate_ranking_points(
                    self, False, femaleRankingPosition, losingScore, roundNum)
                FileInformation.update_players_points(
                    self, False, rankingPoints, winningPlayer, femaleRankingPosition)
                FileInformation.update_players_wins(self, False, winningPlayer, losingScore, roundNum)
                FileInformation.update_players_money(self, False, winningPlayer)
                break
            femaleRankingPosition += -1

    """Handles invalid score entries"""
    def handle_invalid_score(self, isMale, playerA, playerAScore, playerB, playerBScore):
        # Set scores based on gender
        if isMale:
            highScore = 3
            lowScore = 2
        else:
            highScore = 2
            lowScore = 1

        while True:
            print("\nERROR IN SCORE ENTRY!!!\n"
                  "Is the below score intended as a player withdraw?[Y/N]:\n"
                  + playerA + "-" + playerAScore + " v " + playerB + "-" + playerBScore)
            userInput = get_valid_input().upper()
            if userInput == 'Y':
                while True:
                    print("\nPlease select the withdrawn player:\n1 - " + playerA + "\n2 - " + playerB)
                    userInput = get_valid_input().upper()
                    if userInput == '1':
                        returnVar = [playerA] + [str(lowScore)] + [playerB] + [str(highScore)]
                        break
                    elif userInput == '2':
                        returnVar = [playerA] + [str(highScore)] + [playerB] + [str(lowScore)]
                        break
                    else:
                        print("Invalid Input!\n")
                break
            elif userInput == 'N':
                # Get a new valid score
                print("\nEnter new score for " + playerA + ":")
                while True:
                    firstScore = get_valid_input()
                    if (int(firstScore) > 3) or (int(firstScore) < 0):
                        print("Score invalid.")
                    else:
                        break
                print("\n\nEnter new score for " + playerB)
                while True:
                    secondScore = get_valid_input()
                    if (int(secondScore) > 3) or (int(secondScore) < 0):
                        print("Score invalid.")
                    else:
                        break
                returnVar = [playerA] + [str(firstScore)] + [playerB] + [str(secondScore)]
                break
            else:
                print("Invalid input!\n")
        return returnVar

    """Calculates a players ranking points based on the score of the match"""
    def calculate_ranking_points(self, isMale, rankingPos, losingScore, roundNum):
        if int(roundNum) == 1:  # No points given for round 1
            return 0
        # Calculate MALE player points
        if isMale:
            rankingPoints = float(rankingPointsInfo[rankingPos])
            if int(losingScore) == 0:
                rankingPoints = rankingPoints * HIGHEST_MODIFIER
            elif int(losingScore) == 1:
                rankingPoints = rankingPoints * MIDDLE_MODIFIER
            elif int(losingScore) == 2:
                rankingPoints = rankingPoints * LOWEST_MODIFIER
            return rankingPoints

        # Calculate FEMALE player points
        else:
            rankingPoints = int(rankingPointsInfo[rankingPos])
            if int(losingScore) == 0:
                rankingPoints = rankingPoints * HIGHEST_MODIFIER
            elif int(losingScore) == 1:
                rankingPoints = rankingPoints * LOWEST_MODIFIER
            return rankingPoints

    """Multiply each players ranking points by the tournament difficulty"""
    def multiply_ranking_points(self):
        # Multiply MALE ranking points
        for i, players in enumerate(malePlayerRankings):
            player = players.split('-')  # Splits player information
            playerName = player[0]
            playerPos = player[2]
            rankingPoints = float(player[1]) * tournamentDifficulty
            if len(player) > 3:  # If player has money
                playerMoney = player[3]
                malePlayerRankings[i] = playerName + '-' + str(rankingPoints) + '-' + str(playerPos)\
                                        + '-' + str(playerMoney)
            else:  # If player has no money
                malePlayerRankings[i] = playerName + '-' + str(rankingPoints) + '-' + str(playerPos)

        # Multiply FEMALE ranking points
        for i, players in enumerate(femalePlayerRankings):
            player = players.split('-')  # Splits player information
            playerName = player[0]
            playerPos = player[2]
            rankingPoints = float(player[1]) * tournamentDifficulty
            if len(player) > 3:  # If player has money
                playerMoney = player[3]
                femalePlayerRankings[i] = playerName + '-' + str(rankingPoints) + '-' + str(playerPos)\
                                        + '-' + str(playerMoney)
            else:  # If player has no money
                femalePlayerRankings[i] = playerName + '-' + str(rankingPoints) + '-' + str(playerPos)

    """Adds to a players ranking points"""
    def update_players_points(self, isMale, rankingPoints, playerName, rankingPos):
        global malePlayerRankings
        global femalePlayerRankings

        newPlayer = True
        # Calculate MALE player points
        if isMale:
            for i, players in enumerate(malePlayerRankings):
                player = players.split('-')  # Splits player information
                if player[0] == playerName:
                    rankingPoints += float(player[1])  # Add pre-existing points
                    if len(player) > 3:  # If player has money
                        playerMoney = player[3]
                        malePlayerRankings[i] = playerName + '-' + str(rankingPoints) + '-' + str(rankingPos) \
                                                + '-' + str(playerMoney)
                    else:  # If player has no money
                        malePlayerRankings[i] = playerName + '-' + str(rankingPoints) + '-' + str(rankingPos)
                    newPlayer = False
                    break
            if newPlayer:
                malePlayerRankings.append(playerName + '-' + str(rankingPoints) + '-' + str(rankingPos))

        # Calculate FEMALE player points
        else:
            for i, players in enumerate(femalePlayerRankings):
                player = players.split('-')  # Splits player information
                if player[0] == playerName:
                    rankingPoints += float(player[1])  # Add pre-existing points
                    if len(player) > 3:  # If player has money
                        playerMoney = player[3]
                        femalePlayerRankings[i] = playerName + '-' + str(rankingPoints) + '-' + str(rankingPos) \
                                                + '-' + str(playerMoney)
                    else:  # If player has no money
                        femalePlayerRankings[i] = playerName + '-' + str(rankingPoints) + '-' + str(rankingPos)
                    newPlayer = False
                    break
            if newPlayer:
                femalePlayerRankings.append(playerName + '-' + str(rankingPoints) + '-' + str(rankingPos))

    """Adds players win to list, and saves win type"""
    def update_players_wins(self, isMale, playerName, losingScore, roundNum):
        global maleWinCount
        global femaleWinCount

        # Add win to MALE player
        if isMale:
            # Calculate win type
            if int(losingScore) == 0:
                winType = HIGHEST_MODIFIER
            elif int(losingScore) == 1:
                winType = MIDDLE_MODIFIER
            elif int(losingScore) == 2:
                winType = LOWEST_MODIFIER
            maleWinCount.append(playerName + '-' + str(winType) + '-' + str(roundNum))

        # Add win to FEMALE player
        else:
            # Calculate win type
            if int(losingScore) == 0:
                winType = HIGHEST_MODIFIER
            elif int(losingScore) == 1:
                winType = LOWEST_MODIFIER
            femaleWinCount.append(playerName + '-' + str(winType) + '-' + str(roundNum))

    """Add prize money to the top players totals"""
    def update_players_money(self, isMale, playerName):
        global malePlayerRankings
        global femalePlayerRankings

        # Assign MALE PLAYERS winnings
        if isMale:
            for i, players in enumerate(malePlayerRankings):
                player = players.split('-')  # Splits player information
                if player[0] == playerName:
                    # Get prize money
                    prizeInfo = malePrizeMoneyInfo.pop()  # Gets last money entry in list
                    prize = prizeInfo.split('-')  # Splits prize information
                    rankingPoints = player[1]
                    playerPos = player[2]
                    money = float(prize[1].replace(',', ''))
                    malePlayerRankings[i] = playerName + '-' + str(rankingPoints) + '-' + \
                                            str(playerPos) + '-' + str(money)
                    break

        # Assign FEMALE PLAYERS winnings
        else:
            for i, players in enumerate(femalePlayerRankings):
                player = players.split('-')  # Splits player information
                if player[0] == playerName:
                    # Get prize money
                    prizeInfo = femalePrizeMoneyInfo.pop()  # Gets last money entry in list
                    prize = prizeInfo.split('-')  # Splits prize information
                    rankingPoints = player[1]
                    playerPos = player[2]
                    money = float(prize[1].replace(',', ''))
                    femalePlayerRankings[i] = playerName + '-' + str(rankingPoints) + '-' + \
                                            str(playerPos) + '-' + str(money)
                    break

    """Creates temp info file in root directory, or processes data if already present"""
    def create_temp_info_file(self):
        roundNum = 1  # Default
        if tempFilesExist:
            csvFile = open(directoryPath + "\\" + "TEMPINFO.csv")
            readCsv = csv.reader(csvFile, delimiter=',')
            fileLength = len(list(readCsv))  # Get file length
            if fileLength > 1:  # Only process if temp file has data
                clear_screen()
                print("!!!PRE-EXISTING DATA FOUND!!!\nThis will be re-entered for you.\n")
                input("\nPress 'Enter' to continue...")
                roundNum = FileInformation.process_temp_files(self)
            csvFile.close()
        else:
            # Create main TEMP INFO file
            csvFile = open((directoryPath + "\\" + "TEMPINFO.csv"), 'a', newline="\n")
            writer = csv.writer(csvFile, dialect='excel')
            writer.writerow(["Round Number"] + ["Input Type"] + ["File Name"])
            csvFile.close()

            # Create amended score file
            csvFile = open((directoryPath + "\\" + "TEMPAMENDED.csv"), 'a', newline="\n")
            writer = csv.writer(csvFile, dialect='excel')
            writer.writerow(["Round Number"] + ["Tournament Name"] + ["Player A"] + ["Player A Score"]
                            + ["Player B"] + ["Player B Score"])
            csvFile.close()
            roundNum = 1
        return roundNum

    """Updates the main temp info file with information about each rounds data"""
    def update_temp_info_file(self, roundNum, inputType, fileName):
        data = [str(roundNum)] + [str(inputType)] + [str(fileName)]
        csvFile = open((directoryPath + "\\" + "TEMPINFO.csv"), 'a', newline="\n")
        writer = csv.writer(csvFile, dialect='excel')
        writer.writerow(data)
        csvFile.close()

    """Adds user entered male data to temp file"""
    def update_temp_male_file(self, roundNum, data):
        fileName = "TEMP_MALE_" + str(roundNum) + str(tournamentName) + ".csv"  # Access/create relevant file
        files = os.listdir()
        csvFile = open((directoryPath + "\\" + fileName), 'a', newline="\n")
        writer = csv.writer(csvFile, dialect='excel')
        if fileName not in files:  # Add headers if new file
            writer.writerow(["Player A"] + ["Score Player A"] + ["Player B"] + ["Score Player B"])
        writer.writerow(data)
        csvFile.close()

    """Adds user entered female data to temp file"""
    def update_temp_female_file(self, roundNum, data):
        fileName = "TEMP_FEMALE_" + str(roundNum) + str(tournamentName) + ".csv"  # Access/create relevant file
        files = os.listdir()
        csvFile = open((directoryPath + "\\" + fileName), 'a', newline="\n")
        writer = csv.writer(csvFile, dialect='excel')
        if fileName not in files:  # Add headers if new file
            writer.writerow(["Player A"] + ["Score Player A"] + ["Player B"] + ["Score Player B"])
        writer.writerow(data)
        csvFile.close()

    """Adds amended score to temp file"""
    def update_amended_file(self, roundNum, playerA, playerAScore, playerB, playerBScore):
        data = [str(roundNum)] + [tournamentName] + [playerA] + [playerAScore] + [playerB] + [playerBScore]
        csvFile = open((directoryPath + "\\" + "TEMPAMENDED.csv"), 'a', newline="\n")
        writer = csv.writer(csvFile, dialect='excel')
        writer.writerow(data)
        csvFile.close()

    """Finds previously amended score from the temp file if it exists, returns amended game"""
    def find_amended_score(self, roundNum, playerA, playerB):
        with open(directoryPath + "\\" + "TEMPAMENDED.csv") as csvFile:
            readCsv = csv.reader(csvFile, delimiter=',')
            fileLength = len(list(readCsv))  # Get file length
            csvFile.seek(0)  # Reset file iterator pos
            counter = 0
            if fileLength > 1:  # Only if file has data
                for row in readCsv:
                    if counter == 0:
                        row = next(readCsv)  # Skip headers in file
                    counter += 1
                    # Find matching row
                    if row[0] == roundNum and row[1] == tournamentName and row[2] == playerA and row[4] == playerB:
                        returnVar = [row[2]] + [row[3]] + [row[4]] + [row[5]]
                        break
                    else:
                        returnVar = 0
            else:
                returnVar = 0
                csvFile.close()
        return returnVar

    """Processes pre-existing data provided by temp files"""
    def process_temp_files(self):
        global maleScoresFile
        global femaleScoresFile

        with open(directoryPath + "\\" + "TEMPINFO.csv") as csvFile:
            readCsv = csv.reader(csvFile, delimiter=',')
            fileLength = len(list(readCsv))  # Get file length
            csvFile.seek(0)  # Reset file iterator pos
            counter = 0
            for row in readCsv:
                if counter == 0:
                    row = next(readCsv)  # Skip headers in file
                counter += 1
                if row[0] == '1':  # Set difficulty in first round
                    FileInformation.set_difficulty(self, row[2])  # Attempt to pull difficulty from file name
                    # Store information from selected files
                    FileInformation.store_ranking_info(self)
                    FileInformation.store_prize_info(self)
                    FileInformation.store_player_names(self)
                if fileLength > counter + 1:  # If there are both complete male and female files for this round
                    # Process the male and female scores from the files
                    counter += 1
                    maleScoresFile = row[2]
                    row = next(readCsv)
                    femaleScoresFile = row[2]
                    FileInformation.process_file_scores(self, row[0])
                    roundNum = row[0]
                    FileInformation.reset_player_names(self)
                elif fileLength <= counter + 1:  # If there is possibly an incomplete file
                    # Check if MALE file is incomplete
                    if FileInformation.round_complete_check(self, row[0], row[2]) is False:
                        FileInformation.process_partial_user_input(self, row[2], 0)
                        print("Please complete the male scores entry for round %d:" % row[0])
                        FileInformation.get_score_input(self, row[0])
                        roundNum = row[0]
                        FileInformation.reset_player_names(self)
                    # Check if FEMALE file is incomplete
                    else:
                        maleFileName = row[2]
                        roundNum = row[0]
                        dataEntryType = row[1]
                        try:
                            row = next(readCsv)
                            if FileInformation.round_complete_check(self, row[0], row[2]) is False:
                                FileInformation.process_partial_user_input(self, maleFileName, row[2])
                                print("Please complete the female scores entry for round %d:" % row[0])
                                FileInformation.get_score_input(self, row[0])
                                FileInformation.reset_player_names(self)
                        except StopIteration:  # If female temp file doesn't exist
                            if dataEntryType == "File":  # Handle missing female FILE
                                # Get FEMALE SCORES File Name
                                while True:
                                    for f, fileName in enumerate(fileList):
                                        print(f, "-", fileName)
                                    print(
                                        "\nPlease select the file containing the FEMALE PLAYERS scores for round %d: "
                                        % int(roundNum))
                                    userInput = get_valid_input()
                                    if (int(userInput) < 0) or (int(userInput) > len(fileList)):
                                        print("Invalid Input!!!\n")
                                    else:
                                        break
                                # Process files
                                maleScoresFile = maleFileName
                                femaleScoresFile = fileList[int(userInput)]  # Stores female file name globally
                                fileList.remove(
                                    femaleScoresFile)  # Removes file from list so it cannot be selected again
                                FileInformation.update_temp_info_file(self, roundNum, "File", femaleScoresFile)
                                FileInformation.process_file_scores(self, roundNum)
                                FileInformation.display_round_winners(self, roundNum)
                                FileInformation.reset_player_names(self)
                            elif dataEntryType == "User":  # Handle missing female USER
                                FileInformation.process_partial_user_input(self, maleFileName, 0)
                                FileInformation.reset_player_names(self)
                                FileInformation.handle_female_input(self, roundNum)
                                FileInformation.process_user_scores(self, roundNum)
                                FileInformation.display_round_winners(self, roundNum)
                    break

        return int(roundNum) + 1  # Add 1 as the recent round would of been processed

    """Checks if file is incomplete in relation to the round number/number of players"""
    def round_complete_check(self, roundNum, fileName):
        with open(directoryPath + "\\" + fileName) as csvFile:
            readCsv = csv.reader(csvFile, delimiter=',')
            fileLength = len(list(readCsv))  # Get file length
            # Check if amount of games in file is correct for round
            roundComplete = True
            if roundNum == 1:  # Round 1 should have 16 game rows (+1 for headers)
                if fileLength != 17:
                    roundComplete = False
            elif roundNum == 2:  # Round 2 should have 8 game rows (+1 for headers)
                if fileLength != 9:
                    roundComplete = False
            elif roundNum == 3:  # Round 3 should have 4 game rows (+1 for headers)
                if fileLength != 5:
                    roundComplete = False
            elif roundNum == 4:  # Round 4 should have 2 game rows (+1 for headers)
                if fileLength != 3:
                    roundComplete = False
            elif roundNum == 5:  # Round 5 should have 1 game row (+1 for headers)
                if fileLength != 2:
                    roundComplete = False
            csvFile.close()
        return roundComplete

    """Handles when the program has male data, but no female data, via user input"""
    def handle_female_input(self, roundNum):
        global femaleUserScores
        femaleUserScores = []

        # Get FEMALE PLAYER scores as input
        fileCreated = False
        while len(femalePlayerNames) > 1:  # While there are still female players left without a score
            clear_screen()
            print("Entering FEMALE PLAYER scores for round %d: \n" % int(roundNum))
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

            # Add FEMALE temp file to main temp info file if it isn't already
            if fileCreated is False:
                fileCreated = True
                femaleFileName = "TEMP_FEMALE_" + str(roundNum) + str(tournamentName) + ".csv"
                FileInformation.update_temp_info_file(self, roundNum, "User", femaleFileName)

            # Adds most recent FEMALE match entry to temp file
            FileInformation.update_temp_female_file(self, roundNum, row)

    """Processes information from previously interrupted user inputted scores"""
    def process_partial_user_input(self, tempMaleFile, tempFemaleFile):
        global maleUserScores
        global femaleUserScores

        if tempMaleFile != 0:
            with open(directoryPath + "\\" + tempMaleFile) as csvFile:
                readCsv = csv.reader(csvFile, delimiter=',')
                next(readCsv)  # Skip headers in file
                # Adds matches from current round and removes them from selection
                for row in readCsv:
                    match = [row[0]] + [row[1]] + [row[2]] + [row[3]]
                    maleUserScores.append(match)
                    if row[0] in malePlayerNames:
                        malePlayerNames.remove(row[0])
                    if row[2] in malePlayerNames:
                        malePlayerNames.remove(row[2])

        # Process FEMALE PLAYER temp file
        if tempFemaleFile != 0:
            with open(directoryPath + "\\" + tempFemaleFile) as csvFile:
                readCsv = csv.reader(csvFile, delimiter=',')
                next(readCsv)  # Skip headers in file
                # Adds matches from current round and removes them from selection
                for row in readCsv:
                    match = [row[0]] + [row[1]] + [row[2]] + [row[3]]
                    femaleUserScores.append(match)
                    if row[0] in femalePlayerNames:
                        femalePlayerNames.remove(row[0])
                    if row[2] in femalePlayerNames:
                        femalePlayerNames.remove(row[2])

    """Adds the tournament results to the overall seasons"""
    def add_season_results(self):
        global maleSeasonRankings
        global femaleSeasonRankings

        # Add MALE data
        if len(maleSeasonRankings) < 1:  # If there are no pre-existing season results
            maleSeasonRankings.extend(malePlayerRankings)
        else:
            for playerRankings in malePlayerRankings:
                player = playerRankings.split('-')
                for i, seasonRankings in enumerate(maleSeasonRankings):
                    season = seasonRankings.split('-')
                    if player[0] == season[0]:  # Player match found
                        rankingPoints = float(season[1]) + float(player[1])
                        if len(player) > 3:  # Player has money
                            money = float(season[3]) + float(player[3])
                            maleSeasonRankings[i] = player[0] + '-' + str(rankingPoints) + '-' + "0" + '-' + str(money)
                        else:
                            if len(season) > 3:  # Player has previous money
                                maleSeasonRankings[i] = player[0] + '-' + str(rankingPoints) +\
                                                        '-' + "0" + '-' + season[3]
                            else:
                                maleSeasonRankings[i] = player[0] + '-' + str(rankingPoints) + '-' + "0" + '-' + "0.0"

        # Add FEMALE data
        if len(femaleSeasonRankings) < 1:  # If there are no pre-existing season results
            femaleSeasonRankings.extend(femalePlayerRankings)
        else:
            for playerRankings in femalePlayerRankings:
                player = playerRankings.split('-')
                for i, seasonRankings in enumerate(femaleSeasonRankings):
                    season = seasonRankings.split('-')
                    if player[0] == season[0]:  # Player match found
                        rankingPoints = float(season[1]) + float(player[1])
                        if len(player) > 3:  # Player has money
                            money = float(season[3]) + float(player[3])
                            femaleSeasonRankings[i] = player[0] + '-' + str(rankingPoints) + '-' +\
                                                      "0" + '-' + str(money)
                        else:
                            if len(season) > 3:  # Player has previous money
                                femaleSeasonRankings[i] = player[0] + '-' + str(rankingPoints) +\
                                                          '-' + "0" + '-' + season[3]
                            else:
                                femaleSeasonRankings[i] = player[0] + '-' + str(rankingPoints) + '-' + "0" + '-' + "0.0"

    """Displays results of the current round"""
    def display_round_winners(self, roundNum):
        clear_screen()
        print("\nThe following results for round " + str(roundNum) + " have been calculated:")

        # Prints all MALE winners
        print("\nMale Winners:")
        for winners in maleWinCount:
            winner = winners.split('-')  # Splits win information
            if int(winner[2]) == roundNum:
                print("Player Name - " + winner[0])

        # Prints all FEMALE winners
        print("\nFemale Winners:")
        for winners in femaleWinCount:
            winner = winners.split('-')  # Splits win information
            if int(winner[2]) == roundNum:
                print("Player Name - " + winner[0])

        input("\nPress 'Enter' to continue...")

    """Displays results to the user in order of prize money won"""
    def display_results_prize_order(self):
        clear_screen()
        print("The following results for tournament " + tournamentName + " have been calculated:")

        # Displays the MALE PLAYER results
        tempPlayerArray = []
        print("\nMale Players in order of prize money:")
        for players in malePlayerRankings:
            player = players.split('-')  # Splits player information
            #  Create temp list
            if len(player) > 3:
                tempPlayerArray.append([player[0]] + [player[1]] + [player[2]] + [player[3]])
            else:
                tempPlayerArray.append([player[0]] + [player[1]] + [player[2]] + ["0.0"])
        tempPlayerArray.sort(key=lambda x: float(x[3]))  # Sort list
        for player in tempPlayerArray[::-1]:
            rankingPoints = "%.2f" % float(player[1])
            if float(player[3]) != 0.0:
                money = "%.2f" % float(player[3])
                print("Player Name - " + player[0] + ", Ranking Points - " + rankingPoints
                      + ", Prize Money - $" + money + ", Place - " + player[2])
            else:
                print("Player Name - " + player[0] + ", Ranking Points - " + rankingPoints + ", Place - " +
                      player[2])

        # Displays the FEMALE PLAYER results
        tempPlayerArray = []
        print("\nFemale Players in order of prize money:")
        for players in femalePlayerRankings:
            player = players.split('-')  # Splits player information
            #  Create temp list
            if len(player) > 3:
                tempPlayerArray.append([player[0]] + [player[1]] + [player[2]] + [player[3]])
            else:
                tempPlayerArray.append([player[0]] + [player[1]] + [player[2]] + ["0.0"])
        tempPlayerArray.sort(key=lambda x: float(x[3]))  # Sort list
        for player in tempPlayerArray[::-1]:
            rankingPoints = "%.2f" % float(player[1])
            if float(player[3]) != 0.0:
                money = "%.2f" % float(player[3])
                print("Player Name - " + player[0] + ", Ranking Points - " + rankingPoints
                      + ", Prize Money - $" + money + ", Place - " + player[2])
            else:
                print("Player Name - " + player[0] + ", Ranking Points - " + rankingPoints + ", Place - " +
                      player[2])

        input("\nPress 'Enter' to continue...")

    """Displays results to the user in order of ranking points"""
    def display_results_points_order(self):
        clear_screen()
        print("The following results for tournament " + tournamentName + " have been calculated:")

        # Displays the MALE PLAYER results
        tempPlayerArray = []
        print("\nMale Players in order of ranking points:")
        for players in malePlayerRankings:
            player = players.split('-')  # Splits player information
            #  Create temp list
            if len(player) > 3:
                tempPlayerArray.append([player[0]] + [player[1]] + [player[2]] + [player[3]])
            else:
                tempPlayerArray.append([player[0]] + [player[1]] + [player[2]] + ["0.0"])
        tempPlayerArray.sort(key=lambda x: float(x[1]))  # Sort list
        for player in tempPlayerArray[::-1]:
            rankingPoints = "%.2f" % float(player[1])
            if float(player[3]) != 0.0:
                money = "%.2f" % float(player[3])
                print("Player Name - " + player[0] + ", Ranking Points - " + rankingPoints
                      + ", Prize Money - $" + money + ", Place - " + player[2])
            else:
                print("Player Name - " + player[0] + ", Ranking Points - " + rankingPoints + ", Place - " +
                      player[2])

        # Displays the FEMALE PLAYER results
        tempPlayerArray = []
        print("\nFemale Players in order of ranking points:")
        for players in femalePlayerRankings:
            player = players.split('-')  # Splits player information
            #  Create temp list
            if len(player) > 3:
                tempPlayerArray.append([player[0]] + [player[1]] + [player[2]] + [player[3]])
            else:
                tempPlayerArray.append([player[0]] + [player[1]] + [player[2]] + ["0.0"])
        tempPlayerArray.sort(key=lambda x: float(x[1]))  # Sort list
        for player in tempPlayerArray[::-1]:
            rankingPoints = "%.2f" % float(player[1])
            if float(player[3]) != 0.0:
                money = "%.2f" % float(player[3])
                print("Player Name - " + player[0] + ", Ranking Points - " + rankingPoints
                      + ", Prize Money - $" + money + ", Place - " + player[2])
            else:
                print("Player Name - " + player[0] + ", Ranking Points - " + rankingPoints + ", Place - " +
                      player[2])

        input("\nPress 'Enter' to continue...")

    """Displays overall season rankings"""
    def display_season_results(self):
        clear_screen()
        print("The following results for the current season have been calculated:")

        # Displays the MALE PLAYER results
        tempPlayerArray = []
        print("\nMale Players in order of ranking points:")
        for players in maleSeasonRankings:
            player = players.split('-')  # Splits player information
            #  Create temp list
            if len(player) > 3:
                tempPlayerArray.append([player[0]] + [player[1]] + [player[2]] + [player[3]])
            else:
                tempPlayerArray.append([player[0]] + [player[1]] + [player[2]] + ["0.0"])
        tempPlayerArray.sort(key=lambda x: float(x[1]))  # Sort list
        for player in tempPlayerArray[::-1]:
            rankingPoints = "%.2f" % float(player[1])
            if float(player[3]) != 0.0:
                money = "%.2f" % float(player[3])
                print("Player Name - " + player[0] + ", Ranking Points - " + rankingPoints
                      + ", Prize Money - $" + money)
            else:
                print("Player Name - " + player[0] + ", Ranking Points - " + rankingPoints)

        # Displays the FEMALE PLAYER results
        tempPlayerArray = []
        print("\nFemale Players in order of ranking points:")
        for players in femaleSeasonRankings:
            player = players.split('-')  # Splits player information
            #  Create temp list
            if len(player) > 3:
                tempPlayerArray.append([player[0]] + [player[1]] + [player[2]] + [player[3]])
            else:
                tempPlayerArray.append([player[0]] + [player[1]] + [player[2]] + ["0.0"])
        tempPlayerArray.sort(key=lambda x: float(x[1]))  # Sort list
        for player in tempPlayerArray[::-1]:
            rankingPoints = "%.2f" % float(player[1])
            if float(player[3]) != 0.0:
                money = "%.2f" % float(player[3])
                print("Player Name - " + player[0] + ", Ranking Points - " + rankingPoints
                      + ", Prize Money - $" + money)
            else:
                print("Player Name - " + player[0] + ", Ranking Points - " + rankingPoints)

        input("\nPress 'Enter' to continue...")

    """Adds tournament data to temp files"""
    def create_temp_tournament_files(self, tournamentCount):
        # Create temp file containing ranking points and prize money won
        with open((directoryPath + "\\" + "TEMP_PREVIOUS_TOURNAMENT.csv"), 'w', newline="\n",
                  encoding="utf-8") as csvFile:
            writer = csv.writer(csvFile, dialect='excel')
            header = ['Player Name', 'Ranking Points', 'Prize Money($)', 'Tournament Count']  # Sets file headers
            writer.writerow(header)
            for players in maleSeasonRankings:
                player = players.split('-')  # Splits player information
                if len(player) > 3:  # Player has money
                    line = [str(player[0]), str(player[1]), str(player[3]), str(tournamentCount)]
                else:
                    line = [str(player[0]), str(player[1]), "0.0", str(tournamentCount)]
                writer.writerow(line)
            for players in femaleSeasonRankings:
                player = players.split('-')  # Splits player information
                if len(player) > 3:  # Player has money
                    line = [str(player[0]), str(player[1]), str(player[3]), str(tournamentCount)]
                else:
                    line = [str(player[0]), str(player[1]), "0.0", str(tournamentCount)]
                writer.writerow(line)
            csvFile.close()
        # Create temp file containing wins for each player
        with open((directoryPath + "\\" + "TEMP_PREVIOUS_WINS.csv"), 'w', newline="\n",
                  encoding="utf-8") as csvFile:
            writer = csv.writer(csvFile, dialect='excel')
            header = ['Player Name', 'Win Type', 'Round Number']  # Sets file headers
            writer.writerow(header)
            for players in maleWinCount:
                player = players.split('-')  # Splits player information
                line = [str(player[0]), str(player[1]), str(player[2])]
                writer.writerow(line)
            for players in femaleWinCount:
                player = players.split('-')  # Splits player information
                line = [str(player[0]), str(player[1]), str(player[2])]
                writer.writerow(line)
            csvFile.close()

    """Gets tournament count from temp files"""
    def get_tournament_count(self):
        try:
            with open(directoryPath + "\\" + "TEMP_PREVIOUS_TOURNAMENT.csv") as csvFile:
                readCsv = csv.reader(csvFile, delimiter=',')
                fileLength = len(list(readCsv))  # Get file length
                csvFile.seek(0)  # Reset file iterator pos
                for row in readCsv:
                    row = next(readCsv)  # Skip headers
                    returnVar = row[3]
                    break
                csvFile.close()
            if fileLength <= 1:
                returnVar = 0
        except FileNotFoundError:
            returnVar = 0
        return int(returnVar)

    """Adds previous tournament data to the system"""
    def process_temp_tournament_data(self):
        global maleWinCount
        global femaleWinCount

        with open(directoryPath + "\\" + "TEMP_PREVIOUS_TOURNAMENT.csv") as csvFile:
            readCsv = csv.reader(csvFile, delimiter=',')
            next(readCsv)  # Skip headers
            for row in readCsv:
                if row[0] in malePlayerNames:
                    if len(row) > 3:  # Player has money
                        maleSeasonRankings.append(row[0] + '-' + row[1] + "0" + row[3])
                    else:
                        maleSeasonRankings.append(row[0] + '-' + row[1] + "0" + "0.0")
                elif row[0] in femalePlayerNames:
                    if len(row) > 3:  # Player has money
                        femaleSeasonRankings.append(row[0] + '-' + row[1] + "0" + row[3])
                    else:
                        femaleSeasonRankings.append(row[0] + '-' + row[1] + "0" + "0.0")
            csvFile.close()
        with open(directoryPath + "\\" + "TEMP_PREVIOUS_WINS.csv") as csvFile:
            readCsv = csv.reader(csvFile, delimiter=',')
            next(readCsv)  # Skip headers
            for row in readCsv:
                if row[0] in malePlayerNames:
                    maleWinCount.append(row[0] + '-' + row[1] + '-' + row[2])
                elif row[0] in femalePlayerNames:
                    femaleWinCount.append(row[0] + '-' + row[1] + '-' + row[2])

    """Delete temp files to allow for further tournament processing"""
    def delete_temp_files(self):
        # Remove temp round files
        with open(directoryPath + "\\" + "TEMPINFO.csv") as csvFile:
            readCsv = csv.reader(csvFile, delimiter=',')
            next(readCsv)  # Skip headers in file
            for row in readCsv:
                if 'TEMP' in str(row[2]):
                    os.remove(directoryPath + "\\" + str(row[2]))
            csvFile.close()
        # Remove main temp files
        os.remove(directoryPath + "\\" + "TEMPINFO.csv")
        os.remove(directoryPath + "\\" + "TEMPAMENDED.csv")

initial_menu()
if __name__ == "__main__": main()