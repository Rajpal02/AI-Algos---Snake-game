# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 16:46:04 2022

@author: shriya
"""

import numpy as np

n1 = 7
n2 = 9
n3 = 15
n4 = 3

def weight_from_nn(individual):
    W1 = individual[0:n2 * n1]
    W2 = individual[n2 * n1:n3 * n2 + n2 * n1]
    W3 = individual[n3 * n2 + n2 * n1:]
    return (W1.reshape(n2, n1), W2.reshape(n3, n2), W3.reshape(n4, n3))

def sigmoid(x):
    #sigmoid function
    s = 1 / (1 + np.exp(-x))
    return s

def softmax(x):
    s = np.exp(x.T) / np.sum(np.exp(x.T), axis=1).reshape(-1, 1)
    return s

def feed_forward(X, individual):
    W1, W2, W3 = weight_from_nn(individual)
    #matrix multiplication with weight
    X1 = np.tanh(np.matmul(W1, X.T))
    X2 = np.tanh(np.matmul(W2, X1))
    X3 = softmax(np.matmul(W3, X2))
    return X3