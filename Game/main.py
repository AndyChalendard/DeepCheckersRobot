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
    game = ga.Game()

    sizeX = game.getBoard(pl.Player.BLUE).SIZE_X
    sizeY = game.getBoard(pl.Player.BLUE).SIZE_Y

    
    NB_GAMES_AVERAGE = 50

    print("___________________________________")
    print("Type of player:")
    print(pl.PlayerType.HUMAN_TERMINAL, ") Terminal")
    print(pl.PlayerType.IA, ") AI")
    print(pl.PlayerType.RANDOM, ") Random")
    print("")
    playerRedType = int(input("Type of player red: "))
    playerBlueType = int(input("Type of player blue: "))

    print("___________________________________")
    print("Number of game wanted")
    nbGamesMax = int(input(">"))

    learn = False
    if (playerRedType == pl.PlayerType.IA or playerBlueType == pl.PlayerType.IA):
        print("___________________________________")
        print("AI must learn during these games ? (y/N)")
        response = input(">")
        if (response == "y" or response == "Y"):
            learn = True


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

    pawnSelectorModel = None
    kingMovementModel = None
    simplePawnMovementModel = None
    if (playerRedType == pl.PlayerType.IA or playerBlueType == pl.PlayerType.IA):
        pawnSelectorModel = mod.CheckersModel(mod.Mod.PAWN_SELECTOR, sizeX,sizeY)
        kingMovementModel = mod.CheckersModel(mod.Mod.KING_MOVEMENT, sizeX,sizeY)
        simplePawnMovementModel = mod.CheckersModel(mod.Mod.SIMPLE_PAWN_MOVEMENT, sizeX,sizeY)

    players = [pl.Player(pl.Player.RED,playerRedType,sizeX, sizeY, pawnSelectorModel, kingMovementModel, simplePawnMovementModel),pl.Player(pl.Player.BLUE, playerBlueType,sizeX, sizeY, pawnSelectorModel, kingMovementModel, simplePawnMovementModel)]
    party = 0

    redWins = 0
    blueWins = 0

    print("********************************************")
    print("New Game")
    print("********************************************")
    reward = 0
    while (party < nbGamesMax):
        party= party + 1

        jumpedPawns = []
        jumpedPawnsPrev = 0

        currentPlayerId = random.randint(0, 1)

        while (game.isFinished() != True):
            currentPlayer = players[currentPlayerId]

            if (currentPlayer.needDisplay() == True):
                game.getBoard(currentPlayer.getColor()).display()


            availableMovements = game.getAvailableMovementForAllPawns(currentPlayer.getColor())
            validPawns = game.pawnsCanBePlayed(availableMovements)
            x,y=currentPlayer.getPawnWanted(validPawns,game.getBoard(currentPlayer.getColor()))
            movementsValid = game.movementsValid((x,y),availableMovements)
            finalMovement = game.getFinalMovement(movementsValid)


            xmov,ymov = currentPlayer.getMovementWanted(finalMovement, game.getBoard(currentPlayer.getColor()))

            '''
            if (currentPlayer.getColor() == pl.Player.RED):
                print("RED move " +str((x,y)) + " to " + str((xmov,ymov)))
            else:
                print("BLUE move " +str((x,y)) + " to " + str((xmov,ymov)))
            '''
            for mvt in movementsValid:
                if (mvt[len(mvt) - 1] == (xmov,ymov)):
                    movement = mvt

            reward = jumpedPawnsPrev - len(jumpedPawns)
            jumpedPawnsPrev = len(jumpedPawns)

            if (learn):
                currentPlayer.setReward(reward) #we calculate the rewards of the previous movement

            jumpedPawns=game.setMovement((x,y),(xmov,ymov),currentPlayer.getColor(),movement)

            '''
            if (len(jumpedPawns) > 0):
                if (currentPlayer.getColor() == pl.Player.RED):
                    print("Player RED jumped " +str(jumpedPawns))
                else:
                    print("Player BLUE jumped " +str(jumpedPawns))
            '''
            currentPlayerId =(currentPlayerId +1) % 2

        if (currentPlayer.getColor() == pl.Player.RED):
            redWins+=1
        else:
            blueWins+=1
        
        if (playerRedType == pl.PlayerType.HUMAN_TERMINAL or playerBlueType == pl.PlayerType.HUMAN_TERMINAL):
            print("-------------------Game finish------------------")
            game.getBoard(0).display()
            print("------------------------------------------------")
            
        if (currentPlayer.getColor() == pl.Player.RED):
            print("-----------RED wins !!-----------")
        else:
            print("-----------BLUE wins !!----------")

        if (graphShow):
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

        game.reset()
        players[0].reset()
        players[1].reset()

    if (learn):
        pawnSelectorModel.saveModel()
        kingMovementModel.saveModel()
        simplePawnMovementModel.saveModel()
    
    print(" ********  Statistiques ******* ")
    print("The red player wins " + str(redWins) + " parties and the blue player wins " +str(blueWins) + " parties")

    if (graphShow):
        graphShow(axs, gamesWinRatioLastXGames, gamesWinRatio, gamesWinLoseDiff, gamesWin)

        input("Push enter to continue and close graphs...")
