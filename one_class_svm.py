import numpy as np
import argparse

from sklearn.neighbors import NearestNeighbors

from sklearn.svm import OneClassSVM

from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix

from sklearn.metrics import precision_recall_fscore_support

def main():

	parser = argparse.ArgumentParser()
	parser.add_argument("train_data_filename", type=str, help="Train data file name (*.npy)")
	#parser.add_argument("train_labels_filename", type=str, help="Train data file name (*.npy)")
	parser.add_argument("known_test_filename", type=str, help="Known test data file name (*.npy)")
	parser.add_argument("unknown_test_filename", type=str, help="Unknown test data file name (*.npy)")
	args = parser.parse_args()

	train_data_filename = args.train_data_filename
	#train_labels_filename = args.train_labels_filename
	known_test_filename = args.known_test_filename
	unknown_test_filename = args.unknown_test_filename

	train_data = np.load(train_data_filename)
	#train_labels = np.load(train_labels_filename)
	kw_data = np.load(known_test_filename)
	unkw_data = np.load(unknown_test_filename)

	#num_train = len(train_labels)
	#num_classes = len(np.unique(train_labels))
	num_classes = 2
	print "read ok"
	gamma = 1
	#cls = OneClassSVM(kernel='linear', gamma=gamma)
	cls = OneClassSVM(kernel="rbf", gamma=0.1)

	cls.fit(train_data)
	print "train ok"

	num_known = len(kw_data)
	num_unknown = len(unkw_data)

	pred_test_labels = np.zeros(num_known+num_unknown).astype(np.int)
	test_labels = np.zeros(num_known+num_unknown).astype(np.int)
	test_labels[:num_known] = 1
	test_labels[num_known:] = 0

	# classify known samples
	#kw_scores = cls.decision_function(kw_data)
	kw_scores = cls.predict(kw_data)

	print "kw_scores"
	print kw_scores
	perc_pos_kw = 0
	for i in xrange(num_known):
		if kw_scores[i] > 0:
			perc_pos_kw += 1
			pred_test_labels[i] = 1
		else:
			pred_test_labels[i] = 0

	perc_pos_kw /= float(num_known)
	#print "perc_pos_kw {}".format(perc_pos_kw)

	# classify unknown samples
	#unkw_scores = cls.decision_function(unkw_data)
	unkw_scores = cls.predict(unkw_data)
	#print "unkw_scores"
	#print unkw_scores	
	perc_pos_unkw = 0
	for i in xrange(num_unknown):
		if unkw_scores[i] < 0:
			perc_pos_unkw += 1
			pred_test_labels[i+num_known] = 0
		else:
			pred_test_labels[i+num_known] = 1

	perc_pos_unkw /= float(num_unknown)
	#print "perc_pos_unkw {}".format(perc_pos_unkw)
	
	normalized_accuracy = (perc_pos_kw + perc_pos_unkw) / 2.0
	
	#print "normalized_accuracy {}".format(normalized_accuracy)


	precision, recall, fscore, support =  precision_recall_fscore_support(test_labels ,pred_test_labels)
	print "Fscore {}".format(fscore[1])

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
	
	print "Overall Accuracy {}: ".format(acc_test)
	


if __name__ == '__main__':
	main()