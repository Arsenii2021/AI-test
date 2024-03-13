import cv2
import numpy as np
import os
from random import shuffle
from tqdm import tqdm
import tflearn
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
import tensorflow as tf
import matplotlib.pyplot as plt

TRAIN_DIR = './dir/train'
TEST_DIR = './dir/test'
IMG_WIDTH = 200
IMG_HEIGHT = 200
LR = 1e-6
MODEL_NAME = 'vm.model'

# Define label conversion functions (switch_label and switch_number) 
# This block in proccess 

# Modify the label_img function to handle multiple images
def label_img(img):
    labels = [img.split('.')[0][0] for img in os.listdir(TRAIN_DIR)]
    return [switch_label(label) for label in labels]

# Modify the process_data function to handle multiple images
def process_data(img, labels):
    img = cv2.resize(img, (IMG_HEIGHT, IMG_WIDTH))
    npImg = np.array(img)
    npLabels = np.array(labels)
    return npImg, npLabels

# Modify the create_train_data function to handle all images in the directory
def create_train_data():
    training_data = []
    for img in tqdm(os.listdir(TRAIN_DIR)):
        labels = label_img(img)
        path = os.path.join(TRAIN_DIR, img)
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        npImg, npLabels = process_data(img, labels)
        training_data.append([npImg, npLabels])
    shuffle(training_data)
    np.save('train_data_all.npy', training_data)
    return training_data

# Modify the process_test_data function to handle all images in the directory
def process_test_data():
    testing_data = []
    for img in tqdm(os.listdir(TEST_DIR)):
        labels = [img.split('.')[0] for img in os.listdir(TEST_DIR)]
        path = os.path.join(TEST_DIR, img)
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        npImg, npLabels = process_data(img, labels)
        testing_data.append([npImg, npLabels])
    shuffle(testing_data)
    np.save('test_data_all.npy', testing_data)
    return testing_data

# Modify the create_model function to handle multi-label classification and all training data
def create_model(train_data=None):
  tf.reset_default_graph()

	convnet = input_data(shape=[None, IMG_HEIGHT, IMG_WIDTH, 1], name='input')

	convnet = conv_2d(convnet, 32, 3, padding='valid', activation='relu')
	convnet = max_pool_2d(convnet, 2, padding='valid', strides=2)

	convnet = conv_2d(convnet, 64, 3, padding='valid', activation='relu')
	convnet = max_pool_2d(convnet, 2, padding='valid', strides=2)

	convnet = conv_2d(convnet, 128, 3, padding='valid', activation='relu')
	convnet = max_pool_2d(convnet, 2, padding='valid', strides=2)

	convnet = conv_2d(convnet, 256, 5, padding='valid', activation='relu')
	convnet = max_pool_2d(convnet, 2)

	convnet = conv_2d(convnet, 256, 5, activation='relu')
	convnet = max_pool_2d(convnet, 3)

	convnet = conv_2d(convnet, 256, 3, activation='relu')
	convnet = max_pool_2d(convnet, 3)

	convnet = conv_2d(convnet, 512, 3, activation='relu')
	convnet = max_pool_2d(convnet, 2)

	convnet = fully_connected(convnet, 1024, activation='relu')
	convnet = dropout(convnet, 0.8)

	convnet = fully_connected(convnet, 4, activation='softmax')
	convnet = regression(convnet, optimizer='adam', learning_rate=LR, loss='categorical_crossentropy', name='targets')

	model = tflearn.DNN(convnet, tensorboard_dir='log')

	if os.path.exists('{}.meta'.format(MODEL_NAME)):
		model.load(MODEL_NAME)
		print('model loaded!')
		return model

	else:

		if train_data == None:
			train_data = create_train_data()

		test_size = int(0.2*len(train_data))

		train = train_data[:-test_size]
		test = train_data[-test_size:]


		X = np.array([i[0] for i in train]).reshape(-1,IMG_HEIGHT, IMG_WIDTH, 1)
		y = [i[1] for i in train]

		X_test = np.array([i[0] for i in test]).reshape(-1,IMG_HEIGHT, IMG_WIDTH, 1)
		y_test = [i[1] for i in test]

		model.fit({'input': X}, {'targets': y}, n_epoch=30, validation_set=({'input': X_test}, {'targets': y_test}), snapshot_step=100, show_metric=True, run_id=MODEL_NAME)

		model.save(MODEL_NAME)
		print('model created!')
		return model


# Modify the run_test_data and predict_data functions to handle multiple images
def run_test_data(test_data, model):
    fig=plt.figure()

	for num,data in enumerate(test_data[30:42]):
		img_num = data[1]
		img_data = data[0]

		y = fig.add_subplot(3,4,num+1)
		orig = img_data
		data = img_data.reshape(IMG_HEIGHT,IMG_WIDTH,1)
		model_out = model.predict([data])[0]

		str_label = switch_number(np.argmax(model_out))
		    
		y.imshow(orig,cmap='gray')
		plt.title(str_label)
		y.axes.get_xaxis().set_visible(False)
		y.axes.get_yaxis().set_visible(False)
	plt.show()

def predict_data(img_data, model):
    data = img_data[0].reshape(IMG_HEIGHT,IMG_WIDTH,1)
	model_out = model.predict([data])[0]
	str_label = switch_number(np.argmax(model_out))
	return str_label
