"""Data preprocessing methods.

Authors:
    Keer Ni - knni@ucdavis.edu

"""

"""Missing value imputation methods.

1. KNN
2. missForest

"""

import numpy as np
import copy

from sklearn.impute import KNNImputer

# hyperparameter tuning for missing value imputation

def KNN_impute(re_train_data):
    """Impute missing data using KNN.

    Args:
        re_train_data (list of lists): train data with random removal.

    Returns:
        im_train_data (list of lists): imputed train data.

    """
    X = copy.deepcopy(re_train_data)
    nan = np.nan

    # make np.nan when creating the data directly
    for i in range(len(X)):
        for j in range(len(X[0])):
            if X[i][j] == None:
                X[i][j] = nan

    imputer = KNNImputer(n_neighbors = 5, weights="uniform")
    im_train_data = imputer.fit_transform(X)

    return im_train_data


import sys
import warnings

import sklearn.neighbors._base
sys.modules['sklearn.neighbors.base'] = sklearn.neighbors._base # noqa
from missingpy import MissForest

def MissForest_impute(re_train_data):
    """Impute missing data using MissForest.

    Args:
        re_train_data (list of lists): train data with random removal.

    Returns:
        im_train_data (list of lists): imputed train data.

    """
    X = copy.deepcopy(re_train_data)
    nan = float("NaN")

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")

        for i in range(len(X)):
            for j in range(len(X[0])):
                if X[i][j] == None:
                    X[i][j] = nan

        imputer = MissForest()
        im_train_data = imputer.fit_transform(X)

    return im_train_data



"""Feature scaling methods.

1. MinMax
2. Standardization

"""

from sklearn.preprocessing import MinMaxScaler

def MinMax_scale(im_train_data):
    """Scale data using MinMax.

    Args:
        im_train_data (list of lists): imputed train data.

    Returns:
        sc_train_data (list of lists): scaled train data.

    """
    scaler = MinMaxScaler()

    sc_train_data = scaler.fit(im_train_data).transform(im_train_data)

    return sc_train_data


from sklearn.preprocessing import StandardScaler

def Standardize_scale(im_train_data):
    """Scale data using Standardization.

    Args:
        im_train_data (list of lists): imputed train data.

    Returns:
        sc_train_data (list of lists): scaled train data.

    """
    scaler = StandardScaler()

    sc_train_data = scaler.fit(im_train_data).transform(im_train_data)

    return sc_train_data



"""Outlier detection methods.

1. LOF
2. IsolationForest

"""

from sklearn.neighbors import LocalOutlierFactor

def LOF_outlier(im_train_data):
    """Detect outlier using LOF.

    Args:
        im_train_data (list of lists): imputed train data.

    Returns:
        (list): indices of detected outliers.

    """
    clf = LocalOutlierFactor(n_neighbors=2)

    is_outlier = list(clf.fit_predict(im_train_data))

    return [i for i, x in enumerate(is_outlier) if x != 1]


from sklearn.ensemble import IsolationForest

def IsolationForest_outlier(im_train_data):
    """Detect outlier using IsolationForest.

    Args:
        im_train_data (list of lists): imputed train data.

    Returns:
        (list): indices of detected outliers.

    """
    clf = IsolationForest(random_state=0).fit(im_train_data)

    is_outlier = list(clf.predict(im_train_data))

    return [i for i, x in enumerate(is_outlier) if x != 1]

# PCA
# TSNE // generally better