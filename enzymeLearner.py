#March 29, 2019
#Alex Muralles
#EnzymeLearner.py

#Train an active learning algorithm to identify placental (1) vs bacterial (0) alkaline phosphatases based on 
#substrate-dependent enzyme velocity. 


import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from modAL.uncertainty import uncertainty_sampling
from modAL.models import ActiveLearner
import matplotlib.pyplot as plt





def loadData(filename):
#Process data from a CSV
    data = pd.read_csv(filename)
    X = data.iloc[:,:2].values
    y = LabelEncoder().fit_transform(data.iloc[:,-1])

    return X, y

def make_active_learner(estimator,X_training,y_training,query_strategy=uncertainty_sampling,random_state=0):

    learner = ActiveLearner(
        estimator = estimator,
        query_strategy = query_strategy,
        X_training = X_training,
        y_training = y_training
    )

    return learner

def split_data(X,y,random_state=0):

    X_training, y_training = [], []

    for i in range(int(len(y)/5)):

        #Implementation left this way to allow for random selection of i, potential addition in future updates
        xx = X[i]
        X_training.append(xx)
        y_training.append(i)
        X, y = np.delete(X, i, axis=0), np.delete(y, i, axis=0)

    X_pool, X_test, y_pool, y_test = train_test_split(X,y,test_size=0.5,random_state=random_state)

    return np.asarray(X_training), X_pool, np.asarray(y_training), y_pool, X_test, y_test


def Learner(X,y):
    X_training, X_pool, y_training, y_pool, X_test, y_test = split_data(X,y)

    accuracies = []

    uncertainty_sampler = make_active_learner(RandomForestClassifier(random_state=0),X_training,y_training,uncertainty_sampling)

    while X_pool.size != 0:
        accuracies.append(uncertainty_sampler.score(X_test,y_test))
        idx, sample = uncertainty_sampler.query(X_pool)
        label = y_pool[idx]

        uncertainty_sampler.teach(sample,label)
        X_pool = np.delete(X_pool, idx,0)
        y_pool = np.delete(y_pool, idx, 0)

    accuracies.append(uncertainty_sampler.score(X_test,y_test))

    return accuracies


def plotData(accuracies):
    x_axis = range(0,len(accuracies))
    plt.plot(x_axis,accuracies)
    plt.xlabel("Query number")
    plt.ylabel("Test accuracy")
    plt.title("Learning")
    plt.show()

#Things to try

#1. The current setup for selecting training data isn't random, it would be interesting to compare different
#Splits in testing vs. training data. It's known that this effects the learner (obviously) but seeing it with
#this data would be neat to tryself.

#2. Compare the available samplers

#3. Create my own sampler


if __name__ == '__main__':

    X,y = loadData("BioRadAssayData.csv")
    accuracies = Learner(X,y)
    plotData(accuracies)
