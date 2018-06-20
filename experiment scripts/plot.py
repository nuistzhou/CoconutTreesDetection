import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
from matplotlib.pyplot import style
from matplotlib import ticker
from matplotlib.font_manager import FontProperties


# # Create 3 x 1 sub plots
# gs = gridspec.GridSpec(3, 2)
style.use('seaborn-notebook')
# fontP = FontProperties()
# fontP.set_size('small')
#
# recallLinearSVM = [0.84, 0.65, 0.83, 0.85, 0.91]
# recallRBF_SVM = [0.90, 0.88, 0.92, 0.83, 0.91]
# recallRF = [0.85, 0.72, 0.82, 0.84, 0.92]
#
# precisionLinearSVM = [0.91, 0.87, 0.91, 0.86, 0.91]
# precisionRBF_SVM = [0.84, 0.89, 0.92, 0.85, 0.91]
# precisionRF = [0.92, 0.88, 0.92, 0.82, 0.91]
#
# fscoreLinearSVM = [0.88, 0.74, 0.87, 0.85, 0.91]
# fscoreRBF_SVM = [0.91, 0.88, 0.92, 0.84, 0.91]
# fscoreRF = [0.89, 0.79, 0.87, 0.83, 0.91]
#
# # Recall
# recallHog = [recallLinearSVM[0], recallRBF_SVM[0], recallRF[0]]
# recallSURF = [recallLinearSVM[1], recallRBF_SVM[1], recallRF[1]]
# recallSIFT = [recallLinearSVM[2], recallRBF_SVM[2], recallRF[2]]
# recallBoVW_SUFR = [recallLinearSVM[3], recallRBF_SVM[3], recallRF[3]]
# recallBoVW_SIFT = [recallLinearSVM[4], recallRBF_SVM[4], recallRF[4]]
#
# # Precision
# precisionHog = [precisionLinearSVM[0], precisionRBF_SVM[0], precisionRF[0]]
# precisionSURF = [precisionLinearSVM[1], precisionRBF_SVM[1], precisionRF[1]]
# precisionSIFT = [precisionLinearSVM[2], precisionRBF_SVM[2], precisionRF[2]]
# precisionBoVW_SUFR = [precisionLinearSVM[3], precisionRBF_SVM[3], precisionRF[3]]
# precisionBoVW_SIFT = [precisionLinearSVM[4], precisionRBF_SVM[4], precisionRF[4]]
#
# # F-score
# fscoreHog = [fscoreLinearSVM[0], fscoreRBF_SVM[0], fscoreRF[0]]
# fscoreSURF = [fscoreLinearSVM[1], fscoreRBF_SVM[1], fscoreRF[1]]
# fscoreSIFT = [fscoreLinearSVM[2], fscoreRBF_SVM[2], fscoreRF[2]]
# fscoreBoVW_SUFR = [fscoreLinearSVM[3], fscoreRBF_SVM[3], fscoreRF[3]]
# fscoreBoVW_SIFT = [fscoreLinearSVM[4], fscoreRBF_SVM[4], fscoreRF[4]]
#
#
# plt.figure()
# ngroups = 3
#
# # Recall
# ax  = plt.subplot(gs[0, :])
# index = np.arange(ngroups)
# bar_width = 0.15
# opacity = 0.6
# plt.ylim(ymin = 0.6)
# plt.grid(True, axis = 'y', linestyle='--', alpha = 0.4)
#
# rectRecallHOG = ax.bar(index, recallHog, bar_width, alpha = opacity, label ="HOG")
# rectRecallSURF = ax.bar(index + bar_width, recallSURF, bar_width, alpha = opacity,  label ="SURF")
# rectRecallSIFT = ax.bar(index + bar_width * 2, recallSIFT, bar_width, alpha = opacity, label ="SIFT")
# rectRecallBoVWSURF = ax.bar(index + bar_width * 3, recallBoVW_SUFR, bar_width, alpha = opacity, label ="BoVW-SURF")
# rectRecallBoVWSIFT = ax.bar(index + bar_width * 4, recallBoVW_SIFT, bar_width, alpha = opacity,  label ="BoVW-SIFT")
#
# # pltRecall.set_xlabel("Classifiers and Feature Descriptors")
# ax.set_ylabel("Recall")
# # pltRecall.set_title("Performance of different feature descriptors")
# # pltRecall.set_xticks(index + bar_width / 2)
# ax.set_xticks([])
# plt.tick_params(
#     axis='x',          # changes apply to the x-axis
#     which='both',      # both major and minor ticks are affected
#     bottom=False,      # ticks along the bottom edge are off
#     top=False) # labels along the bottom edge are off
# # pltRecall.set_xticklabels(("Linear-SVM", "Kernel-SVM", "Random Forest"), ha ='left')
#
# # Shrink current axis by 20%
# box = ax.get_position()
# ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
#
# # Precision
# ax  = plt.subplot(gs[1, :])
# index = np.arange(ngroups)
# bar_width = 0.15
# opacity = 0.6
# plt.ylim(ymin = 0.6)
# plt.grid(True, axis = 'y', linestyle='--', alpha = 0.4)
#
# rectPrecisionHOG = ax.bar(index, precisionHog, bar_width, alpha = opacity,  label ="HOG")
# rectPrecisionSURF = ax.bar(index + bar_width, precisionSURF, bar_width, alpha = opacity,  label ="SURF")
# rectPrecisionSIFT = ax.bar(index + bar_width * 2, precisionSIFT, bar_width, alpha = opacity, label ="SIFT")
# rectPrecisionBoVWSURF = ax.bar(index + bar_width * 3, precisionBoVW_SUFR, bar_width, alpha = opacity, label ="BoVW-SURF")
# rectPrecisionBoVWSIFT = ax.bar(index + bar_width * 4, precisionBoVW_SIFT, bar_width, alpha = opacity, label ="BoVW-SIFT")
#
# # pltPrecision.set_xlabel("Classifiers and Feature Descriptors")
# ax.set_ylabel("Precision")
# # pltPrecision.set_title("Performance of different feature descriptors")
# ax.set_xticks([])
# # pltPrecision.set_xticklabels(("Linear-SVM", "Kernel-SVM", "Random Forest"), ha ='left')
# # Shrink current axis by 20%
# box = ax.get_position()
# ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
# plt.tick_params(
#     axis='x',          # changes apply to the x-axis
#     which='both',      # both major and minor ticks are affected
#     bottom=False,      # ticks along the bottom edge are off
#     top=False) # labels along the bottom edge are off
#
#
# # F-score
# ax  = plt.subplot(gs[2, :])
# index = np.arange(ngroups)
# bar_width = 0.15
# opacity = 0.6
# plt.ylim(ymin = 0.6)
# plt.grid(True, axis = 'y', linestyle='--', alpha = 0.4)
#
# rectFscoreHOG = ax.bar(index, fscoreHog, bar_width, alpha = opacity,  label ="HOG")
# rectFscoreSURF = ax.bar(index + bar_width, fscoreSURF, bar_width, alpha = opacity,  label ="SURF")
# rectFscoreSIFT = ax.bar(index + bar_width * 2, fscoreSIFT, bar_width, alpha = opacity,  label ="SIFT")
# rectFscoreBoVWSURF = ax.bar(index + bar_width * 3, fscoreBoVW_SUFR, bar_width, alpha = opacity, label ="BoVW-SURF")
# rectFscoreBoVWSIFT = ax.bar(index + bar_width * 4, fscoreBoVW_SIFT, bar_width, alpha = opacity,  label ="BoVW-SIFT")
#
# ax.set_xlabel("Classifiers and feature descriptors performance test")
# ax.set_ylabel("F-score")
# # pltPrecision.set_title("Performance of different feature descriptors")
# ax.set_xticks(index + bar_width)
# ax.set_xticklabels(("Linear-SVM", "Kernel-SVM", "Random Forest"), ha ='left')
#
# # Shrink current axis by 20%
# box = ax.get_position()
# ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
# plt.tick_params(
#     axis='x',          # changes apply to the x-axis
#     which='both',      # both major and minor ticks are affected
#     bottom=False,      # ticks along the bottom edge are off
#     top=False) # labels along the bottom edge are off
#
#
# # Put a legend to the right of the current axis
# ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
#
#
# plt.show()


#----------------------------------------------------------------
# recall = [1, 1, 1, 0.9, 0.63, 0.44, 0.32, 0.25, 0.19]
# strideSize = ['5', '10', '15', '20', '25', '30', '35', '40', '45']
# fig, ax = plt.subplots()
# plt.bar(strideSize, recall)
# plt.xticks(strideSize, ['5', '10', '15', '20', '25', '30', '35', '40', '45'])
# ax.set_xlabel("Stride size (pixels)")
# ax.set_ylabel("Recall")
# ax.set_title("Recall of different stride size")
#
# plt.tick_params(
#     axis='x',          # changes apply to the x-axis
#     which='both',      # both major and minor ticks are affected
#     bottom=False,      # ticks along the bottom edge are off
#     top=False) # labels along the bottom edge are off
# plt.show()

#----------------------------------------------------------------
# gridsearchRecall = [1, 1, 1, 0.9, 0.63, 0.44, 0.32, 0.25, 0.19]
# gridsearchNrPatches = [376585, 94146, 41843, 23537, 15063, 10461, 7685, 5884, 4649]
# templatematchingRecall = [0.85, 0.64, 0.47, 0.38]
# templatematchingNrPatches = [1304307, 157849, 54148, 29914]
# fig, ax = plt.subplots()
# ax.scatter(gridsearchRecall, gridsearchNrPatches, marker = 'o', label = 'Grid Search')
# ax.plot(gridsearchRecall, gridsearchNrPatches)
#
# ax.scatter(templatematchingRecall, templatematchingNrPatches, marker = '^', label = 'Template Matching')
# ax.plot(templatematchingRecall, templatematchingNrPatches)
# plt.ylim((0, 1400000))
# plt.xlim(0, 1)
# plt.grid(True, axis = 'y', linestyle='--', alpha = 0.4)
# ax.set_xlabel("Recall")
# ax.set_ylabel("Number of Patches")
#
# ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda y, p: format(int(y), ',')))
# ax.legend()
# plt.show()

##--------------------------feature descriptor and classifier time cost--------------------------------------
linearSVM = [5.3329, 0.0029]
svm = [1981.27, 4.1905]
rf = [70.5856, 0.7596]
plt.figure()
ngroups = 2

ax  = plt.subplot()
index = np.arange(ngroups)
bar_width = 0.15
opacity = 0.6
plt.grid(True, axis = 'y', linestyle='--', alpha = 0.4)

rectRecallHOG = ax.bar(index, linearSVM, bar_width, alpha = opacity, label ="Linear-SVM")
rectRecallSURF = ax.bar(index + bar_width, svm, bar_width, alpha = opacity,  label ="Kernel-SVM")
rectRecallSIFT = ax.bar(index + bar_width * 2, rf, bar_width, alpha = opacity, label ="Random Forest")

# pltRecall.set_xlabel("Classifiers and Feature Descriptors")
ax.set_ylabel("Time (second)")
# pltRecall.set_title("Performance of different feature descriptors")
# pltRecall.set_xticks(index + bar_width / 2)
ax.set_xticks([])
plt.tick_params(
    axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom=False,      # ticks along the bottom edge are off
    top=False) # labels along the bottom edge are off
ax.set_xticklabels(("Train", "Predict"), ha ='left')
ax.yaxis.get_major_formatter().set_powerlimits((0,1))
# Shrink current axis by 20%
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
# ax.set_xlabel("Recall")

ax.legend()
plt.show()