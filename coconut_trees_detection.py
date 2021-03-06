# -*- coding: utf-8 -*-
"""
/***************************************************************************
 CoconutTreesDetection
                                 A QGIS plugin
 Application to annotate coconut trees in aerial imagery and do the detection
                              -------------------
        begin                : 2018-03-07
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Ping Zhou
        email                : nuistzhou@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
import os
import time
import threading
import os.path
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication, Qt
from PyQt4.QtGui import QAction, QIcon
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.gui import *
from qgis.core import *
import pickle
import numpy as np
from PIL import Image
from sklearn import svm
import gdal
from sklearn.calibration import CalibratedClassifierCV
from sklearn.externals import joblib # For model saving
import cv2
from clickTool import *
from tools import *
from config import Parameters
from codebook import extract_code_for_Images_List
from bovw import extract_bovw_features
from createRandomSamplePatches import extractRandomPatchCenterFromListWithoutMask
from visualization import Visualization
import classification_map
from extractTraingSamplePatches import getPointPixelCoordinates


# Initialize Qt resources from filePickle resources.py
import resources

# Import the code for the DockWidget
from coconut_trees_dockwidget_loader import DockWidget



class CoconutTreesDetection:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgisInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        self.canvas = self.iface.mapCanvas()
        self.codebook = None

        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)

        self.dockWidgetAnnotation = DockWidget(self.iface.mainWindow(), self.iface)

        self.uiDockWidgetAnnotation = self.dockWidgetAnnotation.ui


        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'CoconutTreesDetection_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&CoconutTreesDetection')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'CoconutTreesDetection')
        self.toolbar.setObjectName(u'CoconutTreesDetection')

        self.pluginIsActive = False
        self.dockwidget = None




    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('CoconutTreesDetection', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal filePickle system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action


    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        self.iface.addDockWidget(Qt.RightDockWidgetArea, self.dockWidgetAnnotation)
        icon_path = ':/plugins/CoconutTreesDetection/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'coconutTreesDetection'),
            callback=self.run,
            parent=self.iface.mainWindow())

        # imgFilename = self.iface.activeLayer().dataProvider().dataSourceUri()
        self.imgFilename = Parameters.rgb_image_clipped_tif
        self.layer = self.getLayerByName(Parameters.rgb_image_layername)
        self.windowArrayList = list()
        # self.imgArray = cv2.imread(self.imgFilename)
        self.imgArray = gdal.Open(self.imgFilename).ReadAsArray().astype(np.uint8)
        self.imgArray = np.transpose(self.imgArray, (1, 2, 0))
        self.bovwTrainingFeatures = None
        self.labelTrainingArray = None
        self.predicted_probs = None
        self.pred_test_labels = None
        self.windowsCentersList = list()
        self.windowPositiveIndexList = list()
        self.windowNegativeIndexList = list()

        self.config = Parameters(self.layer)
        self.config.readRasterConfig()
        self.canvasClicked = ClickTool(self.config, self.canvas, self.layer, self.imgArray)
        self.canvas.setMapTool(self.canvasClicked)

        self.uiDockWidgetAnnotation.btnLoadAnnotationFile.clicked.connect(self.loadAnnotationsAndDisplay)
        self.uiDockWidgetAnnotation.btnSaveAnnotationFile.clicked.connect(self.saveAnnotationFile)
        self.uiDockWidgetAnnotation.btnAddAnnotationCoco.clicked.connect(self.addAnnotationsCoco)
        self.uiDockWidgetAnnotation.btnDeleteAnnotation.clicked.connect(self.deleteAnnotation)
        self.uiDockWidgetAnnotation.btnClassify.clicked.connect(self.classify)
        self.uiDockWidgetAnnotation.btnPreprocess.clicked.connect(self.preprocess)
        self.uiDockWidgetAnnotation.btnAddAnnotationNoncoco.clicked.connect(self.addAnnotationsNoncoco)
        self.uiDockWidgetAnnotation.btnDeleteAllAnnotation.clicked.connect(self.deleteAllAnnnotaions)
        self.uiDockWidgetAnnotation.btnVisualize.clicked.connect(self.tsneVisualization)
        self.uiDockWidgetAnnotation.btnTest.clicked.connect(self.calRecall)
        self.uiDockWidgetAnnotation.btnValidate.clicked.connect(self.validate)



        #-------------------------------------------------------------------
        # Add function for auto-save later...
        # autoSaver = threading.Thread(target = self.autosavePickleFile())
        # autoSaver.start()
        #--------------------------------------------------------------------


    def getLayerByName(self, layer_name):
        layer = None
        for lyr in QgsMapLayerRegistry.instance().mapLayers().values():
            if lyr.name() == layer_name:
                layer = lyr
                break
        return layer


    def loadAnnotationsAndDisplay(self):

        self.canvasClicked.addingCoco = False
        self.canvasClicked.addingNoncoco = False
        self.canvasClicked.deleting = False

        if not os.path.isfile(Parameters.annotationCocoFile):
            with open(Parameters.annotationCocoFile, 'w') as filePickle_read:
                pass
            QMessageBox.information(self.iface.mainWindow(), "Load Coconut Annotations", "Coconut annotation file created!")

        else:
            try:
                with open(Parameters.annotationCocoFile, "r") as filePickle_read:
                    self.canvasClicked.annotationCocoList = pickle.load(filePickle_read)

                    # QMessageBox.information(self.iface.mainWindow(), "loadCocoAnnotations", "Coco annotations Loaded!")
            except EOFError:
                QMessageBox.information(self.iface.mainWindow(), "Load Coconut Annotations", "Empty coconut annotation file!")

        if not os.path.isfile(Parameters.annotationNoncocoFile):
            with open(Parameters.annotationNoncocoFile, 'w') as filePickle_read:
                pass
            QMessageBox.information(self.iface.mainWindow(), "Load Non-coconut Annotations", "Non-coconut annotation file created!")

        else:
            try:
                with open(Parameters.annotationNoncocoFile, "r") as filePickle_read:
                    self.canvasClicked.annotationNoncocoList = pickle.load(filePickle_read)


                    QMessageBox.information(self.iface.mainWindow(), "LoadAnnotations", "Annotations Loaded!")
            except EOFError:
                    QMessageBox.information(self.iface.mainWindow(), "LoadAnnotations", "Empty non-coconut annotation file!")

        # Display loaded annotations on canvas
        self.canvasClicked.displayAnnotations()


    def saveAnnotationFile(self):
        with open(Parameters.annotationCocoFile, "w") as filePickle_save:
            pickle.dump(self.canvasClicked.annotationCocoList, filePickle_save)
        with open(Parameters.annotationNoncocoFile, "w") as filePickle_save:
            pickle.dump(self.canvasClicked.annotationNoncocoList, filePickle_save)

        self.canvasClicked.deleting = False
        self.canvasClicked.addingCoco = False
        self.canvasClicked.addingNoncoco = False
        QMessageBox.information(self.iface.mainWindow(), "Save Annotations", "All annotations saved!")

    def addAnnotationsCoco(self):
        """Call this function to get clicked point coordinates after pressed the 'Add' button"""
        self.canvasClicked.addingCoco = True
        self.canvasClicked.addingNoncoco = False
        self.canvasClicked.deleting = False
        self.canvas.setMapTool(self.canvasClicked)

    def addAnnotationsNoncoco(self):
        """Call this function to get clicked point coordinates after pressed the 'Add' button"""
        self.canvasClicked.addingNoncoco = True
        self.canvasClicked.addingCoco = False
        self.canvasClicked.deleting = False
        self.canvas.setMapTool(self.canvasClicked)


    def deleteAnnotation(self):
        """Delete clicked annotations on the canvas"""
        self.canvasClicked.addingCoco = False # Deactivate the addingCoco activity
        self.canvasClicked.addingNoncoco = False
        self.canvasClicked.deleting = True
        self.canvas.setMapTool(self.canvasClicked)

    def deleteAllAnnnotaions(self):
        """Delete all annotations on the canvas"""
        self.canvasClicked.addingNoncoco = False
        self.canvasClicked.addingCoco = False
        self.canvasClicked.deleteAllAnnnotaions()


    def preprocess(self):
        """Build the Bag of Visual Words codebook and create sliding windows for grid search
        Check if codebook.npy and testFeatures.npy exist, if not, create, otherwise load from disk."""
        timeStart = time.time()
        self.canvasClicked.addingCoco = False
        self.canvasClicked.addingNoncoco = False
        self.canvasClicked.deleting = False
        if not os.path.isfile(Parameters.codebookFileName):
            imgHeight = self.imgArray.shape[0]
            imgWidth = self.imgArray.shape[1]
            nrRandomSamples = Parameters.bovwCodebookNrRandomSamples
            randomPatchesArrayList = list()
            print "Creating random samples for building the codebook ..."
            randomPatchesCenterList = extractRandomPatchCenterFromListWithoutMask(nrRandomSamples, imgHeight, imgWidth)

            for randomPatchCenter in randomPatchesCenterList:
                centerX = randomPatchCenter[0]
                centerY = randomPatchCenter[1]

                tl_x = int(centerX - Parameters.samplePatchSize / 2)
                tl_y = int(centerY - Parameters.samplePatchSize / 2)

                br_x = tl_x + Parameters.samplePatchSize
                br_y = tl_y + Parameters.samplePatchSize

                # Replace with boundary when beyond
                tl_x = max(tl_x, 0)
                tl_y = max(tl_y, 0)
                br_x = min(br_x, self.imgArray.shape[1] - 1)
                br_y = min(br_y, self.imgArray.shape[0] - 1)

                randomPatchesArrayList.append(self.imgArray[tl_y: br_y + 1, tl_x: br_x + 1,:])

            timeRandomPatchForCodebook = time.time()
            print "Random samples generated!"
            print "Generating codebook with {0} random samples, takes {1: .2f} seconds".format(nrRandomSamples, timeRandomPatchForCodebook - timeStart)

            print "Building the codebook ..."
            self.codebook = extract_code_for_Images_List(randomPatchesArrayList)
            np.save(Parameters.codebookFileName, self.codebook)
            print "Codebook built!"


        else:
            self.codebook = np.load(Parameters.codebookFileName)
            print "Codebook loaded!"

        # if not os.path.exists(Parameters.testFeatures):
        self.extractProposalFeaturesForPrediction()
            # np.save(Parameters.testFeatures, self.bovwTestFeatures)
        timeEndPreprocessing = time.time()
        print "The whole preprocessing takes {0: .2f} seconds!".format(timeEndPreprocessing - timeStart)
        print "Test features loaded!"

    def extractProposalFeaturesForPrediction(self):
        start_time = time.time()
        # Generate sliding windows
        if not (os.path.isfile(Parameters.testWindowCentersList) and
            (os.path.isfile(Parameters.testFeatures))):
            pixel_size_x = self.layer.rasterUnitsPerPixelX()
            pixel_size_y = self.layer.rasterUnitsPerPixelY()
            top_left_x = self.layer.extent().xMinimum()
            top_left_y = self.layer.extent().yMaximum()
            bottom_right_x = self.layer.extent().xMaximum()
            bottom_right_y = self.layer.extent().yMinimum()
            dim_x = int((bottom_right_x - top_left_x) / pixel_size_x)
            dim_y = int((top_left_y - bottom_right_y) / pixel_size_y)

            window_top_left_y = 0
            window_bottom_right_y = 90
            while window_bottom_right_y < dim_y - Parameters.samplePatchSize:
                window_bottom_right_x = 90
                window_top_left_x = 0
                while (window_bottom_right_x < dim_x  - Parameters.samplePatchSize):
                    windowArray = self.imgArray[window_top_left_y : window_bottom_right_y,
                                  window_top_left_x : window_bottom_right_x, :]
                    self.windowArrayList.append(windowArray)
                    windowCenterTuple = ((window_top_left_x + Parameters.samplePatchSize/2),
                                   (window_top_left_y + Parameters.samplePatchSize/2))
                    self.windowsCentersList.append(windowCenterTuple)
                    window_top_left_x += Parameters.strideSize
                    window_bottom_right_x += Parameters.strideSize
                window_top_left_y  += Parameters.strideSize
                window_bottom_right_y += Parameters.strideSize


            with open(Parameters.testWindowCentersList, 'w') as f:
                pickle.dump(self.windowsCentersList, f)
            print "All window centers list created!"

            self.bovwTestFeatures = extract_bovw_features(self.windowArrayList, self.codebook)[0]

            with open(Parameters.testFeatures, 'w') as f:
                pickle.dump(self.bovwTestFeatures, f)
            #
            # with open(Parameters.testWindowArrayList, 'w') as f:
            #     pickle.dump(self.windowArrayList, f)

            print "All  windows created!"
            timeGeneratingSlindingwindows = time.time()
            # print "Generating {0} sliding windows with stride size of {1} takes {2:.2f} seconds".format(len(self.windowArrayList), Parameters.strideSize, timeGeneratingSlindingwindows - start_time)


        else:
            with open(Parameters.testWindowCentersList, 'r') as f:
                self.windowsCentersList = pickle.load(f)

                self.bovwTestFeatures = np.load(Parameters.testFeatures)
            print "Window bovw features loaded!"

            print "Window Centers List loaded!"

            print "All window bovw features extracted! "
            timeExtractWindowFeatures = time.time()
            # print "Extracting features from all sliding windows takes {0:.2f} seconds".format(timeExtractWindowFeatures - timeGeneratingSlindingwindows)



            # with open(Parameters.testWindowArrayList, 'r') as f:
            #     self.windowArrayList = pickle.load(f)


    def classify(self):
        timeStart = time.time()

        """Do the classification job here"""
        self.canvasClicked.addingCoco = False
        self.canvasClicked.deleting = False


        # Do the classification
        bovwTrainingCocoFeatures = extract_bovw_features(self.canvasClicked.patchArrayCocoList, self.codebook)[0]
        labelTrainingCocoArray = np.ones(bovwTrainingCocoFeatures.shape[0], dtype = np.int) # One
        bovwTrainingNoncocoFeatures = extract_bovw_features(self.canvasClicked.patchArrayNoncocoList, self.codebook)[0]
        labelTrainingNoncocoArray = np.zeros(bovwTrainingNoncocoFeatures.shape[0], dtype = np.int) # Zero
        self.bovwTrainingFeatures = np.concatenate((bovwTrainingCocoFeatures, bovwTrainingNoncocoFeatures))
        self.labelTrainingArray = np.concatenate((labelTrainingCocoArray, labelTrainingNoncocoArray))

        timeExtractTrainingFeatures = time.time()
        print "Extracting features from all sliding windows takes {0:.2f} seconds".format(timeExtractTrainingFeatures - timeStart)

        print "Number of training samples are {0}, with {1} Coco and {2} Non_coco!"\
            .format(len(self.bovwTrainingFeatures), len(bovwTrainingCocoFeatures), len(bovwTrainingNoncocoFeatures))
        timeTuningCparameter = time.time()
        print "Tuning C parameter for the SVM takes {0:.2f} seconds".format(timeTuningCparameter - timeExtractTrainingFeatures)

        # Only train the new model when the model file is not exists on the disk
        if not os.path.isfile(Parameters.trainedModelPath):
            c_tuned = linearSVM_grid_search(self.bovwTrainingFeatures, self.labelTrainingArray)
            print "Tuned C parameter is {0}".format(c_tuned)
            linear_svm_classifier = svm.LinearSVC(C = c_tuned, random_state = 10)

            calibrated_svc = CalibratedClassifierCV(linear_svm_classifier)
            calibrated_svc.fit(self.bovwTrainingFeatures, self.labelTrainingArray)

        # linear_svm_classifier.fit(self.bovwTrainingFeatures, self.labelTrainingArray)
            # save the trained model to a pickle file locally on the disk
            # joblib.dump(linear_svm_classifier, Parameters.trainedModelPath)
            joblib.dump(calibrated_svc, Parameters.trainedModelPath)

        else:
        # load the previsouly trained model
        #     linear_svm_classifier = joblib.load(Parameters.trainedModelPath)
            calibrated_svc = joblib.load(Parameters.trainedModelPath)

        self.predicted_probs = calibrated_svc.predict_proba(self.bovwTestFeatures)


        # self.pred_test_labels = linear_svm_classifier.predict(self.bovwTestFeatures)
        # calibrated_svc = CalibratedClassifierCV(linear_svm_classifier)
        # calibrated_svc.fit(self.bovwTrainingFeatures, self.labelTrainingArray)
        # self.predicted_probs = calibrated_svc.predict_proba(self.bovwTestFeatures)  # important to use predict_proba
        self.pred_test_labels = np.argmax(self.predicted_probs, 1)
        print "Number of {0} Prediction Labels created! ".format(len(self.pred_test_labels))


        timeTrainAndPredict = time.time()
        print "Training and predicting takes {0:.2f} seconds".format(timeTrainAndPredict - timeTuningCparameter)
        print "It takes {0} seconds to classify in total!".format(timeTrainAndPredict - timeStart)

        np.save(Parameters.predictionLabels, self.pred_test_labels)
        np.save(Parameters.predictionProbs,self.predicted_probs)

        # Load the classification probability map
        predicted_probs_matrix = classification_map.calPredictedProbsMatrix(Parameters.rgb_image_clipped_tif, self.pred_test_labels, self.predicted_probs)
        classficationLayer = classification_map.loadRasterLayer(predicted_probs_matrix, Parameters.rgb_image_clipped_tif, Parameters.rstClassPathext, "probability_map")
        classification_map.styleProbabilityMapRasterLayer(classficationLayer)

        # Separate windows classified as trees or no
        for i,label in enumerate(self.pred_test_labels):
            if label == 0:
                self.windowNegativeIndexList.append(i)
            else:
                self.windowPositiveIndexList.append(i)

    # def calRecall(self):
    #     """Calculate recall based on the confusion matrix."""
    #     distanceThreshold = 45**2 # unit: pixel
    #     countedWindowsIndexList = list()
    #     countedWindowsCentersList = list()
    #
    #     # Load the ground truths
    #     groundTruthCentersList = featurePoint2PixelPosition(Parameters.groundTruthLayername, Parameters.rgb_image_layername)
    #     tpCounter = 0 # true positive counter
    #     fnCounter = 0 # false negative counter
    #     tnCounter = 0 # true negative counter
    #     fpCounter = 0 # false positive counter
    #
    #     print len(groundTruthCentersList)
    #     print len(self.windowsCentersList)
    #     print len(self.windowNegativeIndexList), "Negative prediction"
    #     print len(self.windowPositiveIndexList), "Positive prediction"
    #
    #     # True positive (TP) and False negative (FN):
    #     for groundtruth in groundTruthCentersList:
    #         found = False
    #         for windowCenterIndex in self.windowPositiveIndexList:
    #             distance = calDistanceBetweenCenterTuple(groundtruth, self.windowsCentersList[windowCenterIndex])
    #             if distance <= distanceThreshold:
    #                 tpCounter += 1
    #                 found = True
    #                 break
    #         if not found:
    #             fnCounter += 1
    #     # True negative (TN) and False positive (FP):
    #     for i,window in enumerate(self.windowsCentersList):
    #         found = False
    #         if (i in self.windowNegativeIndexList):
    #             # for groundtruthCenter in groundTruthCentersList:
    #             #     distance = calDistanceBetweenCenterTuple(groundtruthCenter, window)
    #             #     if distance < distanceThreshold:
    #             #         found = True
    #             #         break
    #             # if not found:
    #             #     tnCounter += 1
    #             pass
    #         else:
    #             # if i not in countedWindowsIndexList:
    #             for groundtruthCenter in groundTruthCentersList:
    #                 distance = calDistanceBetweenCenterTuple(groundtruthCenter, window)
    #                 if distance <= distanceThreshold:
    #                     found = True
    #                     break
    #             if found:
    #                 continue
    #
    #             overlap = False
    #             for countedWindow in countedWindowsCentersList:
    #                 d = calDistanceBetweenCenterTuple(countedWindow, window)
    #                 if d <= distanceThreshold:
    #                     overlap = True
    #                     break
    #
    #             if not overlap:
    #                 countedWindowsIndexList.append(i)
    #                 countedWindowsCentersList.append(window)
    #                 fpCounter += 1
    #
    #     print "False positive, true positive, true negative, false negative:", fpCounter, tpCounter, tnCounter,fnCounter
    #     recall = float(tpCounter)/(tpCounter + fnCounter)  * 100
    #     precision = float(tpCounter)/(tpCounter + fpCounter) * 100
    #     print "The recalll is {0} and the precision is {1} for distanceThreshold {2}".format(recall, precision,distanceThreshold)

    def calRecall(self):
        """Calculate recall based on the confusion matrix."""
        distanceThresholdSquare = Parameters.recallDistanceSquare**2  # unit: pixel
        countedWindowsIndexList = list()
        countedWindowsCentersList = list()

        # Load the ground truths
        groundTruthCentersList = featurePoint2PixelPosition(Parameters.groundTruthLayername,
                                                            Parameters.rgb_image_layername)
        # print groundTruthCentersList
        # print self.windowsCentersList
        tpCounter = 0  # true positive counter
        fnCounter = 0  # false negative counter
        tnCounter = 0  # true negative counter
        fpCounter = 0  # false positive counter

        print len(groundTruthCentersList)
        print len(self.windowsCentersList)
        print len(self.windowNegativeIndexList), "Negative prediction"
        print len(self.windowPositiveIndexList), "Positive prediction"

        # True positive (TP) and False negative (FN):
        for groundtruth in groundTruthCentersList:
            found = False
            for windowCenterIndex in self.windowPositiveIndexList:
                distanceSquare = calDistanceBetweenCenterTuple(groundtruth, self.windowsCentersList[windowCenterIndex])
                if distanceSquare <= distanceThresholdSquare:
                    tpCounter += 1
                    found = True
                    break
            if not found:
                fnCounter += 1
        print "proc... TP and FN ok"
        # True negative (TN) and False positive (FP):
        """
        for i,window in enumerate(self.windowsCentersList):
            found = False
            if (i in self.windowNegativeIndexList):
                # for groundtruthCenter in groundTruthCentersList:
                #     distance = calDistanceBetweenCenterTuple(groundtruthCenter, window)
                #     if distance < distanceThreshold:
                #         found = True
                #         break
                # if not found:
                #     tnCounter += 1
                pass
            else:
                # if i not in countedWindowsIndexList:
                for groundtruthCenter in groundTruthCentersList:
                    distance = calDistanceBetweenCenterTuple(groundtruthCenter, window)
                    if distance <= distanceThreshold:
                        found = True
                        break
                if found:
                    continue

                overlap = False
                for countedWindow in countedWindowsCentersList:
                    d = calDistanceBetweenCenterTuple(countedWindow, window)
                    if d <= distanceThreshold:
                        overlap = True
                        break

                if not overlap:
                    countedWindowsIndexList.append(i)
                    countedWindowsCentersList.append(window)
                    fpCounter += 1
        """

        for windowCenterIndex in self.windowPositiveIndexList:
            window = self.windowsCentersList[windowCenterIndex]
            found = False
            for groundtruthCenter in groundTruthCentersList:
                distanceSquare = calDistanceBetweenCenterTuple(groundtruthCenter, window)
                if distanceSquare <= distanceThresholdSquare:
                    found = True
                    break
            if found:
                continue

            overlap = False
            for countedWindow in countedWindowsCentersList:
                distanceSquare = calDistanceBetweenCenterTuple(countedWindow, window)
                if distanceSquare <= distanceThresholdSquare:
                    overlap = True
                    break

            if not overlap:
                # countedWindowsIndexList.append(i)
                countedWindowsCentersList.append(window)
                fpCounter += 1

        print "False positive, true positive, true negative, false negative:", fpCounter, tpCounter, tnCounter, fnCounter
        recall = float(tpCounter) / (tpCounter + fnCounter) * 100
        precision = float(tpCounter) / (tpCounter + fpCounter) * 100
        print "The recalll is {0} and the precision is {1} for distanceThreshold {2}".format(recall, precision,
                                                                                             int(math.sqrt(distanceThresholdSquare)))
    # def calRecallValidation(self, windowsCentersList,
    #                         windowNegativeIndexList, windowPositiveIndexList):
    #     """Calculate recall based on the confusion matrix."""
    #     distanceThresholdSquare = 45 # unit: pixel
    #     countedWindowsIndexList = list()
    #     countedWindowsCentersList = list()
    #
    #     # Load the ground truths
    #     groundTruthCentersList = featurePoint2PixelPosition(Parameters.groundTruthLayername_validation, Parameters.rgb_image_layername_validation)
    #     tpCounter = 0 # true positive counter
    #     fnCounter = 0 # false negative counter
    #     tnCounter = 0 # true negative counter
    #     fpCounter = 0 # false positive counter
    #
    #     print len(groundTruthCentersList)
    #     print len(windowsCentersList)
    #     print len(windowNegativeIndexList), "Negative prediction"
    #     print len(windowPositiveIndexList), "Positive prediction"
    #
    #     # True positive (TP) and False negative (FN):
    #     for groundtruth in groundTruthCentersList:
    #         found = False
    #         for windowCenterIndex in windowPositiveIndexList:
    #             distanceSquare = calDistanceBetweenCenterTuple(groundtruth, windowsCentersList[windowCenterIndex])
    #             if distanceSquare <= distanceThresholdSquare:
    #                 tpCounter += 1
    #                 found = True
    #                 break
    #         if not found:
    #             fnCounter += 1
    #     # True negative (TN) and False positive (FP):
    #     for i,window in enumerate(windowsCentersList):
    #         found = False
    #         if (i in windowNegativeIndexList):
    #             # for groundtruthCenter in groundTruthCentersList:
    #             #     distance = calDistanceBetweenCenterTuple(groundtruthCenter, window)
    #             #     if distance < distanceThreshold:
    #             #         found = True
    #             #         break
    #             # if not found:
    #             #     tnCounter += 1
    #             pass
    #         else:
    #             # if i not in countedWindowsIndexList:
    #             for groundtruthCenter in groundTruthCentersList:
    #                 distanceSquare = calDistanceBetweenCenterTuple(groundtruthCenter, window)
    #                 if distanceSquare <= distanceThresholdSquare:
    #                     found = True
    #                     break
    #             if found:
    #                 continue
    #
    #             overlap = False
    #             for countedWindow in countedWindowsCentersList:
    #                 distanceSquare = calDistanceBetweenCenterTuple(countedWindow, window)
    #                 if distanceSquare <= distanceThresholdSquare:
    #                     overlap = True
    #                     break
    #
    #             if not overlap:
    #                 countedWindowsIndexList.append(i)
    #                 countedWindowsCentersList.append(window)
    #                 fpCounter += 1
    #
    #     print "Validation: False positive, true positive, true negative, false negative:", fpCounter, tpCounter, tnCounter,fnCounter
    #     recall = float(tpCounter)/(tpCounter + fnCounter)  * 100
    #     precision = float(tpCounter)/(tpCounter + fpCounter) * 100
    #     print "Validation: The recalll is {0} and the precision is {1} for distanceThreshold {2}".format(recall, precision,distanceThresholdSquare)

    def calRecallValidation(self, windowsCentersList,
                            windowNegativeIndexList, windowPositiveIndexList):
        """Calculate recall based on the confusion matrix."""
        distanceThresholdSquare = Parameters.recallDistanceSquare**2  # unit: pixel
        countedWindowsIndexList = list()
        countedWindowsCentersList = list()

        # Load the ground truths
        groundTruthCentersList = featurePoint2PixelPosition(Parameters.groundTruthLayername_validation,
                                                            Parameters.rgb_image_layername_validation)
        tpCounter = 0  # true positive counter
        fnCounter = 0  # false negative counter
        tnCounter = 0  # true negative counter
        fpCounter = 0  # false positive counter

        # True positive (TP) and False negative (FN):
        for groundtruth in groundTruthCentersList:
            found = False
            for windowCenterIndex in windowPositiveIndexList:
                distanceSquare = calDistanceBetweenCenterTuple(groundtruth, windowsCentersList[windowCenterIndex])
                if distanceSquare <= distanceThresholdSquare:
                    tpCounter += 1
                    found = True
                    break
            if not found:
                fnCounter += 1

        for windowCenterIndex in windowPositiveIndexList:
            window = windowsCentersList[windowCenterIndex]
            found = False

            for groundtruthCenter in groundTruthCentersList:
                distanceSquare = calDistanceBetweenCenterTuple(groundtruthCenter, window)
                if distanceSquare <= distanceThresholdSquare:
                    found = True
                    break
            if found:
                continue

            overlap = False
            for countedWindow in countedWindowsCentersList:
                dSauare = calDistanceBetweenCenterTuple(countedWindow, window)
                if dSauare <= distanceThresholdSquare:
                    overlap = True
                    break

            if not overlap:
                # countedWindowsIndexList.append(i)
                countedWindowsCentersList.append(window)
                fpCounter += 1

        print "Validation: False positive, true positive, true negative, false negative:", fpCounter, tpCounter, tnCounter, fnCounter
        recall = float(tpCounter) / (tpCounter + fnCounter) * 100
        precision = float(tpCounter) / (tpCounter + fpCounter) * 100
        print "Validation: The recalll is {0} and the precision is {1} for distanceThreshold {2}".format(recall,
                                                                                                         precision,
                                                                                                         int(math.sqrt(distanceThresholdSquare)))
    def validate(self):
        timeStart = time.time()
        imgArray = gdal.Open(Parameters.validationImage).ReadAsArray().astype(np.uint8)
        imgArray = np.transpose(imgArray, (1, 2, 0))
        layer = getLayerByName(Parameters.rgb_image_layername_validation)
        windowArrayList = list()
        windowsCentersList = list()

        pixel_size_x = layer.rasterUnitsPerPixelX()
        pixel_size_y = layer.rasterUnitsPerPixelY()
        top_left_x = layer.extent().xMinimum()
        top_left_y = layer.extent().yMaximum()
        bottom_right_x = layer.extent().xMaximum()
        bottom_right_y = layer.extent().yMinimum()
        dim_x = int((bottom_right_x - top_left_x) / pixel_size_x)
        dim_y = int((top_left_y - bottom_right_y) / pixel_size_y)

        codebook = np.load(Parameters.codebookFileName)

        window_top_left_y = 0
        window_bottom_right_y = 90
        if not (os.path.isfile(Parameters.validationWindowCenterList)
        and os.path.isfile(Parameters.validationFeatures)):
            while window_bottom_right_y < dim_y - Parameters.samplePatchSize:
                window_bottom_right_x = 90
                window_top_left_x = 0
                while (window_bottom_right_x < dim_x - Parameters.samplePatchSize):
                    windowArray = imgArray[window_top_left_y: window_bottom_right_y,
                                  window_top_left_x: window_bottom_right_x, :]
                    windowArrayList.append(windowArray)
                    windowCenterTuple = ((window_top_left_x + Parameters.samplePatchSize / 2),
                                         (window_top_left_y + Parameters.samplePatchSize / 2))
                    windowsCentersList.append(windowCenterTuple)
                    window_top_left_x += Parameters.strideSize
                    window_bottom_right_x += Parameters.strideSize
                window_top_left_y += Parameters.strideSize
                window_bottom_right_y += Parameters.strideSize

            with open(Parameters.validationWindowCenterList, 'w') as f:
                pickle.dump(windowsCentersList, f)

        ################################################
            bovwTestFeatures = extract_bovw_features(windowArrayList, codebook)[0]
            np.save(Parameters.validationFeatures, bovwTestFeatures)
            timeFeaturesCreated = time.time()
            print "windows centers list and bow feautures extracted!"
        else:
            bovwTestFeatures = np.load(Parameters.validationFeatures)
            with open(Parameters.validationWindowCenterList, 'r') as f:
                windowsCentersList = pickle.load(f)
            print "windows center list and bow features loaded!"
        #################################################################

        # predict
        calibrated_svc = joblib.load(Parameters.trainedModelPath)

        predicted_probs = calibrated_svc.predict_proba(bovwTestFeatures)
        predictedLabels = np.argmax(predicted_probs, 1)


        # Load the classification probability map
        predicted_probs_matrix = classification_map.calPredictedProbsMatrix(Parameters.validationImage, predictedLabels, predicted_probs)
        classficationLayer = classification_map.loadRasterLayer(predicted_probs_matrix, Parameters.validationImage, Parameters.rstClassPathextValidation, "probability_map_validation")
        classification_map.styleProbabilityMapRasterLayer(classficationLayer)

        windowNegativeIndexList = list()
        windowPositiveIndexList = list()
        # Separate windows classified as trees or no
        for i, label in enumerate(predictedLabels):
            if label == 0:
                windowNegativeIndexList.append(i)
            else:
                windowPositiveIndexList.append(i)
        self.calRecallValidation(windowsCentersList, windowNegativeIndexList, windowPositiveIndexList)
        np.save(Parameters.predictionLabels_validation, predictedLabels)
        np.save(Parameters.predictionProbs_validation, predicted_probs)


    def autosavePickleFile(self):
        while True:
            if len(self.canvasClicked.annotationCocoList) != 0:
                self.saveAnnotationFile()
            time.sleep(5)

    def tsneVisualization(self):
        # Init the widget
        self.visualization = Visualization(self.config)

        # t-SNE features
        tSNE_features = getTSNEFeatures(self.bovwTrainingFeatures)
        self.visualization.show()
        self.visualization.updateNodes(tSNE_features, labels = self.labelTrainingArray)
        # self.visualization.graph_widget.fitInView()
        self.visualization.exec_()

    #--------------------------------------------------------------------------

    def onClosePlugin(self):
        """Cleanup necessary items here when plugin dockwidget is closed"""

        #print "** CLOSING CoconutTreesDetection"

        # disconnects
        self.dockwidget.closingPlugin.disconnect(self.onClosePlugin)

        # remove this statement if dockwidget is to remain
        # for reuse if plugin is reopened
        # Commented next statement since it causes QGIS crashe
        # when closing the docked window:
        # self.dockwidget = None

        self.pluginIsActive = False


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""

        #print "** UNLOAD CoconutTreesDetection"

        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&CoconutTreesDetection'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

    #--------------------------------------------------------------------------

    def run(self):
        """Run method that loads and starts the plugin"""
        self.dockWidgetAnnotation.show()

        """if not self.pluginIsActive:
            self.pluginIsActive = True

            #print "** STARTING CoconutTreesDetection"

            # dockwidget may not exist if:
            #    first run of plugin
            #    removed on close (see self.onClosePlugin method)
            if self.dockwidget == None:
                # Create the dockwidget (after translation) and keep reference
                #self.dockwidget = CoconutTreesDetectionDockWidget()

            # connect to provide cleanup on closing of dockwidget
            self.dockwidget.closingPlugin.connect(self.onClosePlugin)

            # show the dockwidget
            # TODO: fix to allow choice of dock location
            self.iface.addDockWidget(Qt.RightDockWidgetArea, self.dockwidget)
            self.dockwidget.show()
"""
