#!/usr/bin/python2.7
import os
import sys
import argparse
import time
import numpy as np
from sklearn import svm
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV

from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix

from sklearn.preprocessing import normalize


def svmRBF_grid_search(dataset, labels):
	C_s = 10.0 ** np.arange(-1, 3)
	gammas = 10.0 ** np.arange(-1, 3)
	tuned_parameters = [{'kernel': ['rbf'], 'gamma': gammas,'C': C_s}]
	clf = GridSearchCV(svm.SVC(C=1), tuned_parameters, cv=3)
	clf.fit(dataset, labels)
	return (clf.best_params_['C'], clf.best_params_['gamma'])


def linearSVM_grid_search(dataset, labels):
	C_s = 10.0 ** np.arange(-1, 3)
	tuned_parameters = [{'C': C_s}]
	clf = GridSearchCV(svm.LinearSVC(C=1), tuned_parameters, cv=3)
	clf.fit(dataset, labels)
	return clf.best_params_['C']


def main():

	parser = argparse.ArgumentParser()
	parser.add_argument("train_dataset_filename", type=str, help="Dataset file name (*.npy)")
	parser.add_argument("train_labels_filename", type=str, help="Label filename (*.npy)")
	parser.add_argument("test_dataset_filename", type=str, help="Dataset file name (*.npy)")
	parser.add_argument("test_labels_filename", type=str, help="Label filename (*.npy)")
	#parser.add_argument("perc_train", type=float, help="percentage of training set")
	parser.add_argument("method", type=str, help="Classifier", choices=['svm', 'linear_svm'])
	args = parser.parse_args()

	"""
	
	python classifyImagePatches.py /Users/ping/thesis/data/featureDescriptors/merged_features/hog_lower_features.npy /Users/ping/thesis/data/featureDescriptors/merged_features/hog_lower_labels.npy /Users/ping/thesis/data/featureDescriptors/merged_features/hog_upper_features.npy /Users/ping/thesis/data/featureDescriptors/merged_features/hog_upper_labels.npy svm
	python classifyImagePatches.py /Users/ping/thesis/data/featureDescriptors/merged_features/sift_lower_features.npy /Users/ping/thesis/data/featureDescriptors/merged_features/sift_lower_labels.npy /Users/ping/thesis/data/featureDescriptors/merged_features/sift_upper_features.npy /Users/ping/thesis/data/featureDescriptors/merged_features/sift_upper_labels.npy svm
	python classifyImagePatches.py /Users/ping/thesis/data/featureDescriptors/merged_features/surf_lower_features.npy /Users/ping/thesis/data/featureDescriptors/merged_features/surf_lower_labels.npy /Users/ping/thesis/data/featureDescriptors/merged_features/surf_upper_features.npy /Users/ping/thesis/data/featureDescriptors/merged_features/surf_upper_labels.npy svm
	python classifyImagePatches.py /Users/ping/thesis/data/featureDescriptors/merged_features/hog_lower_features.npy /Users/ping/thesis/data/featureDescriptors/merged_features/hog_lower_labels.npy /Users/ping/thesis/data/featureDescriptors/merged_features/hog_upper_features.npy /Users/ping/thesis/data/featureDescriptors/merged_features/hog_upper_labels.npy linear_svm
	python classifyImagePatches.py /Users/ping/thesis/data/featureDescriptors/merged_features/sift_lower_features.npy /Users/ping/thesis/data/featureDescriptors/merged_features/sift_lower_labels.npy /Users/ping/thesis/data/featureDescriptors/merged_features/sift_upper_features.npy /Users/ping/thesis/data/featureDescriptors/merged_features/sift_upper_labels.npy linear_svm
	python classifyImagePatches.py /Users/ping/thesis/data/featureDescriptors/merged_features/surf_lower_features.npy /Users/ping/thesis/data/featureDescriptors/merged_features/surf_lower_labels.npy /Users/ping/thesis/data/featureDescriptors/merged_features/surf_upper_features.npy /Users/ping/thesis/data/featureDescriptors/merged_features/surf_upper_labels.npy linear_svm

	"""

	"""
	dataset_filename = args.dataset_filename
	labels_filename = args.labels_filename
	perc_train = args.perc_train
	method = args.method
	
	dataset = np.load(dataset_filename)
	labels =  np.load(labels_filename).astype(np.int32)	

	num_classes_total = len(np.unique(labels))

	# split dataset in train and test samples
	num_samples = dataset.shape[0]
	random_list = np.arange(num_samples)
	np.random.shuffle(random_list)

	num_train = int(num_samples * perc_train)

	selected_random = random_list[:num_train]
	selected_labels = labels[selected_random]
	num_classes = len(np.unique(selected_labels))
	assert(num_classes == num_classes_total)
	print "num_classes {}".format(num_classes)
	
	train_index = selected_random
	test_index = np.array(list(set(range(num_samples)) - set(train_index))).astype(np.int)
	
	train_data = dataset[train_index]
	test_data = dataset[test_index]
	train_labels = labels[train_index]
	test_labels = labels[test_index]
	"""
	
	train_dataset_filename = args.train_dataset_filename
	train_labels_filename = args.train_labels_filename
	test_dataset_filename = args.test_dataset_filename
	test_labels_filename = args.test_labels_filename
	method = args.method

	train_data = np.load(train_dataset_filename)
	train_data = normalize(train_data)
	train_labels =  np.load(train_labels_filename).astype(np.int32)	
	test_data = np.load(test_dataset_filename)
	test_data = normalize(test_data)
	test_labels =  np.load(test_labels_filename).astype(np.int32)	

	num_train = len(train_data)
	num_classes = len(np.unique(train_labels))

	print "Read dataset Ok"

	time_ini = time.clock()

	# create classifier object
	cls = None
	if method == "linear_svm":
		c = linearSVM_grid_search(train_data, train_labels)
		print "Params-> c value {}".format(c)
		cls = svm.LinearSVC(C=c)
	else:
		c , gamma = svmRBF_grid_search(train_data, train_labels)
		print "Params -> C: "+ str(c) + ", gamma: "+str(gamma)
		cls = svm.SVC(C=c, gamma=gamma)
	
	# train classifier
	cls.fit(train_data, train_labels)
	time_sec = (time.clock() - time_ini)
	print "time train {}".format(time_sec)

	# predict labels of test samples
	time_ini = time.clock()

	pred_test_labels = cls.predict(test_data)

	time_sec = (time.clock() - time_ini)
	print "time classification {}".format(time_sec)

	# compute overall accuracy 
	acc_test = accuracy_score(test_labels, pred_test_labels)

	# compute accuracy for each class
	cmatrix = confusion_matrix(test_labels, pred_test_labels)
	cmatrix = np.transpose(cmatrix) # cols trueLabel and rows predicted
	for i in range(num_classes):
			accuracy_class = 0
			if np.sum(cmatrix[:,i]) > 0:
				accuracy_class = float(cmatrix[i,i]) / float(np.sum(cmatrix[:,i]))
			print "Accuracy class {} : {}".format(i, accuracy_class)
	
	print "Num train samples {} ,  Overall Accuracy {}: ".format(num_train, acc_test)
	

if __name__ == '__main__':
	main()