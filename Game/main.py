import player as pl
import game as ga
import random


if __name__ == "__main__":
    game = ga.Game()

    players = [pl.Player(pl.Player.BLUE,pl.PlayerType.RANDOM),pl.Player(pl.Player.RED,pl.PlayerType.HUMAN_TERMINAL)]
    currentPlayerId = random.randint(0, 1) 

    while (game.isFinished() != True):
        currentPlayer = players[currentPlayerId]

        if (currentPlayer.needDisplay() == True):
            game.getBoard().display()
        
        availableMovements = game.getAvailableMovementForAllPawns(currentPlayer)
        validPawns = game.pawnsCanBePlayed(availableMovements)
        x,y=currentPlayer.getPawnWanted(validPawns)

        movementsValid = game.movementsValid((x,y),availableMovements)
        xmov,ymov = currentPlayer.getMovementWanted(movementsValid)

        for mvt in movementsValid:
            if (mvt[len(mvt) - 1] == (xmov,ymov)):
                movement = mvt

        jumpedPawns=game.setMovement((x,y),(xmov,ymov),currentPlayer.getColor(),movement)
        if (len(jumpedPawns) > 0):
            print("You jumped " +str(jumpedPawns))
        currentPlayerId =(currentPlayerId +1) % 2
    
    print("-------------------Game finish------------------")
    game.getBoard().display()
    print("------------------------------------------------")






            




