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
    def __init__ (self,idModel,sizeX,sizeY,kernelSize = (5,5),learningRate = 0.0001):
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
        if (0) : #os.path.exists(self._pathModel): #load the model TODO
            self._model = tensorflow.keras.models.load_model(self._pathModel)
        else: #create the model
            self._model = Sequential()
            inputShape = (1, sizeY, sizeX//2)
            numOutput = sizeX//2 * sizeY

            self._model.add(Conv2D(64, kernel_size=kernelSize, strides = (1,1), padding='same', activation='relu',input_shape=inputShape,name='Conv1'))
            self._model.add(Conv2D(16, kernel_size=(3,3), strides = (1,1), padding='same', activation='relu',name='Conv2'))
            self._model.add(Flatten(name='Flatten'))
            self._model.add(Dense(128, activation='relu',name='Dense1'))
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
        self._prevPrevBoard = None
        self._prevMove = None
        self._pawnSelectorModel = CheckersModel(Mod.PAWN_SELECTOR, sizeX,sizeY)
        self._kingMovementModel = CheckersModel(Mod.KING_MOVEMENT, sizeX,sizeY)
        self._simplePawnMovementModel = CheckersModel(Mod.SIMPLE_PAWN_MOVEMENT, sizeX,sizeY)

        self._xPawnWanted = None
        self._yPawnWanted = None
        self._xPawnWantedPrec = None
        self._yPawnWantedPrec = None

    def resetIA(self):
        self._prevBoard = None
        self._prevPrevBoard = None
        self._prevMove = None
        self._xPawnWanted = None
        self._yPawnWanted = None
        self._xPawnWantedPrec = None
        self._yPawnWantedPrec = None

    def getPawnWanted(self, board, availablePawn):
        self._xPawnWantedPrec = self._xPawnWanted
        self._yPawnWantedPrec = self._yPawnWanted
        if (random.random() < self._epsilon):
            self._xPawnWanted, self._yPawnWanted = random.choice(availablePawn) #exploration
        else: #exploitation
            output = self._pawnSelectorModel.predictModel(board.getBoard()) #use the model
            max = -1
            self._xPawnWanted = -1
            self._yPawnWanted = -1
            for pawn in availablePawn:
                xPawn = pawn[0]//2
                yPawn = pawn[1]
                index = xPawn*4 + yPawn
                if (max < output[0][index]):
                    max = output[0][index]
                    self._xPawnWanted = pawn[0]
                    self._yPawnWanted = pawn[1]

        return self._xPawnWanted, self._yPawnWanted

    def learn(self, reward, availablePawn, finalMovement):
        if self._prevPrevBoard:
            #Learn for pawnSelector
            prevQPawnSelect = self._pawnSelectorModel.predictModel(self._prevPrevBoard.getBoard())
            newQPawnSelect = self._pawnSelectorModel.predictModel(self._prevBoard.getBoard())
            maxNewQPawnSelect = -1
            for pawn in availablePawn:
                xPawn = pawn[0]//2
                yPawn = pawn[1]
                index = xPawn*4 + yPawn
                if (maxNewQPawnSelect < newQPawnSelect[0][index]):
                    maxNewQPawnSelect = newQPawnSelect[0][index]
            self._pawnSelectorModel.trainModel(self._prevBoard.getBoard(),prevQPawnSelect + self._alpha *((reward + self._gamma * maxNewQPawnSelect)-prevQPawnSelect))

            #Learn for KingMovements
            if (self._prevPrevBoard.getSquare(self._xPawnWantedPrec,self._yPawnWantedPrec) == bd.Pawns.RED_KING):
                prevQKingMovements = self._kingMovementModel.predictModel(self._prevPrevBoard.getBoard())
                newQKingMovements = self._kingMovementModel.predictModel(self._prevBoard.getBoard())
                maxNewQKingMovements = -1
                for mov in finalMovement:
                    xMov = mov[0]//2
                    yMov = mov[1]
                    index = xMov*4 + yMov
                    if (maxNewQKingMovements < newQKingMovements[0][index]):
                        maxNewQKingMovements = newQKingMovements[0][index]
                self._kingMovementModel.trainModel(self._prevBoard.getBoard(),prevQKingMovements + self._alpha *((reward + self._gamma * maxNewQKingMovements)-prevQKingMovements))

            #Learn for SimpleMovements
            elif (self._prevPrevBoard.getSquare(self._xPawnWantedPrec,self._yPawnWantedPrec) == bd.Pawns.RED):
                prevQSimpleMovements = self._simplePawnMovementModel.predictModel(self._prevPrevBoard.getBoard())
                newQSimpleMovements = self._simplePawnMovementModel.predictModel(self._prevBoard.getBoard())
                maxNewQSimpleMovements = -1
                for mov in finalMovement:
                    xMov = mov[0]//2
                    yMov = mov[1]
                    index = xMov*4 + yMov
                    if (maxNewQSimpleMovements < newQSimpleMovements[0][index]):
                        maxNewQSimpleMovements = newQSimpleMovements[0][index]
                self._kingMovementModel.trainModel(self._prevBoard.getBoard(),prevQSimpleMovements + self._alpha *((reward + self._gamma * maxNewQSimpleMovements)-prevQSimpleMovements))

        self._prevPrevBoard = None

    def saveNeuralNetworks(self):
        self._pawnSelectorModel.saveModel()
        self._kingMovementModel.saveModel()
        self._simplePawnMovementModel.saveModel()

    def getMovementWanted(self, board, finalMovement):
        self._prevPrevBoard = self._prevBoard
        self._prevBoard = board.copy()
        if (random.random() < self._epsilon):
            xMovWanted, yMovWanted = random.choice(finalMovement) #exploration
        else: #exploitation
            if (board.getSquare(self._xPawnWanted,self._yPawnWanted) == bd.Pawns.RED_KING):
                output = self._kingMovementModel.predictModel(board.getBoard()) #use kingMovement model
            elif(board.getSquare(self._xPawnWanted,self._yPawnWanted) == bd.Pawns.RED):
                output = self._simplePawnMovementModel.predictModel(board.getBoard()) #use simplePawnMovement model
            max = -1
            xMovWanted = -1
            yMovWanted = -1
            for mov in finalMovement:
                xMov = mov[0]//2
                yMov = mov[1]
                index = xMov*4 + yMov
                if (max < output[0][index]):
                    max = output[0][index]
                    xMovWanted = mov[0]
                    yMovWanted = mov[1]

        return xMovWanted, yMovWanted
