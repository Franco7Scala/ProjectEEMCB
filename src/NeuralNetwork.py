import os
import matplotlib.pyplot as plotter

from keras import losses, optimizers
from keras.initializers import glorot_normal
from keras.models import model_from_json, Sequential
from keras.layers import Dense
from keras.utils import plot_model


class NeuralNetwork:

    def __init__(self):
        self.neural_network = Sequential()

    def create(self, input_size, output_size):
        """
        This function build the neural network
        uses the parameters as input and output size
        """
        # network
        self.neural_network.add(Dense(input_size, input_dim=input_size))
        self.neural_network.add(Dense(units=1024, activation='relu', kernel_initializer=glorot_normal(seed=None)))
        self.neural_network.add(Dense(units=512, activation='relu', kernel_initializer=glorot_normal(seed=None)))
        self.neural_network.add(Dense(units=256, activation='relu', kernel_initializer=glorot_normal(seed=None)))
        self.neural_network.add(Dense(units=128, activation='relu', kernel_initializer=glorot_normal(seed=None)))
        self.neural_network.add(Dense(units=output_size, activation='relu'))
        self.neural_network.compile(optimizer=optimizers.Adam(lr=0.0001), loss=losses.mse, metrics=['accuracy'])

    def load(self, path_network):
        json_file = open(path_network + '/neural_network.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        self.neural_network = model_from_json(loaded_model_json)
        self.neural_network.load_weights(path_network + '/neural_network.h5')
        self.neural_network.compile(optimizer=optimizers.Adam(lr=0.0001), loss=losses.mse, metrics=['accuracy'])

    def save(self, path_network):
        if not os.path.exists(path_network):
            os.makedirs(path_network)
        model_json = self.neural_network.to_json()
        with open(path_network + '/neural_network.json', "w") as json_file:
            json_file.write(model_json)
        self.neural_network.save_weights(path_network + '/neural_network.h5')
        plot_model(self.neural_network, to_file=(path_network + '/neural_network.png'))

    def evaluate(self, data):
        return self.neural_network.predict(data)

    def train(self, training_input, training_output, test_input, test_output, epochs=100, batch_size=32, verbose=0):
        history = self.neural_network.fit(training_input, training_output,
                                          epochs=epochs,
                                          batch_size=batch_size,
                                          shuffle=True,
                                          verbose=1,
                                          validation_data=(test_input, test_output))
        if verbose == 1:
            # summarize history for accuracy
            plotter.plot(history.history['acc'])
            plotter.plot(history.history['val_acc'])
            plotter.title('model accuracy')
            plotter.ylabel('accuracy')
            plotter.xlabel('epoch')
            plotter.legend(['train', 'test'], loc='upper left')
            plotter.show()
            # summarize history for loss
            plotter.plot(history.history['loss'])
            plotter.plot(history.history['val_loss'])
            plotter.title('model loss')
            plotter.ylabel('loss')
            plotter.xlabel('epoch')
            plotter.legend(['train', 'test'], loc='upper left')
            plotter.show()
