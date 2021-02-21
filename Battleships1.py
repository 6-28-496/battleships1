__author__ = 'Galen'

from random import randint

def main():
    print("Welcome to Battleships!")
    game()


def game():
    compFleet = [["~"] * 10 for i in range(10)] # initialise the computer fleet with blank cells ("~")
    humanFleet = [["~"] * 10 for i in range(10)]
    compDeploy(compFleet)
    # showFleet(compFleet, False)
    humanDeploy(humanFleet)

    lastHitX = 10 # the x and y coordinates of the last cell that the computer hit
    lastHitY = 10 # initialised to 10 at the start of the game
    compIsUp = True

    while isPlayerAlive(compFleet) == True and isPlayerAlive(humanFleet) == True:
        if compIsUp == True:
            compTurn(humanFleet, lastHitX, lastHitY)
            compIsUp = False # now it's the human player's turn
        else:
            humanTurn(compFleet)
            compIsUp = True # now it's the computer player's turn

    if isPlayerAlive(humanFleet):
        print("You have won the game.")
    else:
        print("You have lost the game.")

    showFleet(compFleet, False) # show the final positions of the computer player's fleet for good measure


def compDeploy(compFleet):
    xStart = 0
    xEnd = 0
    yStart = 0
    yEnd = 0

    for shipLength in range (1, 6):
        vertical = randint(0, 1)# flag to determine if ship is vertical (1) or horizontal (0)
        if vertical == 1: # if ship is vertical
            xStart = randint(0, 9)
            xEnd = xStart # ship is vertical, so the start x-coordinate is the same as the end x-coordinate
            yStart = randint(0, 9-(shipLength-1))
            yEnd = yStart + (shipLength-1)
            while areaIsClear(xStart, xEnd, yStart, yEnd, compFleet) == False: # keep looping till ship is deployed
                xStart = randint(0, 9)
                xEnd = xStart
                yStart = randint(0, 9-(shipLength-1))
                yEnd = yStart + (shipLength-1)

            for i in range (yStart, yEnd+1):
                compFleet[xStart][i] = "S"

        else: # if ship is horizontal
            xStart = randint(0, 9-(shipLength-1))
            xEnd = xStart + (shipLength-1)
            yStart = randint(0, 9)
            yEnd = yStart # ship is horizontal, so the start y-coordinate is the same as the end y-coordinate
            while areaIsClear(xStart, xEnd, yStart, yEnd, compFleet) == False: # keep looping till ship is deployed
                xStart = randint(0, 9-(shipLength-1))
                xEnd = xStart + (shipLength-1)
                yStart = randint(0, 9)
                yEnd = yStart

            # fill in the cells for the ship with the letter S
            for i in range (xStart, xEnd+1):
                compFleet[i][yStart] = "S"

    return compFleet


def humanDeploy(humanFleet):
    showFleet(humanFleet, False)

    # deploy the ship of length 1:
    print("Please enter the coordinate for the ship of length 1 e.g. A0")
    coordinate = input("> ")

    while validCoordinate(coordinate) == False: # check if the coordinate entered is valid or not
        print("Please enter a valid coordinate in the form column-row, e.g. A0")
        coordinate = input("> ")

    # store the ship of length 1 in the humanFleet list
    humanFleet[ord(coordinate[0]) - ord("A")][int(coordinate[1])] = "S"

    for shipLength in range (2,6):
        validShip = False # set this flag to False initially so following code runs at least once

        while validShip == False:
            showFleet(humanFleet, False)

            print("Please enter the first coordinate for the ship of length", shipLength, "e.g. A0")
            coordinate = input("> ")

            while validCoordinate(coordinate) == False: # check if the coordinate entered is valid or not
                print("Please enter a valid coordinate in the form column-row, e.g. A0")
                coordinate = input("> ")

            xStart = ord(coordinate[0]) - ord("A")
            yStart = ord(coordinate[1]) - ord("0")

            print("Should this ship be horizontal (H) or vertical (V)?")
            orientation = input("> ")
            # loop while orientation is not valid
            while orientation != "H" and orientation != "V" and orientation != "h" and orientation != "v":
                print("Please enter either H for horizontal or V for vertical!")
                orientation = input("> ")

            if orientation == "H" or orientation == "h": # if ship is horizontal
                xEnd = xStart + (shipLength - 1)
                yEnd = yStart

                if xEnd > 9: # if ship deployment is too far to the right
                    print("This deployment is too far to the right!")
                    # check to see if this deployment would overlap with another one:
                elif areaIsClear(xStart, xEnd, yStart, yEnd, humanFleet) == False:
                        print("This deployment overlaps with another ship!")
                else:
                    validShip = True # deployment is successful
                    for i in range (xStart, xEnd + 1):
                        humanFleet[i][yStart] = "S" # fill in ship's space with S's

            if orientation == "V" or orientation == "v": # if ship is vertical
                xEnd = xStart
                yEnd = yStart + (shipLength - 1)

                if yEnd > 9: # if ship deployment is too far down
                    print("This deployment is too far down!")
                    # check to see if this deployment would overlap with another one:
                elif areaIsClear(xStart, xEnd, yStart, yEnd, humanFleet) == False:
                        print("This deployment overlaps with another ship!")
                else:
                    validShip = True
                    for i in range (yStart, yEnd + 1):
                        humanFleet[xStart][i] = "S" # fill in ship's space with S's

    return humanFleet


def compTurn(humanFleet, lastHitX, lastHitY):
    if lastHitX == 10 and lastHitY == 10: # if the computer hasn't hit anything yet
        targetX = randint(0, 9)
        targetY = randint(0, 9)

    newTarget = False # set this flag to False so the following code runs at least once:

    while newTarget == False:
        if humanFleet[targetX][targetY] == "S":
            humanFleet[targetX][targetY] = "X"
            print("The computer hit one of your ships!")
            newTarget = True
        elif humanFleet[targetX][targetY] == "~":
            humanFleet[targetX][targetY] = "."
            print("The computer missed.")
            newTarget = True
        else:
            targetX = randint(0, 9)
            targetY = randint(0, 9)

    showFleet(humanFleet, False)
    return humanFleet


def humanTurn(compFleet):
    newTarget = False # set this flag to False so the following code runs at least once

    while newTarget == False:
        showFleet(compFleet, True) # display the computer player's fleet with fog of war turned on, i.e. ships hidden
        print("Please enter a coordinate for your next strike:")
        coordinate = input("> ")

        if coordinate == "reveal":
            print ("Shame on you for cheating!")
            showFleet(compFleet, False) # displays the entire computer fleet, then gives the user another attempt

        while validCoordinate(coordinate) == False: # check if the coordinate entered is valid or not
            print("Please enter a valid coordinate in the form column-row, e.g. A0")
            coordinate = input("> ")

        xStrike = ord(coordinate[0]) - ord("A")
        yStrike = ord(coordinate[1]) - ord("0")

        if compFleet[xStrike][yStrike] == "." or compFleet[xStrike][yStrike] == "X": # if cell has been targeted before
            print("Please enter a coordinate you have not yet attacked.")
        elif compFleet[xStrike][yStrike] == "~":
            print("You missed.")
            compFleet[xStrike][yStrike] = "."
            newTarget = True
        elif compFleet[xStrike][yStrike] == "S":
            print("You hit a ship!")
            compFleet[xStrike][yStrike] = "X"
            newTarget = True

    return compFleet


def isPlayerAlive(fleet):
    for j in range (10):
        for i in range (10):
            if fleet[i][j] == "S": # if player has a single ship cell alive, the player is alive
                return True

    return False # no ship cells survive, so the player is not alive


def validCoordinate(coordinate):
    # test whether or not the string entered is false
    if len(coordinate) != 2:
        print("Coordinate should be two characters long!")
        return False
    elif coordinate[0] < "A" or coordinate[0] > "J":
        print("The column coordinate should be between A and J!")
        return False
    elif coordinate[1] < "0" or coordinate[1] > "9":
        print("The row coordinate should be between 0 and 9!")
        return False
    else:
        return True


def showFleet(fleet, fogOfWar):
    # print top of table
    print() # print a blank line
    print(" ", end=" ")
    for i in range(9): # print the letters A through I at the top of the table
        print(chr(i + ord("A")), end=" ")
    print("J") # include a carriage return at the end of the row

    # print rows of table
    for j in range(10):
        print(j, end=" ")
        for i in range(9):
            if fleet[i][j] == "S" and fogOfWar == True: # show an empty cell if actually empty or if fogOfWar flag is true
                print("~", end=" ")
            else:
                print(fleet[i][j], end=" ")
        # make sure that last cell in row is always printed with a carriage return
        if fleet[9][j] == "S" and fogOfWar == True: # show an empty cell if actually empty or if fogOfWar flag is true
            print("~")
        else:
            print(fleet[9][j])


def areaIsClear(xStart, xEnd, yStart, yEnd, compFleet):
    # trying to deploy a vertical ship:
    if xStart == xEnd:
        for y in range(yStart, yEnd+1):
            if compFleet[xStart][y] != "~":
                return False

    # trying to deploy a horizontal ship:
    elif yStart == yEnd:
        for x in range(xStart, xEnd+1):
            if compFleet[x][yStart] != "~":
                return False

    return True

main()