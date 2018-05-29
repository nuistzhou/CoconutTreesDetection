#!/usr/bin/python2.7
import os
import sys
import argparse
import time
import numpy as np
from tabulate import tabulate

from sklearn import svm
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV

from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix

from sklearn.preprocessing import normalize

from sklearn.metrics import f1_score
from sklearn.metrics import precision_recall_fscore_support

from config import Parameters


def svmRBF_grid_search(dataset, labels):
    C_s = 10.0 ** np.arange(-1, 3)
    gammas = 10.0 ** np.arange(-3, 3)
    tuned_parameters = [{'kernel': ['rbf'], 'gamma': gammas,'C': C_s}]
    clf = GridSearchCV(svm.SVC(C=1), tuned_parameters, cv=5)
    clf.fit(dataset, labels)
    return (clf.best_params_['C'], clf.best_params_['gamma'])


def linearSVM_grid_search(dataset, labels):
    C_s = 10.0 ** np.arange(-1, 3)
    tuned_parameters = [{'C': C_s}]
    clf = GridSearchCV(svm.LinearSVC(C=1), tuned_parameters, cv=3)
    clf.fit(dataset, labels)
    return clf.best_params_['C']

def print_confusion_matrix(confusionMatrix, num_classes, file):
    """pretty print for confusion matrixes"""

    cm_list=confusionMatrix.tolist()
    cm_list[0].insert(0,'Predicted non-coco')
    cm_list[1].insert(0,'Predicted coco')
    cmTable = tabulate(cm_list,headers=['        ','Actual non-coco', 'Actual coco'])
    print cmTable
    file.write("Confusion Matrix:\n")
    file.write(cmTable + '\n\n')
    classes = ["non-coco", "coco"]
    for i in range(num_classes):
            accuracy_class = 0
            if np.sum(confusionMatrix[:,i]) > 0:
                accuracy_class = float(confusionMatrix[i,i]) / float(np.sum(confusionMatrix[:,i]))
            print "Accuracy class {} : {}".format(classes[i], accuracy_class)
            file.write("Accuracy class {} : {}\n".format(classes[i], accuracy_class))
    file.write("\n")

def main(train_dataset_filename, train_labels_filename,
         test_dataset_filename, test_labels_filename, classifier):

    # parser = argparse.ArgumentParser()
    # parser.add_argument("train_dataset_filename", type=str, help="train_dataset_filename")
    # parser.add_argument("train_labels_filename", type=str, help="train_labels_filename")
    # parser.add_argument("test_dataset_filename", type=str, help="test_dataset_filename")
    # parser.add_argument("test_labels_filename", type=str, help="test_labels_filename")
    # parser.add_argument("classifier", type=str, help="test_labels_filename", choices=['svm', 'linear_svm'])

    # args = parser.parse_args()

    # Get the current descriptor name from the "train_dataset_filename"
    descriptor_name = train_dataset_filename[:-19]
    performance_test_filename = descriptor_name + '_' + classifier
    performance_test_file_path = os.path.join(Parameters.performanceTestDir,performance_test_filename)
    f = open(performance_test_file_path, 'w')

    # train_dataset_filename = os.path.join(Parameters.mergedFeatureDescriptorPath, train_dataset_filename)
    # train_labels_filename = os.path.join(Parameters.mergedFeatureDescriptorPath, train_labels_filename)
    # test_dataset_filename = os.path.join(Parameters.mergedFeatureDescriptorPath, test_dataset_filename)
    # test_labels_filename = os.path.join(Parameters.mergedFeatureDescriptorPath, test_labels_filename)

    train_dataset_filename = os.path.join(Parameters.bowFeatureDescriptorPath, train_dataset_filename)
    train_labels_filename = os.path.join(Parameters.bowFeatureDescriptorPath, train_labels_filename)
    test_dataset_filename = os.path.join(Parameters.bowFeatureDescriptorPath, test_dataset_filename)
    test_labels_filename = os.path.join(Parameters.bowFeatureDescriptorPath, test_labels_filename)



    train_data = np.load(train_dataset_filename)
    train_data = normalize(train_data)
    train_labels =  np.load(train_labels_filename).astype(np.int32)
    test_data = np.load(test_dataset_filename)
    test_data = normalize(test_data)
    test_labels =  np.load(test_labels_filename).astype(np.int32)

    num_train = len(train_data)
    num_classes = len(np.unique(test_labels))

    print "Read dataset Ok"
    print "Working on the {0} method for descriptor {1}".format(classifier, descriptor_name)

    time_ini = time.clock()

    # create classifier object
    cls = None
    if classifier == "linear_svm":
        c = linearSVM_grid_search(train_data, train_labels)
        print "Params-> c value {}".format(c)
        f.write("Params-> c value {}\n".format(c))
        cls = svm.LinearSVC(C=c)
    else:
        c , gamma = svmRBF_grid_search(train_data, train_labels)
        print "Params -> C: "+ str(c) + ", gamma: "+str(gamma)
        f.write("Params -> C: "+ str(c) + ", gamma: \n"+str(gamma))
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

    precision, recall, fscore, support =  precision_recall_fscore_support(test_labels ,pred_test_labels)
    print "Fscore {}".format(fscore[1])
    f.write("FScore is {0}\n\n".format(fscore[1]))


    # compute overall accuracy
    acc_test = accuracy_score(test_labels, pred_test_labels)

    # compute accuracy for each class
    test_labels = [",".join(item) for item in test_labels.astype(str)]
    pred_test_labels = [",".join(item) for item in pred_test_labels.astype(str)]
    cmatrix = confusion_matrix(test_labels, pred_test_labels)
    cmatrix = np.transpose(cmatrix) # cols trueLabel and rows predicted
    print_confusion_matrix(cmatrix, num_classes, f)

    print "Number of training samples {} ,  Overall Accuracy {}: ".format(num_train, acc_test)
    f.write("Number of training samples {} ,  Overall Accuracy {}: \n".format(num_train, acc_test))

    f.close()


# if __name__ == '__main__':
    # main("hog_lower_features.npy", "hog_lower_labels.npy", "hog_upper_features.npy",
    #      "hog_upper_labels.npy", 'svm')
    # main("sift_lower_features.npy", "sift_lower_labels.npy", "sift_upper_features.npy",
    #      "sift_upper_labels.npy", 'svm')
    # main("surf_lower_features.npy", "surf_lower_labels.npy", "surf_upper_features.npy",
    #      "surf_upper_labels.npy", 'svm')

    # main("hog_lower_features.npy", "hog_lower_labels.npy", "hog_upper_features.npy",
    #      "hog_upper_labels.npy", 'linear_svm')
    # main("sift_lower_features.npy", "sift_lower_labels.npy", "sift_upper_features.npy",
    #      "sift_upper_labels.npy", 'linear_svm')
    # main("surf_lower_features.npy", "surf_lower_labels.npy", "surf_upper_features.npy",
    #      "surf_upper_labels.npy", 'linear_svm')
    # main("bow_sift_lower_features.npy", "bow_sift_lower_labels.npy",
    #      "bow_sift_upper_features.npy", "bow_sift_upper_labels.npy", 'linear_svm')
    # main("bow_surf_lower_features.npy", "bow_surf_lower_labels.npy",
    #      "bow_surf_upper_features.npy", "bow_surf_upper_labels.npy", 'linear_svm')

    # main("bow100_sift_lower_features.npy", "bow100_sift_lower_labels.npy", "bow100_sift_upper_features.npy", "bow100_sift_upper_labels.npy", "linear_svm")
    # main("bow50_sift_lower_features.npy", "bow50_sift_lower_labels.npy", "bow50_sift_upper_features.npy", "bow50_sift_upper_labels.npy", "linear_svm")
    #
    # main("bow100_surf_lower_features.npy", "bow100_surf_lower_labels.npy", "bow100_surf_upper_features.npy", "bow100_surf_upper_labels.npy", "linear_svm")
    # main("bow50_surf_lower_features.npy", "bow50_surf_lower_labels.npy", "bow50_surf_upper_features.npy", "bow50_surf_upper_labels.npy", "linear_svm")

