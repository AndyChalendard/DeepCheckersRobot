import board as bd
import os.path
import random
import numpy as np
import tensorflow

if (str(tensorflow.__version__) == "1.8.0"): # Use for GPU training (with tensorflow 1.8)
    import keras as tk
    from keras.layers import Input, Dense, Activation,Lambda,Flatten,Dropout
    from keras.layers import Conv2D
    from keras.layers import MaxPooling2D
    from keras.models import Sequential
    from keras.optimizers import Adam
else: # Classic use
    import tensorflow.keras as tk
    from tensorflow.keras.layers import Input, Dense, Activation,Lambda,Flatten,Dropout
    from tensorflow.keras.layers import Conv2D
    from tensorflow.keras.layers import MaxPooling2D
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.optimizers import Adam


class Mod:
    PAWN_SELECTOR = 0 #Selection of the pawn that we want to play with
    KING_MOVEMENT = 1 #Selection of the movement done by the king pawn
    SIMPLE_PAWN_MOVEMENT = 2 #Selection of the movement done by the simple pawn


class CheckersModel :
    def __init__ (self,idModel,sizeX,sizeY,kernelSize = (3,3),learningRate = 0.0001):
        '''
        Creation of the model or load the model
        '''
        self._idModel = idModel
        self._learningRate = learningRate
        if (self._idModel == Mod.PAWN_SELECTOR):
            _nomModel = 'pawn_selector'
        elif (self._idModel == Mod.KING_MOVEMENT):
            _nomModel = 'king_movement'
        else:
            _nomModel = 'simple_pawn_movement'

        self._pathModel = '../ModelsWeights/'
        if (os.path.exists(self._pathModel) == False):
            os.mkdir(self._pathModel)

        self._pathModel += _nomModel

        self._model = Sequential()
        inputShape = (1, sizeY, sizeX//2)
        numOutput = sizeX//2 * sizeY

        self._model.add(Conv2D(128, kernel_size=(6,3), strides = (1,1), padding='same', activation='relu',input_shape=inputShape,name='Conv1'))
        self._model.add(Conv2D(64, kernel_size=(4,2), strides = (1,1), padding='same', activation='relu',name='Conv2'))
        self._model.add(Conv2D(16, kernel_size=(4,2), strides = (1,1), padding='same', activation='relu',name='Conv3'))
        self._model.add(Flatten(name='Flatten'))
        self._model.add(Dense(128, activation='relu',name='Dense1'))
        self._model.add(Dense(numOutput, activation='softmax',name='DenseOutput'))
        adam = Adam(lr=self._learningRate)
        self._model.compile(loss=tk.losses.categorical_crossentropy,optimizer=adam,metrics=['acc'])

        if os.path.exists(self._pathModel): # we load the weights if they exist
            self._model.load_weights(self._pathModel)

        self._model.summary()

    def getModel(self):
        '''
        Return the model
        '''
        return self._model

    def saveModel(self):
        '''
        Save the model to a futur use
        '''
        self._model.save_weights(self._pathModel)

    def trainModel(self, xTrain, yTrain, batchSize = 1, numEpoch = 3):
        '''
        Train the model, return the history of the epoch
        '''
        xTrain = np.array([[xTrain]], dtype=np.float32)
        #yTrain = np.array([[yTrain]], dtype=np.float64)
        history = self._model.fit(xTrain, yTrain, batch_size=batchSize, epochs=numEpoch, verbose=0)
        return history

    def predictModel(self,x):
        '''
        Use the model to predict the output
        x: board
        y: flatten board
        '''
        x = np.array([[x]], dtype=np.float32)
        y = self._model.predict(x)
        return y

class IA :

    def __init__ (self, sizeX, sizeY, pawnSelectorModel, kingMovementModel, simplePawnModel, epsilon=0.1, alpha=0.1, gamma=0.9, ):
        '''
        Epsilon: chance of random exploration (epsilon greedy algorithm)
        Alpha: discount factor for futur action (for the qfunction)
        Gamma: the weight of the rewards (if gamma=1 ; the reward is also important than an other)
        '''
        self._epsilon = epsilon
        self._alpha = alpha
        self._gamma = gamma

        self._prevBoard = None
        self._prevPrevBoard = None
        self._prevAvailablePawn = None
        self._pawnSelectorModel = pawnSelectorModel
        self._kingMovementModel = kingMovementModel
        self._simplePawnMovementModel = simplePawnModel

        self._prevXPawnWanted = None
        self._prevYPawnWanted = None
        self._prevPrevXPawnWanted = None
        self._prevPrevYPawnWanted = None

        self._prevXMouvementWanted = None
        self._prevYMouvementWanted = None
        self._prevPrevXMouvementWanted = None
        self._prevPrevYMouvementWanted = None

    def resetIA(self):
        '''
        Reset all attributes of the IA
        '''
        self._prevBoard = None
        self._prevPrevBoard = None
        self._prevAvailablePawn = None

        self._prevXPawnWanted = None
        self._prevYPawnWanted = None
        self._prevPrevXPawnWanted = None
        self._prevPrevYPawnWanted = None

        self._prevXMouvementWanted = None
        self._prevYMouvementWanted = None
        self._prevPrevXMouvementWanted = None
        self._prevPrevYMouvementWanted = None

    def getPawnWanted(self, board, availablePawn):
        '''
        Return (x,y) the pawn to play with
        We use the model for exploitation and random for exploration
        '''
        self._prevAvailablePawn = availablePawn

        self._prevPrevXPawnWanted = self._prevXPawnWanted
        self._prevPrevYPawnWanted = self._prevYPawnWanted
        if (random.random() < self._epsilon):
            self._prevXPawnWanted, self._prevYPawnWanted = random.choice(availablePawn) #exploration
        else: #exploitation
            output = self._pawnSelectorModel.predictModel(board.getBoard()) #use the model
            max = -1
            self._prevXPawnWanted = -1
            self._prevYPawnWanted = -1
            for pawn in availablePawn:
                xPawn = pawn[0]//2
                yPawn = pawn[1]
                index = xPawn*(board.SIZE_X//2) + yPawn
                if (max < output[0][index]):
                    max = output[0][index]
                    self._prevXPawnWanted = pawn[0]
                    self._prevYPawnWanted = pawn[1]

        return self._prevXPawnWanted, self._prevYPawnWanted

    def _learnModel(self, modelToLearn, action, reward):
        '''
        Private : template of the Q-function for a modeltolearn
        '''
        prevQ = modelToLearn.predictModel(self._prevPrevBoard.getBoard())
        newQ = modelToLearn.predictModel(self._prevBoard.getBoard())
        maxNewQ = max(newQ[0])

        indiceAction = (action[0]//2) * (self._prevBoard.SIZE_X//2) + action[1]
        prevQ[0][indiceAction] += self._alpha * ( (reward + self._gamma * maxNewQ) - prevQ[0][indiceAction])
        modelToLearn.trainModel(self._prevPrevBoard.getBoard(),prevQ)

    def learn(self, reward, currentBoard = None):
        '''
        We learn action and theirs reward. 
        The value of currentBoard permits to learn in the end of the game (when the AI has no pawn to played)
        '''
        if (currentBoard != None):
            self._prevPrevBoard = self._prevBoard
            self._prevBoard = currentBoard.copy()

            self._prevPrevXPawnWanted = self._prevXPawnWanted
            self._prevPrevYPawnWanted = self._prevYPawnWanted

            self._prevPrevXMouvementWanted = self._prevXMouvementWanted
            self._prevPrevYMouvementWanted = self._prevYMouvementWanted

        if self._prevPrevBoard:
            #Learn for pawnSelector
            self._learnModel(self._pawnSelectorModel, (self._prevPrevXPawnWanted, self._prevPrevYPawnWanted), reward)

            #Learn for KingMovements
            if (self._prevPrevBoard.getSquare(self._prevPrevXPawnWanted,self._prevPrevYPawnWanted) == bd.Pawns.RED_KING):
                self._learnModel(self._kingMovementModel, (self._prevPrevXMouvementWanted, self._prevPrevYMouvementWanted), reward)

            #Learn for SimpleMovements
            elif (self._prevPrevBoard.getSquare(self._prevPrevXPawnWanted,self._prevPrevYPawnWanted) == bd.Pawns.RED):
                self._learnModel(self._simplePawnMovementModel, (self._prevPrevXMouvementWanted, self._prevPrevYMouvementWanted), reward)

        if (currentBoard != None):
            self.resetIA()

        self._prevPrevBoard = None

    def getMovementWanted(self, board, finalMovement):
        '''
        Return (x,y) the square of the movement
        Exploitation use the model of the neural network
        Exploration :  random
        '''
        self._prevPrevXMouvementWanted = self._prevXMouvementWanted
        self._prevPrevYMouvementWanted = self._prevYMouvementWanted
        self._prevPrevBoard = self._prevBoard
        self._prevBoard = board.copy()
        if (random.random() < self._epsilon):
            self._prevXMouvementWanted, self._prevYMouvementWanted = random.choice(finalMovement) #exploration
        else: #exploitation
            if (board.getSquare(self._prevXPawnWanted,self._prevYPawnWanted) == bd.Pawns.RED_KING):
                output = self._kingMovementModel.predictModel(board.getBoard()) #use kingMovement model
            elif(board.getSquare(self._prevXPawnWanted,self._prevYPawnWanted) == bd.Pawns.RED):
                output = self._simplePawnMovementModel.predictModel(board.getBoard()) #use simplePawnMovement model
            max = -1
            self._prevXMouvementWanted = -1
            self._prevYMouvementWanted = -1
            for mov in finalMovement:
                xMov = mov[0]//2
                yMov = mov[1]
                index = xMov*4 + yMov
                if (max < output[0][index]):
                    max = output[0][index]
                    self._prevXMouvementWanted = mov[0]
                    self._prevYMouvementWanted = mov[1]

        return self._prevXMouvementWanted, self._prevYMouvementWanted
