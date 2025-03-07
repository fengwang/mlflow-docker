import numpy as np
from tensorflow import keras
from tensorflow.keras.datasets import reuters
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation
from tensorflow.keras.preprocessing.text import Tokenizer

import mlflow
mlflow.set_tracking_uri('http://123.3.2.1:5000') ## <-- change the ip address here
#mlflow.set_tracking_uri('http://mlflow.local:5000') ## <-- change the ip address here
mlflow.tensorflow.autolog()

max_words = 1000
batch_size = 32
epochs = 5

(x_train, y_train), (x_test, y_test) = reuters.load_data(num_words=max_words, test_split=0.2)

print(len(x_train), "train sequences")
print(len(x_test), "test sequences")

num_classes = np.max(y_train) + 1

tokenizer = Tokenizer(num_words=max_words)
x_train = tokenizer.sequences_to_matrix(x_train, mode="binary")
x_test = tokenizer.sequences_to_matrix(x_test, mode="binary")

y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)

model = Sequential()
model.add(Dense(512, input_shape=(max_words,)))
model.add(Activation("relu"))
model.add(Dropout(0.5))
model.add(Dense(num_classes))
model.add(Activation("softmax"))

model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

history = model.fit( x_train, y_train, batch_size=batch_size, epochs=epochs, verbose=1, validation_split=0.1)
score = model.evaluate(x_test, y_test, batch_size=batch_size, verbose=1)
print("Test score:", score[0])
print("Test accuracy:", score[1])

