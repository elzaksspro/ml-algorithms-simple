#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import multivariate_normal
from sklearn.cross_validation import train_test_split
from collections import defaultdict
from sklearn.metrics import classification_report


def dL(L, i, n_samples, X_train, y_train):
    res = 0
    res = np.sum([L[j] * y_train[i] * y_train[j] * np.dot(X_train[i], X_train[j]) for j in range(n_samples)])
    return (1 - res)


def fit(X_train, y_train, learning_rate=0.02, max_iter=3):
    n_samples, n_features_b = X_train.shape
    L = np.zeros(n_samples)

    iter = 0
    while iter < max_iter:
        for i in range(n_samples):
            L[i] = L[i] + learning_rate * dL(L, i, n_samples, X_train, y_train)
            L[i] = max(L[i], 0)
        iter += 1

    S = [i for i in range(len(L)) if L[i] >= 0.00001]
    w = np.zeros(n_features_b)
    for n in S:
        w += L[n] * y_train[n] * np.array(X_train[n])
    b = w[2]
    np.delete(w, 2, 0)

    model = defaultdict(np.array)
    model['L'] = L
    model['w'] = w
    model['b'] = b

    return model


def predict(model, X_test, y_test):
    pass


def main():
    # load sample data
    X, X_labels = multivariate_normal.load_data_with_label()

    # input data
    n_samples, n_features = X.shape
    X = np.c_[X, np.ones(n_samples)]
    X_train, X_test, y_train, y_test = train_test_split(X, X_labels)

    # training
    model = fit(X_train, y_train)
    print model

    # predict
    pred = predict(model, X_test, y_test)


if __name__ == '__main__':
    main()
