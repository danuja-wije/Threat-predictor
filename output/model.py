# Libraries

# Operations (numarical) 
import numpy as np
# Ploting Process
import matplotlib.pyplot as plt
# Data set managment
import pandas as pd
import seaborn as sns

# Dataset loading
dataset = pd.read_excel('Data.xlsx')

dataset.head()

# Taking Care of Empty Cells
dataset.fillna(value='Not Assigned', inplace=True)



from sklearn.utils import resample

# Separate majority and minority classes
Citical_level = dataset[dataset.THREAT_LEVEL == 'CRITICAL']
High_level = dataset[dataset.THREAT_LEVEL == 'HIGH']
Low_level = dataset[dataset.THREAT_LEVEL == 'LOW']
Medium_level = dataset[dataset.THREAT_LEVEL == 'MEDIUM']
Threat_level = dataset[dataset.THREAT_LEVEL == 'NO THREAT']

# Upsample mild class
Citical_level_upsampled = resample(Citical_level,
                                   replace=True,  # sample with replacement
                                   n_samples=200  # to match majority class
                                   )

# Upsample mild class
High_level_upsampled = resample(High_level,
                                replace=True,  # sample with replacement
                                n_samples=200  # to match majority class
                                )

# Upsample ModerateDR class
Low_level_upsampled = resample(Low_level,
                               replace=True,  # sample with replacement
                               n_samples=200  # to match majority class
                               )

# Upsample SevereDR class
Medium_level_upsampled = resample(Medium_level,
                                  replace=True,  # sample with replacement
                                  n_samples=200  # to match majority class
                                  )

# Upsample PDR class
Threat_level_upsampled = resample(Threat_level,
                                  replace=True,  # sample with replacement
                                  n_samples=200  # to match majority class
                                  )

# Combine majority class with upsampled minority class
df_upsampled = pd.concat([Citical_level_upsampled, High_level_upsampled, Low_level_upsampled, Medium_level_upsampled,
                          Threat_level_upsampled])

df4 = df_upsampled.sample(frac=1, replace=False, random_state=42)

y = df4.iloc[:, 19]


df4.drop('THREAT_LEVEL', axis='columns', inplace=True)

# Handling Empty Cells
df4.fillna(value='Not Assigned', inplace=True)

cols = df4.columns

# Labeling

# Importing Libraries
from sklearn.preprocessing import LabelEncoder

encode = LabelEncoder()
encoded = list()

# Labeling X
for i in cols:
    p = df4[i].unique()
    df4[i] = encode.fit_transform(df4[i])
    e = df4[i].unique()
    t = dict()
    for j in range(len(p)):
        t[p[j]] = e[j]
    encoded.append(t)
# Labeling y    
test = np.unique(y)
y = encode.fit_transform(y)
test2 = np.unique(y)

encodeY = dict()
flag = 0
for i in test2:
    encodeY[i] = test[flag]
    flag += 1

# Defining Input and Outputs
X = df4.iloc[:, 0:19]

# Splitting the data into training and Testing sets

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# Feature scalling

# Processing Libraries
from sklearn.preprocessing import StandardScaler

# Scalling training and test sets of X
sc_X = StandardScaler()
X_train = sc_X.fit_transform(X_train)
X_test = sc_X.transform(X_test)

X_train[0]

# Fitting the data set with XGboost
# installing xgboost

from xgboost import XGBClassifier

classifier_Xgboost = XGBClassifier(n_estimators=350, max_depth=5, learning_rate=0.116,
                                   colsample_bytree=0.8)  # polsample 0.8 
classifier_Xgboost.fit(X_train, y_train)

print(X_test)
# Testing values
y_pred = classifier_Xgboost.predict(X_test)

# making the confusion matrix
from sklearn.metrics import confusion_matrix

cm = confusion_matrix(y_test, y_pred)

# calculating Acccuracy score
from sklearn.metrics import accuracy_score

#print("Accuracy is ", accuracy_score(y_test, y_pred) * 100)

def model_pred(ip_address, threat_type, action_performed, action_error, cirucmstance_name, flags,
               threat_content_type, tcp_tunnel_status, alert_type, category, severity_occurrence, action,session_end_reason,severity,Action_performed, process_name,
               mallicious_ip, malware_rule, main_class_name):
    # toPredict = ['126.49.253.66', 'Warning', 'trojan', 'Cleaned Failed', 'Error while cleaning',
    #              'Event occurred on a newly created file',
    #              'Not Assigned', 'Not Assigned', 'Not Assigned', 'Not Assigned', 'Not Assigned', 'Not Assigned',
    #              'Not Assigned', 'Not Assigned', 'Not Assigned',
    #              'Alert_Allow', 'Signature Detection ', 'Not Assigned', 'HTTP Illegal Header']
    toPredict = [ip_address, severity_occurrence,threat_type, action_performed, action_error, cirucmstance_name, flags,
               threat_content_type, action,session_end_reason,severity,Action_performed, process_name,mallicious_ip, tcp_tunnel_status, alert_type, category,malware_rule,
                 main_class_name]

    encodePred = list()
    count = 0
    for i in encoded:
        encodePred.append(i[toPredict[count]])
        count += 1
    encodePred = [encodePred]
    y_prediction = classifier_Xgboost.predict(encodePred)

    var = y_prediction[0]

    print(encodeY[y_prediction[0]])
    return encodeY[y_prediction[0]]
