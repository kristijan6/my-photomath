from data_loader import DataLoader
from postifx_calc import Calculator
import tensorflow as tf
import numpy as np

class Model():
    def __init__(self, train_new_model=False):
        self.class_names = ["0", "1", "2", "3", "4", "5", "6", "7", 
                            "8", "9", "(", ")", "*", "/", "+", "-"]
        self.data_loader = DataLoader()
        self.calculator = Calculator()
        
        if train_new_model:
            self.train_model()
        else:
            self.model = tf.keras.models.load_model('saved_model/latest_model')
            self.probability_model = tf.keras.Sequential([self.model, tf.keras.layers.Softmax()])

    def train_model(self):
        X_train, y_train = data_loader.load_data("train_data/")
        X_test, y_test = data_loader.load_data("test_data/")
        
        self.model = tf.keras.Sequential([
            # Unstacking rows of pixels in the image and lining them up
            tf.keras.layers.Flatten(input_shape=(32,32)),
            tf.keras.layers.Dense(128, activation='relu'),
            tf.keras.layers.Dense(16)
        ])
        
        self.model.compile(
            optimizer='adam',
            loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
            metrics=['accuracy']
        )
        
        self.model.fit(X_train, y_train, epochs=20, verbose=True)
        self.probability_model = tf.keras.Sequential([self.model, tf.keras.layers.Softmax()])
        
        test_loss, test_acc = self.model.evaluate(X_test, y_test, verbose=False)
        print("Accuracy on test set: {}".format(test_acc))
        
    def apply_model(self, image_path):
        self.data_loader.prepare_input(image_path)
        data = self.data_loader.get_input()
        predictions = self.probability_model.predict(data)

        expression = "".join([self.class_names[np.argmax(p)] for p in predictions])
        try:
            print("Recognized expression: {}".format(expression))
            result = self.calculator.calculate(expression)
            print("Result: {}".format(result))
        except:
            print("Couldn't calculate that expression.")
            
    def save_model(self):
        self.model.save('saved_model/latest_model')