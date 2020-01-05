import board as bd
import os.path
import random
import numpy as np
import tensorflow
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
    def __init__ (self,idModel,sizeX,sizeY,kernelSize = (2,2),learningRate = 0.0001):
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

        self._pathModel = '../Models/model_'+_nomModel+'.h5'
        if (0) : #os.path.exists(self._pathModel): #load the model
            self._model = tensorflow.keras.models.load_model(self._pathModel)
        else: #create the model
            self._model = Sequential()
            inputShape = (1, sizeY, sizeX//2)
            numOutput = sizeX//2 * sizeY

            self._model.add(Conv2D(1, kernel_size=kernelSize, strides = (1,1), padding='same', activation='relu',input_shape=inputShape,name='Conv1'))
            self._model.add(Conv2D(32, kernel_size=kernelSize, strides = (1,1), padding='same', activation='relu',name='Conv2'))
            self._model.add(Flatten(name='Flatten'))
            self._model.add(Dense(64, activation='relu',name='Dense1'))
            self._model.add(Dense(64, activation='relu',name='Dense2'))
            self._model.add(Dense(numOutput, activation='softmax',name='DenseOutput'))
            adam = Adam(lr=self._learningRate)
            self._model.compile(loss=tk.losses.categorical_crossentropy,optimizer=adam,metrics=['acc'])

            self._model.summary()

    def getModel(self):
        return self._model
    def saveModel(self):
        '''
        Save the model to a futur use
        '''
        self._model.save(self._pathModel)
    
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

    def __init__ (self, sizeX, sizeY, epsilon=0.1, alpha=0.3, gamma=0.9):
        '''
        Epsilon: chance of random exploration (epsilon greedy algorithm)
        Alpha: discount factor for futur action (for the qfunction)
        Gamma: the weight of the rewards (if gamma=1 ; the reward is also important than an other)
        '''
        self._epsilon = epsilon
        self._alpha = alpha
        self._gamma = gamma

        self._prevBoard = None
        self._prevMove = None
        self._OldQ = 1
        self._pawnSelectorModel = CheckersModel(Mod.PAWN_SELECTOR, sizeX,sizeY)
        #self._kingMovementModel = CheckersModel(CheckersModel.PAWN_SELECTOR, board) TODO
        #self._simplePawnMovementModel = CheckersModel(CheckersModel.PAWN_SELECTOR, board) TODO

    def getPawnWanted(self, board, availablePawn):
        self._prevBoard = board.copy()
        if (random.random() < self._epsilon):
            xPawnWanted, yPawnWanted = random.choice(availablePawn) #exploration
        else: #exploitation
            output = self._pawnSelectorModel.predictModel(board.getBoard()) #use the model
            max = -1
            xPawnWanted = -1
            yPawnWanted = -1
            for pawn in availablePawn:
                xPawn = pawn[0]//2 
                yPawn = pawn[1]
                index = xPawn*4 + yPawn
                if (max < output[0][index]):
                    max = output[0][index]
                    xPawnWanted = pawn[0]
                    yPawnWanted = pawn[1]
        return xPawnWanted, yPawnWanted

    def learn(self, reward, availablePawn, board):
        if self._prevBoard:
            prevQ = self._pawnSelectorModel.predictModel(self._prevBoard.getBoard())
            newQ = self._pawnSelectorModel.predictModel(board.getBoard())
            maxNewQ = -1
            for pawn in availablePawn:
                xPawn = pawn[0]//2
                yPawn = pawn[1]
                index = xPawn*4 + yPawn
                if (maxNewQ < newQ[0][index]):
                    maxNewQ = newQ[0][index]
            self._pawnSelectorModel.trainModel(board.getBoard(),prevQ + self._alpha *((reward + self._gamma * maxNewQ)-prevQ))
        self._prevBoard = None

    def saveNeuralNetworks(self):
        self._pawnSelectorModel.saveModel()
        #self._kingMovementModel.saveModel()
        #self._simplePawnMovementModel.saveModel()

    def getMovementWanted(self, board, availableMovement):
        mov = random.randint(0, len(availableMovement)-1)
        xMovWanted,yMovWanted = availableMovement[mov]
        return xMovWanted, yMovWanted
