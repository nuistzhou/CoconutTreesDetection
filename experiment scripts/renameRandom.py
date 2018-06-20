import os

path = '/Users/ping/Documents/thesis/data/patchImages/upper/random'
path_labelled = '/Users/ping/Documents/thesis/data/patchImages/upper/random_copy'

filenames = [f for f in os.listdir(path) if not f.startswith('.')]
filenames.sort()

for filename in filenames:
    filenameIndex = int(filename[:4]) + 1631
    filenameNew = str(filenameIndex) + '.png'
    os.rename(os.path.join(path, filename), os.path.join(path_labelled, filenameNew))
#
# path = '/Users/ping/thesis/data/patchImages/upper/random'
# path_labelled = '/Users/ping/thesis/data/patchImages/upper/random_labelled'
# filenames = [f for f in os.listdir(path) if not f.startswith('.')]
# filenames.sort()
#
# for filename in filenames:
#     filenameIndex = int(filename[:4]) + 1632
#     filenameNew = '0_' + str(filenameIndex) + '.png'
#     print filenameNew
#     os.rename(os.path.join(path, filename), os.path.join(path_labelled, filenameNew))

