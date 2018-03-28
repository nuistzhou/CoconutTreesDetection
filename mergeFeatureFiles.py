import argparse
import numpy as np

def main():

	parser = argparse.ArgumentParser()
	parser.add_argument("non_coco_features_filename", type=str, help="Label filename (*.npy)")
	parser.add_argument("coco_features_filename", type=str, help="Dataset file name (*.npy)")
	parser.add_argument("output_features_filename", type=str, help="Output features filename (*.npy)")
	parser.add_argument("output_labels_filename", type=str, help="Output features filename (*.npy)")
	args = parser.parse_args()

	non_coco_features_filename = args.non_coco_features_filename
	coco_features_filename = args.coco_features_filename
	output_features_filename = args.output_features_filename
	output_labels_filename = args.output_labels_filename

	non_coco_features = np.load(non_coco_features_filename)
	coco_features = np.load(coco_features_filename)

	num_non_coco = len(non_coco_features)
	num_coco = len(coco_features)

	feature_size = non_coco_features.shape[1]

	output_features = np.zeros((num_non_coco+num_coco, feature_size))
	output_labels = np.zeros(num_non_coco+num_coco)

	output_features[:num_non_coco, :] = non_coco_features
	output_features[num_non_coco:, :] = coco_features

	output_labels[:num_non_coco] = 0
	output_labels[num_non_coco:] = 1

	np.save(output_features_filename, output_features)
	np.save(output_labels_filename, output_labels)


if __name__ == '__main__':
	main()