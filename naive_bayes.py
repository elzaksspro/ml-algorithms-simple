#!/usr/bin/env python
# -*- coding: utf-8 -*-

import multivariate_normal
from sklearn.cross_validation import train_test_split
import numpy as np
from collections import defaultdict
import scipy.stats


def train(X_train, y_train):
    n_labels = max(y_train)+1
    n_features = X_train.shape[1]
    N = X_train.shape[0]
    N_l = np.array([(y_train == y).sum() for y in range(n_labels)],
                   dtype=np.float)

    mean = np.zeros((n_labels, n_features), dtype=np.float)
    for y in range(n_labels):
        sum = np.sum(X_train[n] if y_train[n] == y else 0.0 for n in range(N))
        mean[y] = sum / N_l[y]

    var = np.zeros((n_labels, n_features), dtype=np.float)
    for y in range(n_labels):
        sum = np.sum((X_train[n] - mean[y])**2 if y_train[n] == y else 0.0 for n in range(N))
        var[y] = sum / N_l[y]

    pi = np.zeros(n_labels, dtype=np.float)
    pi = N_l / N

    return (mean, var, pi)


def log_gaussian_wrap(x, mean, var):
    epsilon = 1.0e-5
    if var < epsilon:
        return 0.0
    return scipy.stats.norm(mean, var).logpdf(x)


def negative_log_likelihood(model, X, y):
    n_features = X.shape[1]
    log_prior_y = -np.log(model['pi'][y])
    log_posterior_x_given_y = -np.sum([log_gaussian_wrap(X[d], model['mean'][y][d], model['var'][y][d]) for d in range(n_features)])
    return log_prior_y + log_posterior_x_given_y


def fit(model, X_test, y_test):
    n_labels = max(y_test) + 1
    results = [negative_log_likelihood(model, X_test, y) for y in range(n_labels)]
    return np.argmin(results)


def main():
    # load sample data
    X, X_labels = multivariate_normal.load_data_with_label()

    # training
    X_train, X_test, y_train, y_test = train_test_split(X, X_labels)
    mean, var, pi = train(X_train, y_train)
    print 'mean', mean
    print 'var', var
    print 'pi', pi

    model = defaultdict(np.array)
    model['mean'] = mean
    model['var'] = var
    model['pi'] = pi

    # predict
    pred = fit(model, X_test, y_test)
    print pred

if __name__ == '__main__':
    main()
