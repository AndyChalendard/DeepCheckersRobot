import player as pl
import game as ga
import random


if __name__ == "__main__":
    game = ga.Game()

    players = [pl.Player(pl.Player.RED,pl.PlayerType.RANDOM),pl.Player(pl.Player.BLUE,pl.PlayerType.IA)]
    party = 0

    redWins = 0
    blueWins = 0

    print("********************************************")
    print("New Game")
    print("********************************************")
    reward = 0
    while (party < 30000):
        party= party + 1
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

            jumpedPawns=game.setMovement((x,y),(xmov,ymov),currentPlayer.getColor(),movement)
            reward = len(jumpedPawns) - jumpedPawnsPrev
            jumpedPawnsPrev = len(jumpedPawns)

            currentPlayer.setReward(reward) #we calculate the rewards of the previous movement

            '''
            if (len(jumpedPawns) > 0):
                if (currentPlayer.getColor() == pl.Player.RED):
                    print("Player RED jumped " +str(jumpedPawns))
                else:
                    print("Player BLUE jumped " +str(jumpedPawns))
            '''
            currentPlayerId =(currentPlayerId +1) % 2


        print("-------------------Game finish------------------")
        if (currentPlayer.getColor() == pl.Player.RED):
            redWins+=1
        else:
            blueWins+=1
        game.getBoard(0).display()
        print("------------------------------------------------")
        print(" ********  Statistiques ******* ")
        print("The red player wins " + str(redWins) + " parties and the blue player wins " +str(blueWins) + " parties")

        if (currentPlayer.getColor() == pl.Player.RED):
            print("-----------RED wins !!-----------")
        else:
            print("-----------BLUE wins !!----------")
        game.reset()
        players[0].reset()
        players[1].reset()

    players[0].saveModel()
    players[1].saveModel()
