from keras.datasets import mnist
import matplotlib.pyplot as plt
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.utils import np_utils
seed = 7
np.random.seed(seed)

(X_train, y_train), (X_test, y_test) = mnist.load_data()


num_pixels = X_train.shape[1] * X_train.shape[2]
X_train = X_train.reshape(X_train.shape[0], num_pixels).astype("float32") # transforme la matrice de pixels en une
                                                                          # liste de pixels (2D --> 1D)
X_test = X_test.reshape(X_test.shape[0], num_pixels).astype("float32")

X_train = X_train / 255 # normalise les valeurs des pixels
X_test = X_test / 255

y_train = np_utils.to_categorical(y_train) # convertit un n° de classe en un tableau de booléens
                                           # de taille le nombre de classes et avec un 1 à la position
                                           # de la classe en question (fonction indicatrice)
                                           # ex si on a 4 classes : 3 --> [0, 0, 0, 1]
                                           #                        1 --> [0, 1, 0, 0]
y_test = np_utils.to_categorical(y_test)
num_classes = y_test.shape[1]

def baseline_model() :
    model = Sequential() # creation d'un modèle auquel on va ajouter des couches
    # ajout d'une première couche : prend en entrée la liste de pixels, initialise ses poids 'normalement',
    # meme nombre de sorties que d'entrées. La fonction d'activation ('relu') est appliquée sur les combinaisons
    # linéaires des poids ('kernels') et des inputs pour donner les outputs
    model.add(Dense(num_pixels, input_dim = num_pixels, kernel_initializer = "normal", activation = "relu"))
    # il n'y a besoin de préciser l'input size qu'une fois, après Keras sait
    # deuxième et dernière couche : prédit la classe (en output)
    model.add(Dense(num_classes, kernel_initializer = "normal", activation = "softmax"))
    # compile le modèle : on lui passe les métriques à calculer, mais surtout la fonction d'optimisation
    # (comment la descente de gradient est faite) et la fonction de coût à optimiser
    model.compile(loss = "categorical_crossentropy", optimizer = "adam", metrics = ["accuracy"])

    return model

model = baseline_model()
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=10, batch_size=200, verbose=2)
scores = model.evaluate(X_test,y_test, verbose=0)
print(scores[1])