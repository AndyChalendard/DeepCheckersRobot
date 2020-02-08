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
    from keras.models import model_from_json
else: # Classic use
    import tensorflow.keras as tk
    from tensorflow.keras.layers import Input, Dense, Activation,Lambda,Flatten,Dropout
    from tensorflow.keras.layers import Conv2D
    from tensorflow.keras.layers import MaxPooling2D
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.optimizers import Adam
    from tensorflow.keras.models import model_from_json


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

        self._pathModel = '../Models/'
        if (os.path.exists(self._pathModel) == False):
            os.mkdir(self._pathModel)
        
        self._pathModel += _nomModel

        if (os.path.exists(self._pathModel+'.h5') and  os.path.exists(self._pathModel+'.json')):
            # Load the model
            json_file = open(self._pathModel+'.json', 'r')
            loaded_model_json = json_file.read()
            json_file.close()
            self._model = model_from_json(loaded_model_json)
            # Load the weights
            self._model.load_weights(self._pathModel+'.h5')
        else:
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
        # Save of the model
        model_json = self._model.to_json()
        with open(self._pathModel+'.json', "w") as json_file:
            json_file.write(model_json)

        # Save of the weights
        self._model.save_weights(self._pathModel+'.h5')


    def trainModel(self, xTrain, yTrain, batchSize = 1, numEpoch = 3):
        '''
        Train the model, return the history of the epoch
        '''
        xTrain = np.array([[xTrain]], dtype=np.float32)
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

    def __init__ (self, sizeX, sizeY, pawnSelectorModel, kingMovementModel, simplePawnModel, learn, epsilon=0.1, alpha=0.1, gamma=0.9 ):
        '''
        Epsilon: chance of random exploration (epsilon greedy algorithm)
        Alpha: discount factor for futur action (for the qfunction)
        Gamma: the weight of the rewards (if gamma=1 ; the reward is also important than an other)
        '''
        self._epsilon = epsilon
        self._alpha = alpha
        self._gamma = gamma

        self._learn = learn
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
            if (self._learn == True):
                self._prevXPawnWanted, self._prevYPawnWanted = random.choice(availablePawn) #exploration
            else:
                output = self._pawnSelectorModel.predictModel(board.getBoard()) #use the model
                self._prevXPawnWanted, self._prevYPawnWanted = self._searchMax(board, output,availablePawn,nbMax = 2)
        else: #exploitation
            output = self._pawnSelectorModel.predictModel(board.getBoard()) #use the model
            self._prevXPawnWanted, self._prevYPawnWanted = self._searchMax(board, output,availablePawn)
        return self._prevXPawnWanted, self._prevYPawnWanted

    def _searchMax(self, board, output, availableList, nbMax=1):
        '''
        Search the Max of a list and return (x,y) with the probability max
        nbMax = 1 : return the max
        nbMax = 2 : return the second Max
        '''
        max = -1
        prevX = -1
        prevY = -1
        for elt in availableList:
            x = elt[0]//2
            y = elt[1]
            index = x*(board.SIZE_X//2) + y
            if (max < output[0][index]):
                max = output[0][index]
                prevX = elt[0]
                prevY = elt[1]
        if (nbMax >= 2):
            index = (prevX//2)*(board.SIZE_X//2) + prevY
            output[0][index] = -1
            prevX, prevY = self._searchMax(board, output, availableList, nbMax-1)
        return prevX, prevY

    def _learnModel(self, modelToLearn, action, reward):
        '''
        Private : template of the Q-function for a modeltolearn
        '''
        prevQ = modelToLearn.predictModel(self._prevPrevBoard.getBoard())
        newQ = modelToLearn.predictModel(self._prevBoard.getBoard())
        maxNewQ = max(newQ[0])

        indiceAction = (action[0]//2) * (self._prevBoard.SIZE_X//2) + action[1]
        prevQ[0][indiceAction] += self._alpha * ( (reward + self._gamma * maxNewQ) - prevQ[0][indiceAction])
        
        # get prevQ Normalized
        prevQSum = np.sum(prevQ)
        if (prevQSum != 0):
            prevQ = prevQ / prevQSum

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

        if (board.getSquare(self._prevXPawnWanted,self._prevYPawnWanted) == bd.Pawns.RED_KING):
                output = self._kingMovementModel.predictModel(board.getBoard()) #use kingMovement model
        elif(board.getSquare(self._prevXPawnWanted,self._prevYPawnWanted) == bd.Pawns.RED):
            output = self._simplePawnMovementModel.predictModel(board.getBoard()) #use simplePawnMovement model
        if (random.random() < self._epsilon):
            if (self._learn == True):
                self._prevXMouvementWanted, self._prevYMouvementWanted = random.choice(finalMovement) #exploration
            else : 
                self._prevXMouvementWanted, self._prevYMouvementWanted = self._searchMax(board, output,finalMovement,2)
        else: #exploitation
            self._prevXMouvementWanted, self._prevYMouvementWanted = self._searchMax(board, output,finalMovement)
        print (output)
        print(self._prevXMouvementWanted//2*(board.SIZE_X//2)+ self._prevYMouvementWanted)
        return self._prevXMouvementWanted, self._prevYMouvementWanted
