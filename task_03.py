# -*- coding: utf-8 -*-
"""Task_03.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1R06DgG-kC12GXuqz6PB-38zv8mPGHZej
"""

from zipfile import ZipFile

dataset="train.zip"

with ZipFile(dataset, 'r') as zip:
    zip.extractall()

import os
import numpy as np
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
from tqdm import tqdm
import joblib
from sklearn.model_selection import GridSearchCV
import cv2
import seaborn as sns
import time
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split

folder_path = f"Dataset/"
os.makedirs(folder_path, exist_ok=True)

#path
confusion_image_path = os.path.join(folder_path, 'confusion matrix.png')
classification_file_path = os.path.join(folder_path, 'classification_report.txt')
model_file_path = os.path.join(folder_path, "svm_model.pkl")

# Path dataset directory
dataset_dir = "Dataset/"
train_dir = os.path.join(dataset_dir, "train")
test_dir = os.path.join(dataset_dir, "test1")

train_images = os.listdir(train_dir)
features = []
labels = []
image_size = (50, 50)


for image in tqdm(train_images, desc="Processing Train Images"):
    if image[0:3] == 'cat' :
        label = 0
    else :
        label = 1
    image_read = cv2.imread(train_dir+"/"+image)
    image_resized = cv2.resize(image_read, image_size)
    image_normalized = image_resized / 255.0
    image_flatten = image_normalized.flatten()
    features.append(image_flatten)
    labels.append(label)

del train_images

features = np.asarray(features)
labels = np.asarray(labels)

X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, shuffle=True, random_state=40)

del features
del labels

nb_components = 0.7
pca = PCA(nb_components=n_components)
svm = SVC()
pca = PCA(nb_components=nb_components, random_state=4042)
pipeline = Pipeline([
    ('pca', pca),
    ('svm', svm)
])

prm_grid = {
    'pca__n_components': [2, 1, 0.9, 0.8],
    'svm__kernel': ['linear', 'rbf', 'poly', 'sigmoid'],
}

start_time = time.time()
pipeline = Pipeline([
    ('vect', CountVectorizer()),
    ('tfidf', TfidfTransformer()),
    ('clf', MultinomialNB()),
])
grid_search = GridSearchCV(pipeline, prm_grid, cv=3, verbose=4)
grid_search.fit(X_train, y_train)
end_time = time.time()

del X_train
del y_train

best_pipeline = grid_search.best_estimator_
best_prms = grid_search.best_params_
best_score = grid_search.best_score_

print("Best Parameters: ", best_prms)
print("Best Score: ", best_score)

accuracy = best_pipeline.score(X_test, y_test)
print("Accuracy:", accuracy)

y_pred = best_pipeline.predict(X_test)
target_names = ['Cat', 'Dog']
classification_rep = classification_report(y_test, y_pred, target_names=target_names)
print("Classification Report:", classification_rep)

with open(classification_file_path, 'w') as file:
    file.write(classification_rep)

c = confusion_matrix(y_test, y_pred)
sns.heatmap(c, annot=True, fm="pink", cmap="B")
plt.xlabel('Predicted labels')
plt.ylabel('True labels')
plt.savefig(confusion_image_path)
plt.show()