from os import listdir
from os.path import join, isdir, dirname, normpath, abspath
import re
import pandas as pd
import numpy as np
from model import Model

# Load data
print 'Loading data...'

rx_filename = re.compile('^.*\d+\.txt$')

texts = []
labels = np.array([], dtype=np.uint8)
label_names = []

datadir = normpath(join(abspath(dirname(__file__)), '../data/livedoornews'))
subdirs = listdir(datadir)
label = 0
for subdir in subdirs:
    subdir_path = join(datadir, subdir)
    if not isdir(subdir_path):
        continue

    texts_of_this_label = []
    textfiles = listdir(subdir_path)
    for j, textfile in enumerate(textfiles):
        if not rx_filename.match(textfile):
            continue

        textfile_path = join(subdir_path, textfile)

        with open(textfile_path, 'r') as f:
            texts_of_this_label.append(f.read())

    texts.extend(texts_of_this_label)
    labels = np.hstack((
        labels,
        np.ones(len(texts_of_this_label), dtype=np.uint8) * label
    ))
    label_names.append(subdir)

    label += 1
    print subdir

# Train
print 'Training...'
np.random.seed(42)
indices = np.random.permutation(len(texts))
X = pd.Series(texts)[indices]
Y = labels[indices]

# n_test = 500
n_test = 0  # For production
X_test = X[:n_test]
X_train = X[n_test:]
Y_test = Y[:n_test]
Y_train = Y[n_test:]

model = Model()
model.fit(X_train, Y_train)
model.set_label_names(label_names)
model.save()
