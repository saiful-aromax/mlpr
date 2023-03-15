from django.db import connection
from pandas import read_csv
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, recall_score
from numpy import mean
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC


def get_columns(file_url):
    data = read_csv(file_url)
    return list(data.columns)


def data_prep(file_url, y_value):
    dataset = read_csv(file_url)
    X = dataset.drop(y_value, axis=1)  # matrix of input variables
    y = dataset[y_value]  # output variable
    return X, y


def get_models():
    models = dict()
    models['dt_ent'] = DecisionTreeClassifier(criterion='entropy')
    models['dt_gini'] = DecisionTreeClassifier(criterion='gini')
    models['lr'] = LogisticRegression(max_iter=10000)
    models['svc_l'] = SVC(kernel='linear')
    # models['svc_r'] = SVC()
    # models['svc_s'] = SVC(kernel='sigmoid')
    # models['svc_p'] = SVC(kernel='poly')
    return models

def evaluate_model_mc(model, X, y, mc, split):
    accuracy = [] 
    for i in range(mc):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=split)  # split dataset
        m = model.fit(X_train, y_train)  # fit the model
        prediction = m.predict(X_test)  # prediction
        accuracy.append(accuracy_score(y_test, prediction))  # compute & append accuracy
        return mean(accuracy)
    
def model_score_mc(file_url, y_value, mc, split):
    dataset = read_csv(file_url)
    X = dataset.drop(y_value, axis=1)  # matrix of input variables
    y = dataset[y_value]  # output variable
    models = get_models()
    # evaluate the models and store results
    results, names = list(), list()
    output = dict()
    for name, model in models.items():
        scores = evaluate_model_mc(model, X, y, mc, split)
        output[name] = scores
    return output