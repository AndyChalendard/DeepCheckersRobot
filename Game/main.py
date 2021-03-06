import matplotlib.pyplot as plt

import player as pl
import game as ga
import random
import models as mod

def graphShow(axs, gamesWinRatioLastXGames, gamesWinRatio, gamesWinLoseDiff, gamesWin):
    axs[0,0].plot(gamesWinRatioLastXGames, 'tab:green')
    axs[0,0].axis([10, party, 0, 1])
    axs[0,1].plot(gamesWinRatio, 'tab:green')
    axs[0,1].axis([10, party, 0, 1])
    axs[1,0].plot(gamesWinLoseDiff, 'tab:green')
    axs[1,0].axis([10, party, min(gamesWinLoseDiff), max(gamesWinLoseDiff)])
    axs[1,1].plot(gamesWin, 'tab:green')
    axs[1,1].axis([10, party, 0, party])

    plt.pause(0.0001)


if __name__ == "__main__":
    NB_GAMES_AVERAGE = 50

    classicConfig = True
    print("___________________________________")
    print("Do you want to play with the classic configuration? (Y/n)")
    response = input(">")
    if (response == "N" or response == "n"):
        classicConfig = False
    
    if (classicConfig == True):
        learn = False

        playerRedType = pl.PlayerType.IA
        playerBlueType = pl.PlayerType.CAMERA

        import robotCom as rc
        gameRobot = rc.GameRobot()

    else:
        print("___________________________________")
        print("Type of player:")
        print(pl.PlayerType.HUMAN_TERMINAL, ") Terminal")
        print(pl.PlayerType.IA, ") AI")
        print(pl.PlayerType.RANDOM, ") Random")
        print(pl.PlayerType.CAMERA, ") Camera")
        print("")
        playerRedType = pl.PlayerType.CAMERA
        while (playerRedType == pl.PlayerType.CAMERA):
            playerRedType = int(input("Type of player red (No camera): "))
        playerBlueType = int(input("Type of player blue (No robot): "))

        gameRobot = None
        if ((playerRedType == pl.PlayerType.RANDOM or playerRedType == pl.PlayerType.IA) and playerBlueType == pl.PlayerType.CAMERA):
            print("___________________________________")
            print("Do you want to play with the robot ? (y/N)")
            response = input(">")
            if (response == "y" or response == "Y"):
                import robotCom as rc
                gameRobot = rc.GameRobot()
        
        learn = False
        if (playerRedType == pl.PlayerType.IA or playerBlueType == pl.PlayerType.IA):
            print("___________________________________")
            print("AI must learn during these games ? (y/N)")
            response = input(">")
            if (response == "y" or response == "Y"):
                learn = True

    print("___________________________________")
    print("Number of game wanted")
    try:
        nbGamesMax = int(input(">"))
    except ValueError :
        nbGamesMax = 1

    showGraph = False
    if (playerRedType == pl.PlayerType.IA and playerBlueType == pl.PlayerType.RANDOM):
        print("___________________________________")
        print("Do you want to show the graph ? (y/N)")
        response = input(">")
        if (response == "y" or response == "Y"):
            showGraph = True

    if (showGraph):
        fig, axs = plt.subplots(2,2)
        fig.suptitle('Red player stats')

        gamesWinRatioLastXGames = []
        gamesWinRatio = []
        gamesWinLoseDiff = []
        gamesWin = []

        axs[0, 0].set_title('Games win/nbGames (on the last '+str(NB_GAMES_AVERAGE)+' games)')
        axs[0, 1].set_title('Games win/nbGames')
        axs[1, 0].set_title('Games win-loses')
        axs[1, 1].set_title('Games win')
    if(learn == True and playerRedType == pl.PlayerType.IA and playerBlueType == pl.PlayerType.IA):
        randomBoard = True
    else:
        randomBoard = False

    game = ga.Game(random = randomBoard,nbMaxPawnRandom=30)
    sizeX = game.getBoard(pl.Player.BLUE).SIZE_X
    sizeY = game.getBoard(pl.Player.BLUE).SIZE_Y

    pawnSelectorModel = None
    kingMovementModel = None
    simplePawnMovementModel = None
    if (playerRedType == pl.PlayerType.IA or playerBlueType == pl.PlayerType.IA):
        pawnSelectorModel = mod.CheckersModel(mod.Mod.PAWN_SELECTOR, sizeX,sizeY)
        kingMovementModel = mod.CheckersModel(mod.Mod.KING_MOVEMENT, sizeX,sizeY)
        simplePawnMovementModel = mod.CheckersModel(mod.Mod.SIMPLE_PAWN_MOVEMENT, sizeX,sizeY)

    players = [pl.Player(pl.Player.RED,playerRedType,sizeX, sizeY, pawnSelectorModel, kingMovementModel, simplePawnMovementModel, learn),pl.Player(pl.Player.BLUE, playerBlueType,sizeX, sizeY, pawnSelectorModel, kingMovementModel, simplePawnMovementModel, learn)]
    party = 0

    redWins = 0
    blueWins = 0

    print("********************************************")
    print("New Game")
    print("********************************************")
    reward = 0

    # We play to nbGamesMax games
    while (party < nbGamesMax):
        party= party + 1

        prevScore = 0
        prevPrevScore = 0

        if (gameRobot):
            gameRobot.reset()
            print("___________________________________")
            print("Push enter when the board is ready..")
            input("")

        currentPlayerId = random.randint(0, 1)

        while (game.isFinished(players[currentPlayerId].getColor()) != True):
            currentPlayer = players[currentPlayerId]

            if (currentPlayer.needDisplay() == True):
                game.getBoard(currentPlayer.getColor()).display()

            # We request the pawns to played and the mouvement wanted
            availableMovements = game.getAvailableMovementForAllPawns(currentPlayer.getColor())
            validPawns = game.pawnsCanBePlayed(availableMovements)
            x,y=currentPlayer.getPawnWanted(validPawns,game.getBoard(currentPlayer.getColor()), availableMovements)
            movementsValid = game.movementsValid((x,y),availableMovements)
            finalMovement = game.getFinalMovement(movementsValid)


            movement = currentPlayer.getMovementWanted(finalMovement, movementsValid, game.getBoard(currentPlayer.getColor()))


            # We figure out the current player's score
            prevPrevReward = prevPrevScore - prevScore
            prevPrevScore = prevScore

            if (learn):
                if (game.isFinished(players[(currentPlayerId + 1) % 2].getColor()) == True):
                    prevPrevReward += 3

                 # We figure out the rewards of the previous movement of the current player
                currentPlayer.setReward(prevPrevReward)

            # Do the mouvement and return the score
            jumpedPawns, prevScore ,goToKing= game.setMovement((x,y),currentPlayer.getColor(),movement)


            if (currentPlayer.getColor() == pl.Player.RED and gameRobot != None):
                gameRobot.movePawn((x,y),jumpedPawns,goToKing,movement,game.getBoard(currentPlayer.getColor()))


            currentPlayerId =(currentPlayerId +1) % 2

        if (currentPlayer.getColor() == pl.Player.RED):
            redWins+=1
        else:
            blueWins+=1
        
        # We give the reward for the loosing player
        if (learn):
            loosePlayer = players[(currentPlayerId + 1) % 2]
            loosePlayer.setReward(-3 - prevScore, game.getBoard(loosePlayer.getColor()))
        
        if (playerRedType == pl.PlayerType.HUMAN_TERMINAL or playerBlueType == pl.PlayerType.HUMAN_TERMINAL):
            print("-------------------Game finish------------------")
            game.getBoard(0).display()
            print("------------------------------------------------")
            
        if (currentPlayer.getColor() == pl.Player.RED):
            print("-----------RED wins !!-----------")
        else:
            print("-----------BLUE wins !!----------")

        print(party, "Games finished")

        if (showGraph):
            gamesWin.append(redWins)
            gamesWinRatio.append(redWins/party)
            gamesWinLoseDiff.append(redWins-blueWins)
            if (party>NB_GAMES_AVERAGE):
                tmp = NB_GAMES_AVERAGE
                redWinsLast = gamesWin[-NB_GAMES_AVERAGE]
            else:
                tmp = party
                redWinsLast = 0
            gamesWinRatioLastXGames.append((redWins-redWinsLast)/tmp)

            if (party%NB_GAMES_AVERAGE == 0):
                graphShow(axs, gamesWinRatioLastXGames, gamesWinRatio, gamesWinLoseDiff, gamesWin)

        if (learn):
            if (party%250 == 0):
                pawnSelectorModel.saveModel()
                kingMovementModel.saveModel()
                simplePawnMovementModel.saveModel()
                print("Models Saved !")
        game.reset()
        players[0].reset()
        players[1].reset()

    if (learn):
        pawnSelectorModel.saveModel()
        kingMovementModel.saveModel()
        simplePawnMovementModel.saveModel()
    
    print(" ********  Statistiques ******* ")
    print("The red player wins " + str(redWins) + " parties and the blue player wins " +str(blueWins) + " parties")

    if (showGraph):
        graphShow(axs, gamesWinRatioLastXGames, gamesWinRatio, gamesWinLoseDiff, gamesWin)

        input("Push enter to continue and close graphs...")
