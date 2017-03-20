#!/usr/bin/python

import sys
import pickle
sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data, test_classifier
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".
features_list = ['poi','salary', 'deferral_payments', 'total_payments',
                'loan_advances', 'bonus', 'restricted_stock_deferred',
                'deferred_income', 'total_stock_value', 'expenses',
                'exercised_stock_options', 'other', 'long_term_incentive',
                'restricted_stock', 'director_fees', 'shared_receipt_with_poi',
                'to_messages', 'from_poi_to_this_person', 'from_messages',
                'from_this_person_to_poi']
                
financial_features = ['salary', 'deferral_payments', 'total_payments',
                'loan_advances', 'bonus', 'restricted_stock_deferred',
                'deferred_income', 'total_stock_value', 'expenses',
                'exercised_stock_options', 'other', 'long_term_incentive',
                'restricted_stock', 'director_fees']
                
email_features = ['to_messages', 'shared_receipt_with_poi', 
                  'from_messages', 'from_this_person_to_poi', 
                  'from_poi_to_this_person']

### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

enron_df = pd.DataFrame.from_dict(data_dict, orient='index',dtype=float)
enron_df = enron_df.replace('NaN', np.nan)

enron_df.info()
### Task 2: Remove outliers
enron_df = enron_df.drop("LOCKHART EUGENE E", 0)
enron_df = enron_df.drop("THE TRAVEL AGENCY IN THE PARK", 0)
enron_df = enron_df.drop("TOTAL", 0)
enron_df = enron_df.drop('email_address', 1)


enron_df[email_features] = enron_df[email_features].fillna(enron_df[email_features].median())
enron_df[financial_features] = enron_df[financial_features].fillna(0)

for f in financial_features:
    enron_df[f] = np.log1p(abs(enron_df[f]))

### Task 3: Create new feature(s)
### Store to my_dataset for easy export below.
def from_poi_ratio(row):
    from_poi = row['from_poi_to_this_person']
    from_all = row['from_messages']
    
    n = 0
    
    if from_all > 0:
        n = from_poi / from_all
        
    return n
    
def to_poi_ratio(row):
    to_poi = row['from_this_person_to_poi']
    to_all = row['to_messages']
    
    n = 0
    
    if to_all > 0:
        n = to_poi / to_all
        
    return n


def poi_email_ratio(row):
    to_poi = row['from_this_person_to_poi']
    from_poi = row['from_poi_to_this_person']
    to_all = row['to_messages']
    from_all = row['from_messages']
    
    n = 0
    
    if (to_poi > 0 or to_all > 0):
        n = (to_poi + from_poi) / (to_all + from_all)
    
    return n


enron_df["poi_email_ratio"] = enron_df.apply(lambda row: poi_email_ratio(row), axis=1)
enron_df["to_poi_ratio"] = enron_df.apply(lambda row: to_poi_ratio(row), axis=1)
enron_df["from_poi_ratio"] = enron_df.apply(lambda row: from_poi_ratio(row), axis=1)

features_list.extend(["poi_email_ratio", "to_poi_ratio", "from_poi_ratio"])
print(features_list)

my_dataset = enron_df.T.to_dict()

### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)

### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.preprocessing import MinMaxScaler
from sklearn.cross_validation import train_test_split

features_train, features_test, labels_train, labels_test = \
train_test_split(features, labels, test_size=0.3, random_state=42)


from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.model_selection import StratifiedShuffleSplit
from pprint import pprint
# For sklearn 0.17 or older
# splits = StratifiedShuffleSplit(labels, n_iter = 1000, random_state=42)

sss = StratifiedShuffleSplit(n_splits = 1000, random_state=42)

k = 5 # Change this to the number of features to use.

# We will include all the features into variable best_features, then group by their
# occurrences.
features_scores = {}

# For sklearn 0.17 or older
# for i_train, i_test in splits:

for i_train, i_test in sss.split(features, labels):
    features_train, features_test = [features[i] for i in i_train], [features[i] for i in i_test]
    labels_train, labels_test = [labels[i] for i in i_train], [labels[i] for i in i_test]

    # fit selector to training set
    selector = SelectKBest(k = k)
    selector.fit(features_train, labels_train)

    # Get scores of each feature:
    sel_features = np.array(features_list[1:])[selector.get_support()]
    sel_list = []
    for i in range(len(sel_features)):
        sel_list.append([sel_features[i], selector.scores_[i],selector.pvalues_[i]])

    # Fill to feature_scores dictionary
    for feat, score, pvalue in sel_list:
        if feat not in features_scores:
            features_scores[feat] = {'scores': [], 'pvalues': []}
        features_scores[feat]['scores'].append(score)
        features_scores[feat]['pvalues'].append(pvalue)

# Average scores and pvalues of each feature
features_scores_l = [] # tuple of feature name, avg scores, avg pvalues
for feat in features_scores:
    features_scores_l.append((
        feat,
        np.mean(features_scores[feat]['scores']),
        np.mean(features_scores[feat]['pvalues'])
    ))

# Sort by scores and display
import operator
sorted_feature_scores = sorted(features_scores_l, key=operator.itemgetter(1), reverse=True)
sorted_feature_scores_str = ["{}, {}, {}".format(x[0], x[1], x[2]) for x in sorted_feature_scores]

print "feature, score, pvalue"
pprint(sorted_feature_scores_str)


## SelectKBest
from sklearn.feature_selection import SelectKBest, f_classif
# k = 20
# selector = SelectKBest(f_classif, k=k).fit(features_train, labels_train)
# scores=selector.scores_
# unsorted_pairs = zip(features_list[1:], scores)
# sorted_pairs = list(sorted(unsorted_pairs, key=lambda x: x[1]))
# k_features, k_scores = map(list, zip(*sorted_pairs))



## make the selected features the new features list
#my_features = ['poi'] + k_features[14:]

# Provided to give you a starting point. Try a variety of classifiers.
# from sklearn.naive_bayes import GaussianNB
# clf_bayes = GaussianNB()
# print("Naive Bayes: ")
# test_classifier(clf_bayes, my_dataset, my_features, folds = 1000)
# 
# from sklearn import tree
# clf_tree = tree.DecisionTreeClassifier(min_samples_split = 40)
# print("Decision Tree: ")
# test_classifier(clf_tree, my_dataset, my_features, folds = 1000)
# 
# from sklearn.ensemble import RandomForestClassifier
# clf_rf = RandomForestClassifier()
# print("Random Forest: ")
# test_classifier(clf_rf, my_dataset, my_features, folds = 1000)

from sklearn.ensemble import AdaBoostClassifier
# clf_ada = AdaBoostClassifier()
# print("AdaBoost: ")
# test_classifier(clf_ada, my_dataset, my_features, folds = 1000)


### Task 5: Tune your classifier to achieve better than .3 precision and recall 
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info: 
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

# Example starting point. Try investigating other evaluation techniques!
# from sklearn.pipeline import Pipeline
# from sklearn.feature_selection import SelectPercentile, SelectKBest, f_classif, chi2
# from sklearn.model_selection import StratifiedShuffleSplit
# from sklearn.model_selection import GridSearchCV
# from sklearn.metrics import classification_report
# 
# pipe = Pipeline([
#         ('min_max', MinMaxScaler()),
#         ('k_best', SelectKBest()),
#         ('classify', AdaBoostClassifier())
#     ])
#     
# param_grid = ([
#         {
#             'k_best__k': [5,6,7,8,9,10,11,12,13,14,15],
#             'classify__n_estimators':[10, 15, 20],
#             'classify__algorithm': ['SAMME', 'SAMME.R'],
#             'classify__learning_rate': [1.0, 1.5, 2.0, 2.5],
#         }
#     ])
# 
# sss = StratifiedShuffleSplit()
# clf = GridSearchCV(pipe, param_grid = param_grid, cv = sss, scoring='f1_weighted')
# clf.fit(features_train, labels_train)
# 
# print "(clf.best_estimator_.steps): ", (clf.best_estimator_.steps)
# print "(clf.best_score_): ", (clf.best_score_)
# print "(clf.best_params_): ", (clf.best_params_)
# print "(clf.scorer_): ", (clf.scorer_)
# 
# clf = clf.best_estimator_
# test_classifier(clf, my_dataset, features_list, folds = 1000)


pipe = Pipeline([
         ('min_max', MinMaxScaler()),
         ('k_best', SelectKBest(k=5)),
         ('classify', AdaBoostClassifier(algorithm='SAMME.R', base_estimator=None, learning_rate=1.0, n_estimators=15, random_state=None))
     ])

clf = pipe.fit(features_train, labels_train)    

#test_classifier(clf, my_dataset, my_features, folds = 1000)


### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

dump_classifier_and_data(clf, my_dataset, features_list)