import keras
import numpy as np
from pond.tensor import NativeTensor, PrivateEncodedTensor, PublicEncodedTensor
from pond.nn import Dense, ReluExact, Relu, Reveal, CrossEntropy, SoftmaxStable, \
    Sequential, DataLoader, Conv2D, AveragePooling2D, Flatten
from keras.utils import to_categorical
np.random.seed(42)
import datetime

# Read data.
(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()
x_train = x_train[:, np.newaxis, :, :] / 255.0
x_test = x_test[:, np.newaxis, :, :] / 255.0
y_train = to_categorical(y_train, 10)
y_test = to_categorical(y_test, 10)

_ = np.seterr(over='raise')
_ = np.seterr(under='raise')
_ = np.seterr(invalid='raise')

tensortype = NativeTensor

convnet_shallow = Sequential([
    Flatten(),
    Dense(100, 784),
    ReluExact(),
    Dense(10, 100),
    Reveal(),
    SoftmaxStable()
])

convnet_shallow.initialize()
convnet_shallow.fit(
    x_train=DataLoader(x_train, wrapper=tensortype),
    y_train=DataLoader(y_train, wrapper=tensortype),
    x_valid=DataLoader(x_test, wrapper=tensortype),
    y_valid=DataLoader(y_test, wrapper=tensortype),
    loss=CrossEntropy(),
    epochs=30,
    batch_size=128,
    verbose=1,
    learning_rate=0.01
)
