from django.db import connection

from pandas import read_csv, DataFrame, concat
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler

# Base Classifiers 
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC 

# Ensemble Classifiers 
from sklearn.ensemble import BaggingClassifier, AdaBoostClassifier, StackingClassifier

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, recall_score
from numpy import mean, std

from imblearn.over_sampling import RandomOverSampler
from collections import Counter


def get_columns(file_url):
    data = read_csv(file_url)
    return list(data.columns)

#*****************Read Data*****************

def read_data(file_url):
    dataset = read_csv(file_url)
    
    data = read_csv('heart.csv')
    X = data.drop('HeartDisease', axis=1)  # input
    y = data['HeartDisease']   # output
    oversample = RandomOverSampler(sampling_strategy='minority')
    X_over, y_over = oversample.fit_resample(X, y)

    return X, y


#*****************Data Preprocessing*****************

def data_prep(X_over):
    OHE = OneHotEncoder(handle_unknown='ignore')

    data_sex_OHE = OHE.fit_transform(X_over[['Sex']])
    data_sex_DF = DataFrame(data_sex_OHE.toarray())
    data_sex_DF.columns = OHE.get_feature_names_out()

    data_ChestPainType_OHE = OHE.fit_transform(X_over[['ChestPainType']])
    data_ChestPainType_DF = DataFrame(data_ChestPainType_OHE.toarray())
    data_ChestPainType_DF.columns = OHE.get_feature_names_out()

    data_RestingECG_OHE = OHE.fit_transform(X_over[['RestingECG']])
    data_RestingECG_DF = DataFrame(data_RestingECG_OHE.toarray())
    data_RestingECG_DF.columns = OHE.get_feature_names_out()

    data_ExerciseAngina_OHE = OHE.fit_transform(X_over[['ExerciseAngina']])
    data_ExerciseAngina_DF = DataFrame(data_ExerciseAngina_OHE.toarray())
    data_ExerciseAngina_DF.columns = OHE.get_feature_names_out()

    data_ST_Slope_OHE = OHE.fit_transform(X_over[['ST_Slope']])
    data_ST_Slope_DF = DataFrame(data_ST_Slope_OHE.toarray())
    data_ST_Slope_DF.columns = OHE.get_feature_names_out()

    #***********************Merging multiple DataFrames***********************

    X_binary = concat([data_sex_DF, data_ChestPainType_DF, data_RestingECG_DF, data_ExerciseAngina_DF, data_ST_Slope_DF, X_over[['FastingBS']]], axis=1)
    X_scalable = X_over[['Age', 'RestingBP', 'Cholesterol', 'MaxHR', 'Oldpeak']]  # Orginal numeric columns

    #***********************Applying MinMaxScaler***********************

    X_scaled = MinMaxScaler().fit_transform(X_scalable)
    X_scaled_DF = DataFrame(X_scaled)
    X_scaled_DF.columns = X_scalable.columns

    X_PREP = concat([X_scalable, X_binary], axis=1)  # Prepared Data

    return X_PREP


#*****************get_base_models() Defination*****************

def get_base_models():
    models = dict()
    models['dt_ent'] = DecisionTreeClassifier(criterion='entropy')
    models['dt_gini'] = DecisionTreeClassifier(criterion='gini')
    models['lr'] = LogisticRegression(max_iter=10000)
    models['svc_linear'] = SVC(kernel='linear')
    models['svc_rbf'] = SVC()
    models['svc_sigmoid'] = SVC(kernel='sigmoid')
    models['svc_poly'] = SVC(kernel='poly')
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