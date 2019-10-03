# -*- coding: utf-8 -*-

import keras   #mainly using keras for training model frame
import os
import numpy as np
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Conv2D,MaxPooling2D,Dropout,Flatten,Dense #,BatchNormalization
from keras.utils.vis_utils import plot_model
from keras.optimizers import Adam
from keras.models import load_model

########################
# Some hyperparameters #
########################

epochs = 1000
batch_size = 128
learningrate = 0.005

trainsize = 945 + 1373
testsize = 253 + 409
valsize = 143 + 188
#

##################
# Data generator #
##################


#rescale nomralize it for 0-1 keras.io image processing definition

train_datagen = ImageDataGenerator(rescale=1/255,rotation_range=30,width_shift_range=0.2,
                                   height_shift_range=0.2,shear_range=0.2,zoom_range=0.5,
                                   cval=0,horizontal_flip=True,vertical_flip=True)

val_datagen = ImageDataGenerator(rescale=1/255)
test_datagen = ImageDataGenerator(rescale=1/255)
#train_datagen = ImageDataGenerator()
#
#val_datagen = ImageDataGenerator()
# evaluate the epochs-period 

train_generator = train_datagen.flow_from_directory('./data/train/',
                                                    target_size=(150,150),
                                                    batch_size=batch_size,
                                                    class_mode='categorical')

validation_generator = val_datagen.flow_from_directory('./data/val/',
                                                       target_size=(150,150),
                                                       batch_size=batch_size,
                                                       class_mode='categorical')

test_generator = test_datagen.flow_from_directory('./data/test/',
                                                       target_size=(150,150),
                                                       batch_size=1,
                                                       class_mode=None,
                                                       shuffle=False)
####################################
# Building model sequence (Layers) #
####################################

# Sequencial model

model = Sequential()

# 1-Convolution+Pooling:

model.add(Conv2D(input_shape=(150,150,3), filters=32, kernel_size=(3,3), 
                 padding="same", use_bias=False, kernel_initializer="uniform",
                 data_format="channels_last", activation='relu'))
#model.add(BatchNormalization())

model.add(MaxPooling2D(pool_size=(2,2),padding='same',
                       data_format="channels_last"))
#model.add(BatchNormalization())

# 2-Convolution+Pooling:
model.add(Conv2D(filters=32, kernel_size=(3,3), padding="same", use_bias=False, 
                 kernel_initializer="uniform",data_format="channels_last",
                 activation='relu'))
#model.add(BatchNormalization())

model.add(MaxPooling2D(pool_size=(2,2),padding='same',
                       data_format="channels_last"))
#model.add(BatchNormalization())

# 3-Convolution+Pooling:
model.add(Conv2D(filters=64, kernel_size=(3,3), padding="same", use_bias=False, 
                 kernel_initializer="uniform",data_format="channels_last",
                 activation='relu'))
#model.add(BatchNormalization())

model.add(MaxPooling2D(pool_size=(2,2),padding='same',
                       data_format="channels_last"))
#model.add(BatchNormalization())

# 4-Dropout

model.add(Dropout(0.25))
# dropout some links

# 5-Flatten

model.add(Flatten())
#expand it into a long vector

# 6-Dense

model.add(Dense(units=64, activation="relu"))
#model.add(BatchNormalization())
#fully connnection layer  units= dots 



# 7-Dropout
model.add(Dropout(0.5))


# 8-Dense-output
model.add(Dense(units=2,activation='softmax'))


#######################
# Model visualization #
#######################


plot_model(model, to_file="chongcaoVSrenshen1.png", show_shapes=True)

###################
# Model compiling #
###################

# 1-Instantiating the optimizer
#stochastic gradient descent
#from keras.optimizers import SGD
#sgd = SGD(lr=learningrate, decay=1e-6, momentum=0.9, nesterov=True)

adam = Adam(lr=learningrate)



# 2-Model compiling
#model.compile(loss="mean_squared_error", optimizer="sgd", metrics=["accuracy"])
model.compile(loss=keras.losses.binary_crossentropy, optimizer="adam", 
              metrics=["accuracy"])

######################
## Callback function #
######################
#from keras.callbacks import Callback

checkpoint = keras.callbacks.ModelCheckpoint("chongcaoVSrenshen_best.hdf5", monitor='val_acc',
                                verbose=1, save_best_only=True, mode='max', period=1)
## Callback for loss logging per epoch
#class LossHistory(Callback):
#    def on_train_begin(self, logs={}):
#        self.losses = []
#        self.val_losses = []
#        
#    def on_epoch_end(self, batch, logs={}):
#        self.losses.append(logs.get('loss'))
#        self.val_losses.append(logs.get('val_loss'))
#        
#history = LossHistory()

# Callback for early stopping the training

#early_stopping = keras.callbacks.EarlyStopping(monitor='val_loss', min_delta=0,
#                                               patience=3,verbose=0,mode='auto')

#mode=min



#################
# Model fitting #
#################

fit_model = model.fit_generator(train_generator,
                                steps_per_epoch = trainsize//batch_size,
                                epochs=epochs,
                                validation_data=validation_generator,
                                validation_steps = valsize//batch_size,
                                verbose=1,
                                callbacks=[checkpoint]
                                )
model.save("chongcaoVSrenshen.hdf5")


#####################
## Continue fitting #
#####################
#fit_model2 = model.fit_generator(train_generator,
#                                steps_per_epoch = int(n*(1-ratio))//batch_size,
#                                epochs=epochs,
#                                validation_data=validation_generator,
#                                validation_steps = int(n*(1-ratio))//batch_size,
#                                verbose=1
#                                )
# F9 run current lines



###############
## Prediction #
###############

cwwd = os.getcwd()
filepath = cwwd + '\chongcaoVSrenshen.hdf5'
model = load_model(filepath)


predict_prob = model.predict_generator(test_generator,
                                       steps = testsize,
                                       verbose=1)
predict_labels = np.argmax(predict_prob,axis=1).astype(int)

test_labels = np.ones((testsize)).astype(int)
for i in range(0,253):
    test_labels[i] = 0
    
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
print(classification_report(test_labels, predict_labels))
print(accuracy_score(test_labels, predict_labels))
confmatrix = confusion_matrix(test_labels, predict_labels)
print(confmatrix)
########################
# Result visualization #
########################

import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

plt.figure(1)
plt.plot(fit_model.history['acc'])
plt.plot(fit_model.history['val_acc'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epochs')
plt.legend(['train','test'],loc='upper left')
#train=acc ;test=val_acc
#loc= 左上角的小框框

plt.savefig('Model_Accuracy.jpg')
plt.show()

plt.figure(2)
plt.plot(fit_model.history['loss'])
plt.plot(fit_model.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epochs')
plt.legend(['train','test'],loc='upper left')
plt.savefig('Model_Loss.jpg')
plt.show()