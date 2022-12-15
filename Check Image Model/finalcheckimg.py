# -*- coding: utf-8 -*-
"""FinalCheckimg.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1D9K5FUG2ZwFnhszV1D3pkVLq9ZlTohsz

# Step 1: Mount data from google drive.
"""

from google.colab import drive
drive.mount('/content/drive')

"""# Step 2: Import Libraries."""

# Import Libraries
import os
import glob
import matplotlib.pyplot as plt
import numpy as np

# Keras API
import keras
from keras.models import Sequential
from keras.layers import Dense,Dropout,Flatten
from keras.layers import Conv2D,MaxPooling2D,Activation,AveragePooling2D,BatchNormalization
from keras.preprocessing.image import ImageDataGenerator

"""# Step 3: Unzip data."""

!unzip /content/drive/MyDrive/FinalCheckimg.zip

"""# Step 4: Load train and test data into separate variables."""

train_dir ="/content/FinalCheckimg/train"
test_dir="/content/FinalCheckimg/test"

"""# Step 5: Function to Get count of images in train and test data."""

# function to get count of images
def get_files(directory):
  if not os.path.exists(directory):
    return 0
  count=0
  for current_path,dirs,files in os.walk(directory):
    for dr in dirs:
      count+= len(glob.glob(os.path.join(current_path,dr+"/*")))
  return count

"""# Step 6: View number of images in each."""

train_samples =get_files(train_dir)
num_classes=len(glob.glob(train_dir+"/*"))
test_samples=get_files(test_dir)
print(num_classes,"Classes")
print(train_samples,"Train images")
print(test_samples,"Test images")

"""# Step 7: Pre-processing our raw data into usable format."""

# Pre-processing data with parameters.
train_datagen=ImageDataGenerator(rescale=1./255,
                                   shear_range=0.2,
                                   zoom_range=0.2,
                                   horizontal_flip=True)
test_datagen=ImageDataGenerator(rescale=1./255)

"""# Step 8: Generating augmented data from train and test directories."""

# set height and width and color of input image.
img_width,img_height =256,256
input_shape=(img_width,img_height,3)
batch_size =32

train_generator = train_datagen.flow_from_directory(train_dir,
                                target_size=(img_width,img_height),
                                batch_size=batch_size)

test_generator = test_datagen.flow_from_directory(test_dir,shuffle=False,
                                                target_size=(img_width,img_height),
                                                batch_size=batch_size)

"""# Step 9: Get 2 Image Names/classes."""

# The name of the 2 Image sets.
train_generator.class_indices

"""# Step 10: Building CNN model."""

# CNN building.
model = Sequential()
model.add(Conv2D(32, (5, 5),input_shape=input_shape,activation='relu'))
model.add(MaxPooling2D(pool_size=(3, 3)))
model.add(Conv2D(32, (3, 3),activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(64, (3, 3),activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))   
model.add(Flatten())
model.add(Dense(512,activation='relu'))
model.add(Dropout(0.25))
model.add(Dense(128,activation='relu'))          
model.add(Dense(num_classes,activation='softmax'))
model.summary()

"""**Types of layers**"""

model_layers = [ layer.name for layer in model.layers]
print('layer name : ',model_layers)

"""**Take one image to visualize it's changes after every layer**"""

from keras.preprocessing import image
import numpy as np
img1 = keras.utils.load_img('/content/FinalCheckimg/train/Invalid Image/auditorium (10).jpg')
plt.imshow(img1);

#preprocess image
img1 = keras.utils.load_img('/content/FinalCheckimg/train/Invalid Image/auditorium (10).jpg', target_size=(256, 256))
img = keras.utils.img_to_array(img1)
img = img/255
img = np.expand_dims(img, axis=0)

"""# Step 11: Visualisation of images after every layer."""

# Visualizing output after every layer.
from keras.models import Model
conv2d_output = Model(inputs=model.input,outputs=model.get_layer('conv2d').output)
max_pooling2d_output = Model(inputs=model.input,outputs=model.get_layer('max_pooling2d').output)
conv2d_1_output = Model(inputs=model.input,outputs=model.get_layer('conv2d_1').output)
max_pooling2d_1_output = Model(inputs=model.input,outputs=model.get_layer('max_pooling2d_1').output)
conv2d_2_output = Model(inputs=model.input,outputs=model.get_layer('conv2d_2').output)
max_pooling2d_2_output = Model(inputs=model.input,outputs=model.get_layer('max_pooling2d_2').output)

flatten_output = Model(inputs=model.input,outputs=model.get_layer('flatten').output)

conv2d_features = conv2d_output.predict(img)
max_pooling2d_features = max_pooling2d_output.predict(img)
conv2d_1_features = conv2d_1_output.predict(img)
max_pooling2d_1_features = max_pooling2d_1_output.predict(img)
conv2d_2_features = conv2d_2_output.predict(img)
max_pooling2d_2_features = max_pooling2d_2_output.predict(img)

flatten_features = flatten_output.predict(img)

"""# Step 12: Start Training CNN with Parameters."""

# validation data
validation_generator = train_datagen.flow_from_directory(
                       train_dir, # same directory as training data
                       target_size=(img_height, img_width),
                       batch_size=batch_size)

from tensorflow import keras
# Model building to get trained with parameters.
opt=keras.optimizers.Adam(lr=0.001)
model.compile(optimizer=opt,loss='categorical_crossentropy',metrics=['accuracy'])
train=model.fit_generator(train_generator,
                          epochs = 10,
                          steps_per_epoch=train_generator.samples//batch_size,
                          validation_data = validation_generator, validation_steps = validation_generator.samples // batch_size,verbose=1)

"""# Step 13: Plot For Accuracy And Losses."""

acc = train.history['accuracy']
val_acc = train.history['val_accuracy']
loss = train.history['loss']
val_loss = train.history['val_loss']
epochs = range(1, len(acc) + 1)

#Train and validation accuracy
plt.plot(epochs, acc, 'b', label='Training accurarcy')
plt.plot(epochs, val_acc, 'r', label='Validation accurarcy')
plt.title('Training and Validation accurarcy')
plt.legend()
plt.figure()

#Train and validation loss
plt.plot(epochs, loss, 'b', label='Training loss')
plt.plot(epochs, val_loss, 'r', label='Validation loss')
plt.title('Training and Validation loss')
plt.legend()
plt.show()

"""# Stap 14: Evaluate model using unseen data."""

score,accuracy =model.evaluate(test_generator,verbose=1)
print("Test score is {}".format(score))
print("Test accuracy is {}".format(accuracy))

"""# Step 15: Confusion Matrix."""

predictions= model.predict(test_generator,batch_size=10,verbose=0)

import numpy as np

y_pred = np.rint(predictions)
y_true = test_generator.classes

rounded_labels = np.argmax(y_pred,axis=-1)
rounded_labels[1]

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline
from sklearn.metrics import confusion_matrix, classification_report
import itertools

cm = confusion_matrix(y_true,rounded_labels)

print(classification_report(y_true,rounded_labels))

def plot_confusion_matrix (cm , classes,
                           normalize = False , 
                           title = 'Confusion Matrix' ,
                           #figsize=(20,10), 
                           #fontsize=10, 
                           cmap=plt.cm.Blues):
  plt.imshow(cm,interpolation='nearest',cmap=cmap)
  plt.title(title)
  plt.colorbar()
  #plt.figure(figsize=figsize)
  tick_marks=np.arange(len(classes))
  plt.xticks(tick_marks, classes, rotation=45)
  plt.yticks(tick_marks, classes)



  if normalize:
    cm= cm.astype('float')/cm.sum(axis=1)[:,np.newaxis]
    print("Normalized Confusion Matrix")

  else:
    print('Confusion Matrix,withoutnormalization')

  print(cm)

  thresh=cm.max()/2.
  for i,j in itertools.product(range(cm.shape[0]) , range(cm.shape[1])):
      plt.text(j,i, cm[i , j],
                             horizontalalignment="center",
                             color = "white" if cm[i,j] > thresh else "black")

  plt.tight_layout()
  #plt.figure(figsize=(10,10))
  plt.ylabel('True Lable')
  plt.xlabel('Predicted Label')

cm_plot_labels = ["Invalid Image","Valid Image"]
plot_confusion_matrix(cm, cm_plot_labels, title = 'Confusion Matrix')

"""# Step 16: Saving Model."""

# Save entire model with optimizer, architecture, weights and training configuration.
from keras.models import load_model
model.save('FinalCheckimg.h5')

# Save model weights.
from keras.models import load_model
model.save_weights('FinalCheckimg_weights.h5')

# Get classes of model trained on
classes = train_generator.class_indices 
classes

"""# Step 17: Load Model."""

# Loading model and predict.
from keras.models import load_model
model=load_model('FinalCheckimg.h5')

# Mention name of the disease into list.
Classes = ["Invalid Image","Valid Image"]

"""# Step 18: Predictions"""

import numpy as np
import matplotlib.pyplot as plt

# Pre-Processing test data same as train data.
img_width=256
img_height=256

from keras.preprocessing import image

def prepare(img_path):
    img = keras.utils.load_img(img_path, target_size=(256, 256))
    x = keras.utils.img_to_array(img)
    x = x/255
    return np.expand_dims(x, axis=0)
    
result = model.predict([prepare('/content/FinalCheckimg/test/Invalid Image/auditorium (1).jpg')])
disease = keras.utils.load_img('/content/FinalCheckimg/test/Invalid Image/auditorium (1).jpg')
plt.imshow(disease)
print (Classes[int(np.max(result))])

"""# Step 19: Convert Model To "tflite format"."""

import tensorflow as tf

converter = tf.lite.TFLiteConverter.from_keras_model(model) 
tflite_model = converter.convert()

with open("FinalCheckimg.tflite" , "wb") as f:
  f.write(tflite_model)