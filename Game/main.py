import player as pl
import game as ga
import random


if __name__ == "__main__":
    game = ga.Game()

    players = [pl.Player(pl.Player.RED,pl.PlayerType.IA),pl.Player(pl.Player.BLUE,pl.PlayerType.IA)]
    party = 0

    print("********************************************")
    print("New Game")
    print("********************************************")
    while (party < 500):
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
            print("WANTS : " +str((x,y)) )

            movementsValid = game.movementsValid((x,y),availableMovements)
            xmov,ymov = currentPlayer.getMovementWanted(movementsValid, game.getBoard(currentPlayer.getColor()))
            
            
            if (currentPlayer.getColor() == pl.Player.RED):
                print("RED move " +str((x,y)) + " to " + str((xmov,ymov)))
            else:
                print("BLUE move " +str((x,y)) + " to " + str((xmov,ymov)))
            
            for mvt in movementsValid:
                if (mvt[len(mvt) - 1] == (xmov,ymov)):
                    movement = mvt

            jumpedPawns=game.setMovement((x,y),(xmov,ymov),currentPlayer.getColor(),movement)
            reward = len(jumpedPawns) - jumpedPawnsPrev
            jumpedPawnsPrev = len(jumpedPawns)
            currentPlayer.setReward(reward, game.getBoard(currentPlayer.getColor()), validPawns)

            if (len(jumpedPawns) > 0):
                if (currentPlayer.getColor() == pl.Player.RED):
                    print("Player RED jumped " +str(jumpedPawns))
                else:
                    print("Player BLUE jumped " +str(jumpedPawns))

            currentPlayerId =(currentPlayerId +1) % 2

        
        print("-------------------Game finish------------------")
        game.getBoard(0).display()
        print("------------------------------------------------")

        if (currentPlayer.getColor() == pl.Player.RED):
            print("-----------RED wins !!-----------")
        else:
            print("-----------BLUE wins !!----------")
        game.reset()
    players[0].saveModel()
    players[1].saveModel()






            




