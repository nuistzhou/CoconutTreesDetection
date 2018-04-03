import argparse
import os
import numpy as np
from config import Parameters
"""
python mergeFeatureFiles.py ~/featureDescriptors/hog_lower_non_coco.npy ~/featureDescriptors/hog_lower_coco.npy ~/featureDescriptors/merged_features/hog_lower_features.npy ~/featureDescriptors/merged_features/hog_lower_labels.npy
python mergeFeatureFiles.py ~/featureDescriptors/sift_lower_non_coco.npy ~/featureDescriptors/sift_lower_coco.npy ~/featureDescriptors/merged_features/sift_lower_features.npy ~/featureDescriptors/merged_features/sift_lower_labels.npy
python mergeFeatureFiles.py ~/featureDescriptors/surf_lower_non_coco.npy ~/featureDescriptors/surf_lower_coco.npy ~/featureDescriptors/merged_features/surf_lower_features.npy ~/featureDescriptors/merged_features/surf_lower_labels.npy
python mergeFeatureFiles.py ~/featureDescriptors/hog_upper_non_coco.npy ~/featureDescriptors/hog_upper_coco.npy ~/featureDescriptors/merged_features/hog_upper_features.npy ~/featureDescriptors/merged_features/hog_upper_labels.npy
python mergeFeatureFiles.py ~/featureDescriptors/sift_upper_non_coco.npy ~/featureDescriptors/sift_upper_coco.npy ~/featureDescriptors/merged_features/sift_upper_features.npy ~/featureDescriptors/merged_features/sift_upper_labels.npy
python mergeFeatureFiles.py ~/featureDescriptors/surf_upper_non_coco.npy ~/featureDescriptors/surf_upper_coco.npy ~/featureDescriptors/merged_features/surf_upper_features.npy ~/featureDescriptors/merged_features/surf_upper_labels.npy
"""

def createFullPath(file_path):
    return os.path.join(Parameters.dataPath, file_path)

def main(non_coco_features_filename, coco_features_filename,
         output_features_filename, output_labels_filename):
    # parser = argparse.ArgumentParser()
    # parser.add_argument("non_coco_features_filename", type=str, help="Label filename (*.npy)")
    # parser.add_argument("coco_features_filename", type=str, help="Dataset file name (*.npy)")
    # parser.add_argument("output_features_filename", type=str, help="Output features filename (*.npy)")
    # parser.add_argument("output_labels_filename", type=str, help="Output features filename (*.npy)")
    # args = parser.parse_args()

    # non_coco_features_filename = args.non_coco_features_filename
    # coco_features_filename = args.coco_features_filename
    # output_features_filename = args.output_features_filename
    # output_labels_filename = args.output_labels_filename
    output_features_filename = createFullPath(output_features_filename)
    output_labels_filename = createFullPath(output_labels_filename)
    coco_features_filename = createFullPath(coco_features_filename)
    non_coco_features_filename = createFullPath(non_coco_features_filename)


    non_coco_features = np.load(non_coco_features_filename)
    coco_features = np.load(coco_features_filename)

    num_non_coco = len(non_coco_features)
    num_coco = len(coco_features)

    feature_size = non_coco_features.shape[1]

    output_features = np.zeros((num_non_coco + num_coco, feature_size))
    output_labels = np.zeros(num_non_coco + num_coco)

    output_features[:num_non_coco, :] = non_coco_features
    output_features[num_non_coco:, :] = coco_features

    output_labels[:num_non_coco] = 0
    output_labels[num_non_coco:] = 1

    np.save(output_features_filename, output_features)
    np.save(output_labels_filename, output_labels)


if __name__ == '__main__':
    main("featureDescriptors/hog_lower_non_coco.npy", "featureDescriptors/hog_lower_coco.npy",
         "featureDescriptors/merged_features/hog_lower_features.npy", "featureDescriptors/merged_features/hog_lower_labels.npy")
    main("featureDescriptors/sift_lower_non_coco.npy", "featureDescriptors/sift_lower_coco.npy",
         "featureDescriptors/merged_features/sift_lower_features.npy", "featureDescriptors/merged_features/sift_lower_labels.npy")
    main("featureDescriptors/surf_lower_non_coco.npy", "featureDescriptors/surf_lower_coco.npy",
         "featureDescriptors/merged_features/surf_lower_features.npy", "featureDescriptors/merged_features/surf_lower_labels.npy")
    main("featureDescriptors/hog_upper_non_coco.npy", "featureDescriptors/hog_upper_coco.npy",
         "featureDescriptors/merged_features/hog_upper_features.npy", "featureDescriptors/merged_features/hog_upper_labels.npy")
    main("featureDescriptors/sift_upper_non_coco.npy", "featureDescriptors/sift_upper_coco.npy",
         "featureDescriptors/merged_features/sift_upper_features.npy", "featureDescriptors/merged_features/sift_upper_labels.npy")
    main("featureDescriptors/surf_upper_non_coco.npy", "featureDescriptors/surf_upper_coco.npy",
         "featureDescriptors/merged_features/surf_upper_features.npy", "featureDescriptors/merged_features/surf_upper_labels.npy")