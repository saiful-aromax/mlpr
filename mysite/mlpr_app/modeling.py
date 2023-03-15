from django.db import connection

# Import neccessary library
from statistics import mean
from statsmodels.api import GLM, add_constant, families
from pandas import read_csv, DataFrame, concat
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from math import sqrt

def get_columns(file_url):
    data = read_csv(file_url)
    return list(data.columns)

def data_prep(file_url, y):
    data = read_csv(file_url)
    return ""