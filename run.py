from typing import TypedDict
from flask import Flask, render_template, jsonify, request
from flask_pymongo import PyMongo
from flask_cors import CORS, cross_origin

import json
import copy
import warnings  
import pandas as pd 
pd.set_option('use_inf_as_na', True)
import numpy as np

from joblib import Memory
from collections import Counter

from xgboost import XGBClassifier
from sklearn.neighbors import NearestNeighbors
from bayes_opt import BayesianOptimization
from sklearn.model_selection import cross_validate
from sklearn.model_selection import cross_val_predict
from sklearn.model_selection import train_test_split
from sklearn.metrics import balanced_accuracy_score
from sklearn.metrics import f1_score

from sklearn.metrics import confusion_matrix
import random
from sklearn import preprocessing

import umap
from scipy import spatial
from scipy import stats
from scipy.spatial import distance

from imblearn.over_sampling import SMOTE
from imblearn.over_sampling import ADASYN
from imblearn.under_sampling import OneSidedSelection
from imblearn.under_sampling import NeighbourhoodCleaningRule

# this block of code is for the connection between the server, the database, and the client (plus routing)

# access MongoDB 
app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mydb"
mongo = PyMongo(app)

cors = CORS(app, resources={r"/data/*": {"origins": "*"}})

@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
@app.route('/data/Reset', methods=["GET", "POST"])
def reset():
    global DataRawLength
    global DataResultsRaw
    global previousState
    previousState = []

    global filterActionFinal
    filterActionFinal = ''

    global keySpecInternal
    keySpecInternal = 1

    global RANDOM_SEED
    RANDOM_SEED = 42

    global keyData
    keyData = 0

    global XData
    XData = []
    global yData
    yData = []

    global X_test
    X_test = []
    global y_test
    y_test = []

    # global XDataNorm
    # XDataNorm = []

    global XDataNoRemoval
    XDataNoRemoval = []

    global XDataNoRemovalOrig
    XDataNoRemovalOrig = []

    global XDataStored
    XDataStored = []
    global yDataStored
    yDataStored = []
    
    global finalResultsData
    finalResultsData = []

    global detailsParams
    detailsParams = []

    global algorithmList
    algorithmList = []

    global ClassifierIDsList
    ClassifierIDsList = ''

    global RetrieveModelsList
    RetrieveModelsList = []

    global allParametersPerfCrossMutr
    allParametersPerfCrossMutr = []

    global all_classifiers
    all_classifiers = []

    global crossValidation
    crossValidation = 5
    
    global resultsMetrics
    resultsMetrics = []

    global parametersSelData
    parametersSelData = []

    global target_names
    target_names = []

    global keyFirstTime
    keyFirstTime = True

    global target_namesLoc
    target_namesLoc = []

    global featureCompareData
    featureCompareData = []

    global columnsKeep
    columnsKeep = []

    global columnsNewGen
    columnsNewGen = []

    global underSamplInd
    underSamplInd = []

    global columnsNames
    columnsNames = []

    global fileName
    fileName = []

    global instancesOver
    instancesOver = []

    return 'The reset was done!'

# retrieve data from client and select the correct data set
@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
@app.route('/data/ServerRequest', methods=["GET", "POST"])
def retrieveFileName():
    global DataRawLength
    global DataResultsRaw
    global DataResultsRawTest
    global DataRawLengthTest

    global fileName
    fileName = []
    fileName = request.get_data().decode('utf8').replace("'", '"')

    global keySpecInternal
    keySpecInternal = 1

    global filterActionFinal
    filterActionFinal = ''

    global dataSpacePointsIDs
    dataSpacePointsIDs = []

    global RANDOM_SEED
    RANDOM_SEED = 42

    global keyData
    keyData = 0

    global XData
    XData = []

    global X_test
    X_test = []
    global y_test
    y_test = []

    # global XDataNorm
    # XDataNorm = []

    global XDataNoRemoval
    XDataNoRemoval = []

    global XDataNoRemovalOrig
    XDataNoRemovalOrig = []

    global previousState
    previousState = []

    global yData
    yData = []

    global XDataStored
    XDataStored = []

    global yDataStored
    yDataStored = []

    global finalResultsData
    finalResultsData = []

    global ClassifierIDsList
    ClassifierIDsList = ''

    global algorithmList
    algorithmList = []

    global detailsParams
    detailsParams = []

    global underSamplInd
    underSamplInd = []

    # Initializing models

    global RetrieveModelsList
    RetrieveModelsList = []

    global resultsList
    resultsList = []

    global allParametersPerfCrossMutr
    allParametersPerfCrossMutr = []

    global HistoryPreservation
    HistoryPreservation = []

    global all_classifiers
    all_classifiers = []

    global crossValidation
    crossValidation = 5

    global parametersSelData
    parametersSelData = []

    global StanceTest
    StanceTest = False

    global target_names
    
    target_names = []

    global keyFirstTime
    keyFirstTime = True

    global target_namesLoc
    target_namesLoc = []

    global featureCompareData
    featureCompareData = []

    global columnsKeep
    columnsKeep = []

    global columnsNewGen
    columnsNewGen = []

    global columnsNames
    columnsNames = []

    global instancesOver
    instancesOver = []

    global data

    DataRawLength = -1
    DataRawLengthTest = -1
    data = json.loads(fileName)  
    if data['fileName'] == 'wineOrigC':
        CollectionDB = mongo.db.wineOrigC.find()
        # target_names.append('5')
        # target_names.append('6')
        # target_names.append('7')
        # target_names.append('4')
        # target_names.append('3')
        # target_names.append('8')
    elif data['fileName'] == 'WineC':
        CollectionDB = mongo.db.WineC.find()
        target_names.append('Fine')
        target_names.append('Superior')
        target_names.append('Inferior')
    elif data['fileName'] == 'diabetesC':
        CollectionDB = mongo.db.diabetesC.find()
        target_names.append('Negative')
        target_names.append('Positive')
    elif data['fileName'] == 'VehicleC':
        CollectionDB = mongo.db.VehicleC.find()
        target_names.append('Bus')
        target_names.append('Car')
        target_names.append('Van')
    elif data['fileName'] == 'breastC':
        CollectionDB = mongo.db.breastC.find()
        target_names.append('Benign')
        target_names.append('Malignant')
    elif data['fileName'] == 'ContraceptiveC':
        CollectionDB = mongo.db.ContraceptiveC.find()
        target_names.append('Short-Term')
        target_names.append('Long-Term')
        target_names.append('No-use')
    elif data['fileName'] == 'TitanicC':
        CollectionDB = mongo.db.TitanicC.find()
        target_names.append('Survived')
        target_names.append('Died')
    elif data['fileName'] == 'CreditC':
        CollectionDB = mongo.db.CreditC.find()
        target_names.append('Approved')
        target_names.append('Rejected')
    elif data['fileName'] == 'HappinessC':
        CollectionDB = mongo.db.HappinessC.find()
        target_names.append('HS-Level-3')
        target_names.append('HS-Level-2')
        target_names.append('HS-Level-1')
    else:
        CollectionDB = mongo.db.IrisC.find()
        target_names.append('Setosa')
        target_names.append('Versicolor')
        target_names.append('Virginica')
    DataResultsRaw = []
    for index, item in enumerate(CollectionDB):
        item['_id'] = str(item['_id'])
        item['InstanceID'] = index
        DataResultsRaw.append(item)
    DataRawLength = len(DataResultsRaw)

    DataResultsRawTest = []
    if (StanceTest):
        for index, item in enumerate(CollectionDBTest):
            item['_id'] = str(item['_id'])
            item['InstanceID'] = index
            DataResultsRawTest.append(item)
        DataRawLengthTest = len(DataResultsRawTest)

    dataSetSelection()
    return 'Everything is okay'

def dataSetSelection():

    global AllTargets
    global target_names
    target_namesLoc = []

    DataResults = copy.deepcopy(DataResultsRaw)

    for dictionary in DataResultsRaw:
        for key in dictionary.keys():
            if (key.find('*') != -1):
                target = key
                continue
        continue

    DataResultsRaw.sort(key=lambda x: x[target], reverse=True)
    DataResults.sort(key=lambda x: x[target], reverse=True)

    for dictionary in DataResults:
        del dictionary['_id']
        del dictionary['InstanceID']
        del dictionary[target]

    AllTargets = [o[target] for o in DataResultsRaw]
    AllTargetsFloatValues = []

    global fileName
    data = json.loads(fileName) 

    previous = None
    Class = 0
    for i, value in enumerate(AllTargets):
        if (i == 0):
            previous = value
            if (data['fileName'] == 'BreastC' or data['fileName'] == 'wineOrigC'):
                target_names.append(value)
            else:
                pass
        if (value == previous):
            AllTargetsFloatValues.append(Class)
        else:
            Class = Class + 1
            if (data['fileName'] == 'BreastC' or data['fileName'] == 'wineOrigC'):
                target_names.append(value)
            else:
                pass
            AllTargetsFloatValues.append(Class)
            previous = value

    ArrayDataResults = pd.DataFrame.from_dict(DataResults)

    global XData, yData, X_test, y_test, RANDOM_SEED
    XDataAllUn, yDataAll = ArrayDataResults, AllTargetsFloatValues
    XDataAll = (XDataAllUn-XDataAllUn.min())/(XDataAllUn.max()-XDataAllUn.min())
    # if (data['fileName'] == 'diabetesC'):
    #     XDataAll[['Glucose','BloodPress','SkinThick','Insulin','BMI']] = XDataAll[['Glucose','BloodPress','SkinThick','Insulin','BMI']].replace(0,np.NaN)
    #     XDataAll['Glucose'].fillna(XDataAll['Glucose'].mean(), inplace = True)
    #     XDataAll['BloodPress'].fillna(XDataAll['BloodPress'].mean(), inplace = True)
    #     XDataAll['SkinThick'].fillna(XDataAll['SkinThick'].median(), inplace = True)
    #     XDataAll['Insulin'].fillna(XDataAll['Insulin'].median(), inplace = True)
    #     XDataAll['BMI'].fillna(XDataAll['BMI'].median(), inplace = True)
    X_train, X_testLoc, yData, y_test = train_test_split(XDataAll, yDataAll, test_size=0.25, stratify=yDataAll, random_state=RANDOM_SEED)
    
    X_train = X_train.reset_index(drop=True)
    X_train['my_index'] = yData
    XData = X_train.sort_values(by=['my_index'], ascending=True)
    yData = sorted(yData)
    XData.drop('my_index', inplace=True, axis=1)
    XData = XData.reset_index(drop=True)

    X_testLoc = X_testLoc.reset_index(drop=True)
    X_testLoc['my_index'] = y_test
    X_test = X_testLoc.sort_values(by=['my_index'], ascending=True)
    y_test = sorted(y_test)
    X_test.drop('my_index', inplace=True, axis=1)
    X_test = X_test.reset_index(drop=True)
    # global XDataNorm
    # x = XData.values #returns a numpy array
    # min_max_scaler = preprocessing.MinMaxScaler()
    # x_scaled = min_max_scaler.fit_transform(x)
    # XDataNorm = pd.DataFrame(x_scaled)

    warnings.simplefilter('ignore')

    columnsFeat = []
    for col in XData.columns:
        columnsFeat.append(col)  

    key = 0
    undersamplNow = []
    neigh = 0
    underKey = 0
    kOSS_NCR = 5
    sOSS_SSNCR = 'all'
    typesDataUnder = ['safe', 'borderline', 'rare', 'outlier']
    NS = 1
    TS = 0.5
    oversamplNow = []
    overKey = 0
    kSMOTE_ADASYN = 5
    sSMOTE_ADASYN = 'all'   
    minDist = 0
    typesData = ['safe', 'borderline', 'rare', 'outlier']

    executeSearch(key, undersamplNow, neigh, underKey, kOSS_NCR, sOSS_SSNCR, typesDataUnder, NS, TS, oversamplNow, overKey, kSMOTE_ADASYN, sSMOTE_ADASYN, minDist, typesData)
    
    return 'Everything is okay'

def create_global_function():
    global estimator
    location = './cachedir'
    memory = Memory(location, verbose=0)

    # calculating for all algorithms and models the performance and other results
    @memory.cache
    def estimator(n_estimators, eta, max_depth, subsample, colsample_bytree):
        # initialize model
        print('modelsCompNow!!!!!')
        n_estimators = int(n_estimators)
        max_depth = int(max_depth)
        model = XGBClassifier(n_estimators=n_estimators, eta=eta, max_depth=max_depth, subsample=subsample, colsample_bytree=colsample_bytree, n_jobs=-1, random_state=RANDOM_SEED, seed=RANDOM_SEED, silent=True, verbosity = 0, use_label_encoder=False)
        # set in cross-validation
        result = cross_validate(model, XData, yData, cv=crossValidation, scoring='accuracy')
        # result is mean of test_score
        return np.mean(result['test_score'])

location = './cachedir'
memory = Memory(location, verbose=0)

# calculating for all algorithms and models the performance and other results
@memory.cache
def callKSearch ():
    print('findKValueNow!!!')
    global countPercentageList
    countPercentageList = []
    global storeAllMetricsList
    storeAllMetricsList = []
    global sortShepCorrList
    sortShepCorrList = []
    global GatherSafe
    GatherSafe = []
    global GatherBorder
    GatherBorder = []
    global GatherRare
    GatherRare = []
    global GatherOut
    GatherOut = [] 
    global UMAPModalStore
    UMAPModalStore = []
    global MaxValue
    MaxValue = []
    global MaxIndex
    MaxIndex = []

    kValuesAll = [5,6,7,8,9,10,11,12,13]
    mDistanceAll = [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
    dataNP = XData.to_numpy()
    D_highSpace = distance.squareform(distance.pdist(dataNP))

    for val in kValuesAll:
        safeIndCounter = []
        borderlineIndCounter = []
        rareIndCounter = []
        outIndCounter = []
        countPercentage = []
        
        nbrs = NearestNeighbors(n_neighbors=val, metric="euclidean", n_jobs = -1).fit(XData)
        distances, indices = nbrs.kneighbors(XData)

        summarizePerc = []
        for idx, el in enumerate(indices):
            computePer = -1
            for each in el:
                if (yData[idx] == yData[each]):
                    computePer = computePer + 1
            summarizePerc.append(computePer)

        for i, el in enumerate(summarizePerc):
            if (el >= (0.8 * val)):
                safeIndCounter.append(i)
            elif (el >= (0.5 * val)):
                borderlineIndCounter.append(i)
            elif (el >= (0.2 * val)):
                rareIndCounter.append(i)
            else:
                outIndCounter.append(i)
        
        percsafeIndCounter = len(safeIndCounter) / (len(safeIndCounter)+len(borderlineIndCounter)+len(rareIndCounter)+len(outIndCounter))
        percborderlineIndCounter = len(borderlineIndCounter) / (len(safeIndCounter)+len(borderlineIndCounter)+len(rareIndCounter)+len(outIndCounter))
        percrareIndCounter = len(rareIndCounter) / (len(safeIndCounter)+len(borderlineIndCounter)+len(rareIndCounter)+len(outIndCounter))
        percoutIndCounter = len(outIndCounter) / (len(safeIndCounter)+len(borderlineIndCounter)+len(rareIndCounter)+len(outIndCounter))

        countPercentage.append(percsafeIndCounter*100)
        countPercentage.append(percborderlineIndCounter*100)
        countPercentage.append(percrareIndCounter*100)
        countPercentage.append(percoutIndCounter*100)

        countPercentageList.append(countPercentage)
        
        metricShepCorr = []
        for dis in mDistanceAll:
            SearchUMAP = FunUMAPAll(XData, val, dis)
            D_lowSpace = distance.squareform(distance.pdist(SearchUMAP))
            resultShep = shepard_diagram_correlation(D_highSpace, D_lowSpace) 
            metricShepCorr.append(resultShep*100)
        storeAllMetricsList.append(metricShepCorr)
        sortShepCorr = sorted(range(len(metricShepCorr)), key=lambda k: metricShepCorr[k], reverse=True)[0]
        sortShepCorrList.append(sortShepCorr)

        max_value = max(metricShepCorr)
        max_index = metricShepCorr.index(max_value)
        UMAPModal = FunUMAP(XData, val, mDistanceAll[max_index])
        UMAPModalStore.append(UMAPModal)
        GatherSafe.append(safeIndCounter)
        GatherBorder.append(borderlineIndCounter)
        GatherRare.append(rareIndCounter)
        GatherOut.append(outIndCounter)
        MaxValue.append(max_value)
        MaxIndex.append(max_index)

    return [countPercentageList,sortShepCorrList,storeAllMetricsList,UMAPModalStore,GatherSafe,GatherBorder,GatherRare,GatherOut,MaxValue,MaxIndex]

def executeSearch(key, undersamplNow, neigh, underKey, kOSS_NCR, sOSS_SSNCR, typesDataUnder, NS, TS, oversamplNow, overKey, kSMOTE_ADASYN, sSMOTE_ADASYN, minD, typesData):

    random.seed(RANDOM_SEED)
    np.random.seed(RANDOM_SEED)
    # pd.set_option("display.max_rows", None, "display.max_columns", None)

    global estimator
    global XData
    global yData
    global X_test
    global countPercentageList
    global sortShepCorrList
    global storeAllMetricsList
    global GatherSafe
    global GatherBorder
    global GatherRare
    global GatherOut
    global UMAPModalStore
    global MaxValue
    global MaxIndex
    global target_names
    global finalResultsData
    global underSamplInd
    finalResultsData = []
    yDataList = []
    kValuesAll = [5,6,7,8,9,10,11,12,13]
    mDistanceAll = [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
    minDist = mDistanceAll[minD]

    if (key == 0):
        # if (data['fileName'] == 'diabetesC'):
        #     estimator = MLPClassifier(hidden_layer_sizes=(20, 20), alpha=1, random_state=RANDOM_SEED)
        # else:
        create_global_function()
        params = {"n_estimators": (5, 200), "eta": (0.05, 0.3), "max_depth": (6,12), "subsample": (0.8,1), "colsample_bytree": (0.8,1)}
        bayesopt = BayesianOptimization(estimator, params, random_state=RANDOM_SEED)
        bayesopt.maximize(init_points=20, n_iter=5, acq='ucb') # 20 and 5
        bestParams = bayesopt.max['params']
        estimator = XGBClassifier(n_estimators=int(bestParams.get('n_estimators')), eta=bestParams.get('eta'), max_depth=int(bestParams.get('max_depth')), subsample=bestParams.get('subsample'), colsample_bytree=bestParams.get('colsample_bytree'), probability=True, random_state=RANDOM_SEED, seed=RANDOM_SEED, silent=True, verbosity = 0, use_label_encoder=False)
        countPercentageList,sortShepCorrList,storeAllMetricsList,UMAPModalStore,GatherSafe,GatherBorder,GatherRare,GatherOut,MaxValue,MaxIndex = callKSearch()

    columnsFeatures = []
    columnsFeaturesOld = []
    for col in XData.columns:
        columnsFeaturesOld.append(col) 

    if (underKey == 0):
        underSamplInd = []
        if (overKey == 0):
            fit = estimator.fit(XData, yData)
            FI = fit.feature_importances_
            sortedInd = np.argsort(FI.tolist())
            for i in sortedInd:
                columnsFeatures.append(columnsFeaturesOld[i])
            XData = XData.reindex(columns=columnsFeatures)
            X_test = X_test.reindex(columns=columnsFeatures)
        else:
            X_test = X_test.reindex(columns=columnsFeaturesOld)
        estimator.fit(XData, yData)
        yPredict = cross_val_predict(estimator, XData, yData, cv=crossValidation)
        yPredictProb = cross_val_predict(estimator, XData, yData, cv=crossValidation, method='predict_proba')
        conf = confusion_matrix(yData, yPredict)
        BATrain = balanced_accuracy_score(yData, yPredict)
        FSTrain = f1_score(yData, yPredict, average='macro')
        yPredictTest = estimator.predict(X_test)
        yPredictProbTest = estimator.predict_proba(X_test)
        confTest = confusion_matrix(y_test, yPredictTest)
        BATest = balanced_accuracy_score(y_test, yPredictTest)
        FSTest = f1_score(y_test, yPredictTest, average='macro')
        XTestPandas = X_test.to_json(orient='records') 
        yDataList = yData[:]

        uniqueyData = list(set(yData))
        occurrences = []
        for value in uniqueyData:
            temp = yData.count(value)
            occurrences.append(temp)
            
        XDataPandas = XData.to_json(orient='records')  
        x = XData.values #returns a numpy array
        min_max_scaler = preprocessing.MinMaxScaler()
        x_scaled = min_max_scaler.fit_transform(x)
        XDataNorm = pd.DataFrame(x_scaled)
        XDataNormPandas = XDataNorm.to_json(orient='records')    
        nbrs = NearestNeighbors(n_neighbors=kValuesAll[neigh], metric="euclidean", n_jobs = -1).fit(XData)
        distances, indices = nbrs.kneighbors(XData)
        summarizePerc = []
        for idx, el in enumerate(indices):
            computePer = -1
            for each in el:
                if (yData[idx] == yData[each]):
                    computePer = computePer + 1
            summarizePerc.append(computePer)
        ModelSpaceUMAP = FunUMAP(XData, kValuesAll[neigh], minDist)
        ModelSpaceUMAPTest = FunUMAPTest(XData, kValuesAll[neigh], minDist, X_test)
    elif (underKey == 1):
        safeInd = []
        borderlineInd = []
        rareInd = []
        outInd = []
        nbrs = NearestNeighbors(n_neighbors=kValuesAll[neigh], metric="euclidean", n_jobs = -1).fit(XData)
        distances, indices = nbrs.kneighbors(XData)
        summarizePerc = []
        for idx, el in enumerate(indices):
            computePer = -1
            for each in el:
                if (yData[idx] == yData[each]):
                    computePer = computePer + 1
            summarizePerc.append(computePer)

        for i, el in enumerate(summarizePerc):
            if (el >= (0.8 * kValuesAll[neigh])):
                safeInd.append(i)
            elif (el >= (0.5 * kValuesAll[neigh])):
                borderlineInd.append(i)
            elif (el >= (0.2 * kValuesAll[neigh])):
                rareInd.append(i)
            else:
                outInd.append(i)
        allIndicesTogether = []
        allFlag = True
        for el in typesDataUnder:
            if (el == "safe"):
                allIndicesTogether = allIndicesTogether + safeInd
            elif (el == "borderline"):
                allIndicesTogether = allIndicesTogether + borderlineInd
            elif (el == "rare"):
                allIndicesTogether = allIndicesTogether + rareInd
            elif (el == "outlier"):
                allIndicesTogether = allIndicesTogether + outInd
            else: 
                allFlag = False
        if (allFlag):
            if (len(undersamplNow) == 0):
                boundarySampling = OneSidedSelection(n_neighbors = kOSS_NCR, n_seeds_S= NS, sampling_strategy=sOSS_SSNCR, random_state = RANDOM_SEED, n_jobs = -1)
                fit = estimator.fit(XData, yData)
                FI = fit.feature_importances_
                sortedInd = np.argsort(FI.tolist())
                for i in sortedInd:
                    columnsFeatures.append(columnsFeaturesOld[i])
                XData = XData.reindex(columns=columnsFeatures)
                X_test = X_test.reindex(columns=columnsFeatures)
                X_resampledUnder, y_resampledUnder = boundarySampling.fit_resample(XData, yData)
                artificial = pd.concat([XData, X_resampledUnder]).drop_duplicates(keep=False)
                underSamplInd = []
                for each in artificial.index.values:
                    underSamplInd.append(int(each))
                X_resampledUnder.reset_index(drop=True)
                estimator.fit(XData, yData)
                yPredict = cross_val_predict(estimator, XData, yData, cv=crossValidation)
                yPredictProb = cross_val_predict(estimator, XData, yData, cv=crossValidation, method='predict_proba')
                conf = confusion_matrix(yData, yPredict)
                BATrain = balanced_accuracy_score(yData, yPredict)
                FSTrain = f1_score(yData, yPredict, average='macro')
                yDataList = yData[:]

                uniqueyData = list(set(yData))
                occurrences = []
                for value in uniqueyData:
                    temp = yData.count(value)
                    occurrences.append(temp)
                    
                XDataPandas = XData.to_json(orient='records')  
                x = XData.values #returns a numpy array
                min_max_scaler = preprocessing.MinMaxScaler()
                x_scaled = min_max_scaler.fit_transform(x)
                XDataNorm = pd.DataFrame(x_scaled)
                XDataNormPandas = XDataNorm.to_json(orient='records') 

                nbrs = NearestNeighbors(n_neighbors=kValuesAll[neigh], metric="euclidean", n_jobs = -1).fit(XData)
                distances, indices = nbrs.kneighbors(XData)
                summarizePerc = []
                for idx, el in enumerate(indices):
                    computePer = -1
                    for each in el:
                        if (yData[idx] == yData[each]):
                            computePer = computePer + 1
                    summarizePerc.append(computePer)
                ModelSpaceUMAP = FunUMAP(XData, kValuesAll[neigh], minDist)
                ModelSpaceUMAPTest = FunUMAPTest(XData, kValuesAll[neigh], minDist, X_test)
                
                estimator.fit(X_resampledUnder, y_resampledUnder)
                yPredictTest = estimator.predict(X_test)
                yPredictProbTest = estimator.predict_proba(X_test)
                confTest = confusion_matrix(y_test, yPredictTest)
                BATest = balanced_accuracy_score(y_test, yPredictTest)
                FSTest = f1_score(y_test, yPredictTest, average='macro')
                XTestPandas = X_test.to_json(orient='records') 
            else:
                boundarySampling = OneSidedSelection(n_neighbors = kOSS_NCR, n_seeds_S= NS, sampling_strategy=sOSS_SSNCR, random_state = RANDOM_SEED, n_jobs = -1)
                XDataNewInverse = XData.iloc[~XData.index.isin(undersamplNow)]
                yDataNewInverse = []
                #localUnderSamplInd = []
                for idx, i in enumerate(yData):
                    # if (idx in underSamplInd):
                    #     if (idx in undersamplNow):
                    #         pass
                    #     else:
                    #         localUnderSamplInd.append(idx)
                    if (idx in undersamplNow):
                        pass
                    else:
                        yDataNewInverse.append(i)
                XData = XDataNewInverse.copy()
                yData = yDataNewInverse.copy()
                XData.reset_index(drop=True)
                #underSamplInd = localUnderSamplInd.copy()

                fit = estimator.fit(XData, yData)
                FI = fit.feature_importances_
                sortedInd = np.argsort(FI.tolist())
                for i in sortedInd:
                    columnsFeatures.append(columnsFeaturesOld[i])
                XData = XData.reindex(columns=columnsFeatures)
                X_test = X_test.reindex(columns=columnsFeatures)
                # X_resampledUnder, y_resampledUnder = boundarySampling.fit_resample(XData, yData)
                # artificial = pd.concat([XData, X_resampledUnder]).drop_duplicates(keep=False)
                underSamplInd = []
                # for each in artificial.index.values:
                #     underSamplInd.append(int(each))
                # X_resampledUnder.reset_index(drop=True)
                estimator.fit(XData, yData)
                yPredict = cross_val_predict(estimator, XData, yData, cv=crossValidation)
                yPredictProb = cross_val_predict(estimator, XData, yData, cv=crossValidation, method='predict_proba')
                conf = confusion_matrix(yData, yPredict)
                BATrain = balanced_accuracy_score(yData, yPredict)
                FSTrain = f1_score(yData, yPredict, average='macro')
                yDataList = yData[:]

                uniqueyData = list(set(yData))
                occurrences = []
                for value in uniqueyData:
                    temp = yData.count(value)
                    occurrences.append(temp)
                    
                XDataPandas = XData.to_json(orient='records')  
                x = XData.values #returns a numpy array
                min_max_scaler = preprocessing.MinMaxScaler()
                x_scaled = min_max_scaler.fit_transform(x)
                XDataNorm = pd.DataFrame(x_scaled)
                XDataNormPandas = XDataNorm.to_json(orient='records') 

                nbrs = NearestNeighbors(n_neighbors=kValuesAll[neigh], metric="euclidean", n_jobs = -1).fit(XData)
                distances, indices = nbrs.kneighbors(XData)

                summarizePerc = []
                for idx, el in enumerate(indices):
                    computePer = -1
                    for each in el:
                        if (yData[idx] == yData[each]):
                            computePer = computePer + 1
                    summarizePerc.append(computePer)
                ModelSpaceUMAP = FunUMAP(XData, kValuesAll[neigh], minDist)
                ModelSpaceUMAPTest = FunUMAPTest(XData, kValuesAll[neigh], minDist, X_test)

                yPredictTest = estimator.predict(X_test)
                yPredictProbTest = estimator.predict_proba(X_test)
                confTest = confusion_matrix(y_test, yPredictTest)
                BATest = balanced_accuracy_score(y_test, yPredictTest)
                FSTest = f1_score(y_test, yPredictTest, average='macro')
                XTestPandas = X_test.to_json(orient='records') 
        else:
            if (len(undersamplNow) == 0):
                boundarySampling = OneSidedSelection(n_neighbors = kOSS_NCR, n_seeds_S= NS, sampling_strategy=sOSS_SSNCR, random_state = RANDOM_SEED, n_jobs = -1)
                fit = estimator.fit(XData, yData)
                FI = fit.feature_importances_
                sortedInd = np.argsort(FI.tolist())
                for i in sortedInd:
                    columnsFeatures.append(columnsFeaturesOld[i])
                XData = XData.reindex(columns=columnsFeatures)
                X_test = X_test.reindex(columns=columnsFeatures)
                XDataNew = XData.copy()
                yDataNew = yData.copy()
                XDataNew = XData.iloc[allIndicesTogether]
                XDataNewInverse = XData.iloc[~XData.index.isin(allIndicesTogether)]
                yDataNew = [yData[i] for i in allIndicesTogether]
                X_resampledUnder, y_resampledUnder = boundarySampling.fit_resample(XDataNew, yDataNew)
                artificial = pd.concat([XData, X_resampledUnder]).drop_duplicates(keep=False)
                yDataRemaining = []
                underSamplInd = []
                for each in artificial.index.values:
                    if (each in safeInd):
                        if (typesDataUnder[0] == "safe"):
                            underSamplInd.append(int(each))
                    elif (each in borderlineInd):
                        if (typesDataUnder[1] == "borderline"):
                            underSamplInd.append(int(each))
                    elif (each in rareInd):
                        if (typesDataUnder[2] == "rare"):
                            underSamplInd.append(int(each))
                    else:
                        if (typesDataUnder[3] == "outlier"):
                            underSamplInd.append(int(each))
                X_resampledUnder.reset_index(drop=True)
                estimator.fit(XData, yData)
                yPredict = cross_val_predict(estimator, XData, yData, cv=crossValidation)
                yPredictProb = cross_val_predict(estimator, XData, yData, cv=crossValidation, method='predict_proba')
                conf = confusion_matrix(yData, yPredict)
                BATrain = balanced_accuracy_score(yData, yPredict)
                FSTrain = f1_score(yData, yPredict, average='macro')
                yDataList = yData[:]
                uniqueyData = list(set(yData))
                occurrences = []
                for value in uniqueyData:
                    temp = yData.count(value)
                    occurrences.append(temp)
                    
                XDataPandas = XData.to_json(orient='records')  
                x = XData.values #returns a numpy array
                min_max_scaler = preprocessing.MinMaxScaler()
                x_scaled = min_max_scaler.fit_transform(x)
                XDataNorm = pd.DataFrame(x_scaled)
                XDataNormPandas = XDataNorm.to_json(orient='records') 

                nbrs = NearestNeighbors(n_neighbors=kValuesAll[neigh], metric="euclidean", n_jobs = -1).fit(XData)
                distances, indices = nbrs.kneighbors(XData)
                summarizePerc = []
                for idx, el in enumerate(indices):
                    computePer = -1
                    for each in el:
                        if (yData[idx] == yData[each]):
                            computePer = computePer + 1
                    summarizePerc.append(computePer)
                ModelSpaceUMAP = FunUMAP(XData, kValuesAll[neigh], minDist)
                ModelSpaceUMAPTest = FunUMAPTest(XData, kValuesAll[neigh], minDist, X_test)

                XDataTesting = XData.copy()
                XDataTesting['yDat'] = yData
                XDataTesting.drop(underSamplInd, axis=0, inplace=True)
                yDataRemaining = XDataTesting['yDat'].tolist()
                XDataTesting = XDataTesting.drop('yDat', 1)
                estimator.fit(XDataTesting, yDataRemaining)
                yPredictTest = estimator.predict(X_test)
                yPredictProbTest = estimator.predict_proba(X_test)
                confTest = confusion_matrix(y_test, yPredictTest)
                BATest = balanced_accuracy_score(y_test, yPredictTest)
                FSTest = f1_score(y_test, yPredictTest, average='macro')
                XTestPandas = X_test.to_json(orient='records') 
            else:
                boundarySampling = OneSidedSelection(n_neighbors = kOSS_NCR, n_seeds_S= NS, sampling_strategy=sOSS_SSNCR, random_state = RANDOM_SEED, n_jobs = -1)
                XDataNewInverse = XData.iloc[~XData.index.isin(undersamplNow)]
                yDataNewInverse = []
                #localUnderSamplInd = []
                for idx, i in enumerate(yData):
                    # if (idx in underSamplInd):
                    #     if (idx in undersamplNow):
                    #         pass
                    #     else:
                    #         localUnderSamplInd.append(idx)
                    if (idx in undersamplNow):
                        pass
                    else:
                        yDataNewInverse.append(i)
                XData = XDataNewInverse.copy()
                yData = yDataNewInverse.copy()
                XData.reset_index(drop=True)
                #underSamplInd = localUnderSamplInd.copy()

                fit = estimator.fit(XData, yData)
                FI = fit.feature_importances_
                sortedInd = np.argsort(FI.tolist())
                for i in sortedInd:
                    columnsFeatures.append(columnsFeaturesOld[i])
                XData = XData.reindex(columns=columnsFeatures)
                X_test = X_test.reindex(columns=columnsFeatures)
                # X_resampledUnder, y_resampledUnder = boundarySampling.fit_resample(XData, yData)
                # artificial = pd.concat([XData, X_resampledUnder]).drop_duplicates(keep=False)
                underSamplInd = []
                # for each in artificial.index.values:
                #     underSamplInd.append(int(each))
                # X_resampledUnder.reset_index(drop=True)
                estimator.fit(XData, yData)
                yPredict = cross_val_predict(estimator, XData, yData, cv=crossValidation)
                yPredictProb = cross_val_predict(estimator, XData, yData, cv=crossValidation, method='predict_proba')
                conf = confusion_matrix(yData, yPredict)
                BATrain = balanced_accuracy_score(yData, yPredict)
                FSTrain = f1_score(yData, yPredict, average='macro')
                yDataList = yData[:]

                uniqueyData = list(set(yData))
                occurrences = []
                for value in uniqueyData:
                    temp = yData.count(value)
                    occurrences.append(temp)
                    
                XDataPandas = XData.to_json(orient='records')  
                x = XData.values #returns a numpy array
                min_max_scaler = preprocessing.MinMaxScaler()
                x_scaled = min_max_scaler.fit_transform(x)
                XDataNorm = pd.DataFrame(x_scaled)
                XDataNormPandas = XDataNorm.to_json(orient='records') 

                nbrs = NearestNeighbors(n_neighbors=kValuesAll[neigh], metric="euclidean", n_jobs = -1).fit(XData)
                distances, indices = nbrs.kneighbors(XData)

                summarizePerc = []
                for idx, el in enumerate(indices):
                    computePer = -1
                    for each in el:
                        if (yData[idx] == yData[each]):
                            computePer = computePer + 1
                    summarizePerc.append(computePer)
                ModelSpaceUMAP = FunUMAP(XData, kValuesAll[neigh], minDist)
                ModelSpaceUMAPTest = FunUMAPTest(XData, kValuesAll[neigh], minDist, X_test)

                yPredictTest = estimator.predict(X_test)
                yPredictProbTest = estimator.predict_proba(X_test)
                confTest = confusion_matrix(y_test, yPredictTest)
                BATest = balanced_accuracy_score(y_test, yPredictTest)
                FSTest = f1_score(y_test, yPredictTest, average='macro')
                XTestPandas = X_test.to_json(orient='records')      
    else:
        safeInd = []
        borderlineInd = []
        rareInd = []
        outInd = []
        nbrs = NearestNeighbors(n_neighbors=kValuesAll[neigh], metric="euclidean", n_jobs = -1).fit(XData)
        distances, indices = nbrs.kneighbors(XData)
        summarizePerc = []
        for idx, el in enumerate(indices):
            computePer = -1
            for each in el:
                if (yData[idx] == yData[each]):
                    computePer = computePer + 1
            summarizePerc.append(computePer)

        for i, el in enumerate(summarizePerc):
            if (el >= (0.8 * kValuesAll[neigh])):
                safeInd.append(i)
            elif (el >= (0.5 * kValuesAll[neigh])):
                borderlineInd.append(i)
            elif (el >= (0.2 * kValuesAll[neigh])):
                rareInd.append(i)
            else:
                outInd.append(i)
        allIndicesTogether = []
        allFlag = True
        for el in typesDataUnder:
            if (el == "safe"):
                allIndicesTogether = allIndicesTogether + safeInd
            elif (el == "borderline"):
                allIndicesTogether = allIndicesTogether + borderlineInd
            elif (el == "rare"):
                allIndicesTogether = allIndicesTogether + rareInd
            elif (el == "outlier"):
                allIndicesTogether = allIndicesTogether + outInd
            else: 
                allFlag = False
        if (allFlag):
            if (len(undersamplNow) == 0):
                boundarySampling = NeighbourhoodCleaningRule(n_neighbors = kOSS_NCR, threshold_cleaning = TS, sampling_strategy=sOSS_SSNCR, n_jobs = -1)
                fit = estimator.fit(XData, yData)
                FI = fit.feature_importances_
                sortedInd = np.argsort(FI.tolist())
                for i in sortedInd:
                    columnsFeatures.append(columnsFeaturesOld[i])
                XData = XData.reindex(columns=columnsFeatures)
                X_test = X_test.reindex(columns=columnsFeatures)
                X_resampledUnder, y_resampledUnder = boundarySampling.fit_resample(XData, yData)
                artificial = pd.concat([XData, X_resampledUnder]).drop_duplicates(keep=False)
                underSamplInd = []
                for each in artificial.index.values:
                    underSamplInd.append(int(each))
                X_resampledUnder.reset_index(drop=True)
                estimator.fit(XData, yData)
                yPredict = cross_val_predict(estimator, XData, yData, cv=crossValidation)
                yPredictProb = cross_val_predict(estimator, XData, yData, cv=crossValidation, method='predict_proba')
                conf = confusion_matrix(yData, yPredict)
                BATrain = balanced_accuracy_score(yData, yPredict)
                FSTrain = f1_score(yData, yPredict, average='macro')
                yDataList = yData[:]

                uniqueyData = list(set(yData))
                occurrences = []
                for value in uniqueyData:
                    temp = yData.count(value)
                    occurrences.append(temp)
                    
                XDataPandas = XData.to_json(orient='records')  
                x = XData.values #returns a numpy array
                min_max_scaler = preprocessing.MinMaxScaler()
                x_scaled = min_max_scaler.fit_transform(x)
                XDataNorm = pd.DataFrame(x_scaled)
                XDataNormPandas = XDataNorm.to_json(orient='records') 

                nbrs = NearestNeighbors(n_neighbors=kValuesAll[neigh], metric="euclidean", n_jobs = -1).fit(XData)
                distances, indices = nbrs.kneighbors(XData)
                summarizePerc = []
                for idx, el in enumerate(indices):
                    computePer = -1
                    for each in el:
                        if (yData[idx] == yData[each]):
                            computePer = computePer + 1
                    summarizePerc.append(computePer)
                ModelSpaceUMAP = FunUMAP(XData, kValuesAll[neigh], minDist)
                ModelSpaceUMAPTest = FunUMAPTest(XData, kValuesAll[neigh], minDist, X_test)
                
                estimator.fit(X_resampledUnder, y_resampledUnder)
                yPredictTest = estimator.predict(X_test)
                yPredictProbTest = estimator.predict_proba(X_test)
                confTest = confusion_matrix(y_test, yPredictTest)
                BATest = balanced_accuracy_score(y_test, yPredictTest)
                FSTest = f1_score(y_test, yPredictTest, average='macro')
                XTestPandas = X_test.to_json(orient='records') 
            else:
                boundarySampling = NeighbourhoodCleaningRule(n_neighbors = kOSS_NCR, threshold_cleaning = TS, sampling_strategy=sOSS_SSNCR, n_jobs = -1)
                XDataNewInverse = XData.iloc[~XData.index.isin(undersamplNow)]
                yDataNewInverse = []
                #localUnderSamplInd = []
                for idx, i in enumerate(yData):
                    # if (idx in underSamplInd):
                    #     if (idx in undersamplNow):
                    #         pass
                    #     else:
                    #         localUnderSamplInd.append(idx)
                    if (idx in undersamplNow):
                        pass
                    else:
                        yDataNewInverse.append(i)
                XData = XDataNewInverse.copy()
                yData = yDataNewInverse.copy()
                XData.reset_index(drop=True)
                #underSamplInd = localUnderSamplInd.copy()
                    
                fit = estimator.fit(XData, yData)
                FI = fit.feature_importances_
                sortedInd = np.argsort(FI.tolist())
                for i in sortedInd:
                    columnsFeatures.append(columnsFeaturesOld[i])
                XData = XData.reindex(columns=columnsFeatures)
                X_test = X_test.reindex(columns=columnsFeatures)
                # X_resampledUnder, y_resampledUnder = boundarySampling.fit_resample(XData, yData)
                # artificial = pd.concat([XData, X_resampledUnder]).drop_duplicates(keep=False)
                underSamplInd = []
                # for each in artificial.index.values:
                #     underSamplInd.append(int(each))
                # X_resampledUnder.reset_index(drop=True)
                estimator.fit(XData, yData)
                yPredict = cross_val_predict(estimator, XData, yData, cv=crossValidation)
                yPredictProb = cross_val_predict(estimator, XData, yData, cv=crossValidation, method='predict_proba')
                conf = confusion_matrix(yData, yPredict)
                BATrain = balanced_accuracy_score(yData, yPredict)
                FSTrain = f1_score(yData, yPredict, average='macro')
                yDataList = yData[:]

                uniqueyData = list(set(yData))
                occurrences = []
                for value in uniqueyData:
                    temp = yData.count(value)
                    occurrences.append(temp)
                    
                XDataPandas = XData.to_json(orient='records')  
                x = XData.values #returns a numpy array
                min_max_scaler = preprocessing.MinMaxScaler()
                x_scaled = min_max_scaler.fit_transform(x)
                XDataNorm = pd.DataFrame(x_scaled)
                XDataNormPandas = XDataNorm.to_json(orient='records') 

                nbrs = NearestNeighbors(n_neighbors=kValuesAll[neigh], metric="euclidean", n_jobs = -1).fit(XData)
                distances, indices = nbrs.kneighbors(XData)

                summarizePerc = []
                for idx, el in enumerate(indices):
                    computePer = -1
                    for each in el:
                        if (yData[idx] == yData[each]):
                            computePer = computePer + 1
                    summarizePerc.append(computePer)
                ModelSpaceUMAP = FunUMAP(XData, kValuesAll[neigh], minDist)
                ModelSpaceUMAPTest = FunUMAPTest(XData, kValuesAll[neigh], minDist, X_test)

                yPredictTest = estimator.predict(X_test)
                yPredictProbTest = estimator.predict_proba(X_test)
                confTest = confusion_matrix(y_test, yPredictTest)
                BATest = balanced_accuracy_score(y_test, yPredictTest)
                FSTest = f1_score(y_test, yPredictTest, average='macro')
                XTestPandas = X_test.to_json(orient='records') 
        else:
            if (len(undersamplNow) == 0):
                boundarySampling = NeighbourhoodCleaningRule(n_neighbors = kOSS_NCR, threshold_cleaning = TS, sampling_strategy=sOSS_SSNCR, n_jobs = -1)
                fit = estimator.fit(XData, yData)
                FI = fit.feature_importances_
                sortedInd = np.argsort(FI.tolist())
                for i in sortedInd:
                    columnsFeatures.append(columnsFeaturesOld[i])
                XData = XData.reindex(columns=columnsFeatures)
                X_test = X_test.reindex(columns=columnsFeatures)
                XDataNew = XData.copy()
                yDataNew = yData.copy()
                XDataNew = XData.iloc[allIndicesTogether]
                XDataNewInverse = XData.iloc[~XData.index.isin(allIndicesTogether)]
                yDataNew = [yData[i] for i in allIndicesTogether]
                X_resampledUnder, y_resampledUnder = boundarySampling.fit_resample(XDataNew, yDataNew)
                artificial = pd.concat([XData, X_resampledUnder]).drop_duplicates(keep=False)

                yDataRemaining = []
                underSamplInd = []
                for each in artificial.index.values:
                    if (each in safeInd):
                        if (typesDataUnder[0] == "safe"):
                            underSamplInd.append(int(each))
                    elif (each in borderlineInd):
                        if (typesDataUnder[1] == "borderline"):
                            underSamplInd.append(int(each))
                    elif (each in rareInd):
                        if (typesDataUnder[2] == "rare"):
                            underSamplInd.append(int(each))
                    else:
                        if (typesDataUnder[3] == "outlier"):
                            underSamplInd.append(int(each))
 
                X_resampledUnder.reset_index(drop=True)
                estimator.fit(XData, yData)
                yPredict = cross_val_predict(estimator, XData, yData, cv=crossValidation)
                yPredictProb = cross_val_predict(estimator, XData, yData, cv=crossValidation, method='predict_proba')
                conf = confusion_matrix(yData, yPredict)
                BATrain = balanced_accuracy_score(yData, yPredict)
                FSTrain = f1_score(yData, yPredict, average='macro')
                yDataList = yData[:]

                uniqueyData = list(set(yData))
                occurrences = []
                for value in uniqueyData:
                    temp = yData.count(value)
                    occurrences.append(temp)
                    
                XDataPandas = XData.to_json(orient='records')  
                x = XData.values #returns a numpy array
                min_max_scaler = preprocessing.MinMaxScaler()
                x_scaled = min_max_scaler.fit_transform(x)
                XDataNorm = pd.DataFrame(x_scaled)
                XDataNormPandas = XDataNorm.to_json(orient='records') 

                nbrs = NearestNeighbors(n_neighbors=kValuesAll[neigh], metric="euclidean", n_jobs = -1).fit(XData)
                distances, indices = nbrs.kneighbors(XData)
                summarizePerc = []
                for idx, el in enumerate(indices):
                    computePer = -1
                    for each in el:
                        if (yData[idx] == yData[each]):
                            computePer = computePer + 1
                    summarizePerc.append(computePer)
                ModelSpaceUMAP = FunUMAP(XData, kValuesAll[neigh], minDist)
                ModelSpaceUMAPTest = FunUMAPTest(XData, kValuesAll[neigh], minDist, X_test)

                XDataTesting = XData.copy()
                XDataTesting['yDat'] = yData
                XDataTesting.drop(underSamplInd, axis=0, inplace=True)
                yDataRemaining = XDataTesting['yDat'].tolist()
                XDataTesting = XDataTesting.drop('yDat', 1)
                estimator.fit(XDataTesting, yDataRemaining)
                yPredictTest = estimator.predict(X_test)
                yPredictProbTest = estimator.predict_proba(X_test)
                confTest = confusion_matrix(y_test, yPredictTest)
                BATest = balanced_accuracy_score(y_test, yPredictTest)
                FSTest = f1_score(y_test, yPredictTest, average='macro')
                XTestPandas = X_test.to_json(orient='records') 
            else:
                boundarySampling = NeighbourhoodCleaningRule(n_neighbors = kOSS_NCR, threshold_cleaning = TS, sampling_strategy=sOSS_SSNCR, n_jobs = -1)
                XDataNewInverse = XData.iloc[~XData.index.isin(undersamplNow)]
                yDataNewInverse = []
                for idx, i in enumerate(yData):
                    if (idx in undersamplNow):
                        pass
                    else:
                        yDataNewInverse.append(i)
                XData = XDataNewInverse.copy()
                yData = yDataNewInverse.copy()
                XData.reset_index(drop=True)
                # X_resampledUnder, y_resampledUnder = boundarySampling.fit_resample(XData, yData)
                # artificial = pd.concat([XData, X_resampledUnder]).drop_duplicates(keep=False)
                underSamplInd = []
                # for each in artificial.index.values:
                #     underSamplInd.append(int(each))
                # X_resampledUnder.reset_index(drop=True)
                fit = estimator.fit(XData, yData)
                FI = fit.feature_importances_
                sortedInd = np.argsort(FI.tolist())
                for i in sortedInd:
                    columnsFeatures.append(columnsFeaturesOld[i])
                XData = XData.reindex(columns=columnsFeatures)
                X_test = X_test.reindex(columns=columnsFeatures)
                estimator.fit(XData, yData)
                yPredict = cross_val_predict(estimator, XData, yData, cv=crossValidation)
                yPredictProb = cross_val_predict(estimator, XData, yData, cv=crossValidation, method='predict_proba')
                conf = confusion_matrix(yData, yPredict)
                BATrain = balanced_accuracy_score(yData, yPredict)
                FSTrain = f1_score(yData, yPredict, average='macro')
                yDataList = yData[:]

                uniqueyData = list(set(yData))
                occurrences = []
                for value in uniqueyData:
                    temp = yData.count(value)
                    occurrences.append(temp)
                    
                XDataPandas = XData.to_json(orient='records')  
                x = XData.values #returns a numpy array
                min_max_scaler = preprocessing.MinMaxScaler()
                x_scaled = min_max_scaler.fit_transform(x)
                XDataNorm = pd.DataFrame(x_scaled)
                XDataNormPandas = XDataNorm.to_json(orient='records') 

                nbrs = NearestNeighbors(n_neighbors=kValuesAll[neigh], metric="euclidean", n_jobs = -1).fit(XData)
                distances, indices = nbrs.kneighbors(XData)

                summarizePerc = []
                for idx, el in enumerate(indices):
                    computePer = -1
                    for each in el:
                        if (yData[idx] == yData[each]):
                            computePer = computePer + 1
                    summarizePerc.append(computePer)
                ModelSpaceUMAP = FunUMAP(XData, kValuesAll[neigh], minDist)
                ModelSpaceUMAPTest = FunUMAPTest(XData, kValuesAll[neigh], minDist, X_test)

                yPredictTest = estimator.predict(X_test)
                yPredictProbTest = estimator.predict_proba(X_test)
                confTest = confusion_matrix(y_test, yPredictTest)
                BATest = balanced_accuracy_score(y_test, yPredictTest)
                FSTest = f1_score(y_test, yPredictTest, average='macro')
                XTestPandas = X_test.to_json(orient='records')          
        
    if (overKey == 0):
        overSamplInd = []
    else:
        columnsFeatures = []
        safeInd = []
        borderlineInd = []
        rareInd = []
        outInd = []
        nbrs = NearestNeighbors(n_neighbors=kValuesAll[neigh], metric="euclidean", n_jobs = -1).fit(XData)
        distances, indices = nbrs.kneighbors(XData)
        summarizePerc = []
        for idx, el in enumerate(indices):
            computePer = -1
            for each in el:
                if (yData[idx] == yData[each]):
                    computePer = computePer + 1
            summarizePerc.append(computePer)

        for i, el in enumerate(summarizePerc):
            if (el >= (0.8 * kValuesAll[neigh])):
                safeInd.append(i)
            elif (el >= (0.5 * kValuesAll[neigh])):
                borderlineInd.append(i)
            elif (el >= (0.2 * kValuesAll[neigh])):
                rareInd.append(i)
            else:
                outInd.append(i)
        allIndicesTogether = []
        sepIndicesSafe = []
        sepIndicesBorder = []
        sepIndicesRare = []
        sepIndicesOut = []
        gatherEachBefore = []
        class0 = 0
        class1 = 0
        class2 = 0
        allFlag = True
        for idx, i in enumerate(yData):
            if (i == 0):
                class0 = class0 + 1
            elif (i == 1):
                class1 = class1 + 1
            else:
                class2 = class2 + 1
        gatherEachBefore.append(class0)
        gatherEachBefore.append(class1)
        gatherEachBefore.append(class2)
        min_indexList = []
        min_value = min(gatherEachBefore)
        min_index = gatherEachBefore.index(min_value)
        max_value = max(gatherEachBefore)
        max_index = gatherEachBefore.index(max_value)
        if (sSMOTE_ADASYN == "minority"):
            for idx, i in enumerate(gatherEachBefore):
                if (idx != max_index and idx != min_index):
                    min_indexList.append(idx)
            min_indexList.append(max_index)
            if (typesData[0] == "safe"):
                allIndicesTogether = allIndicesTogether + safeInd
                sepIndicesSafe = safeInd
            else:
                for val in safeInd:
                    if yData[val] in min_indexList:
                        allIndicesTogether.append(val)
                        sepIndicesSafe.append(val)
            if (typesData[1] == "borderline"):
                allIndicesTogether = allIndicesTogether + borderlineInd
                sepIndicesBorder = borderlineInd
            else:
                for val in borderlineInd:
                    if yData[val] in min_indexList:
                        allIndicesTogether.append(val)
                        sepIndicesBorder.append(val)
            if (typesData[2] == "rare"):
                allIndicesTogether = allIndicesTogether + rareInd
                sepIndicesRare = rareInd
            else:
                for val in rareInd:
                    if yData[val] in min_indexList:
                        allIndicesTogether.append(val)
                        sepIndicesRare.append(val)
            if (typesData[3] == "outlier"):
                allIndicesTogether = allIndicesTogether + outInd
                sepIndicesOut = outInd
            else:
                for val in outInd:
                    if yData[val] in min_indexList:
                        allIndicesTogether.append(val)
                        sepIndicesOut.append(val)
        elif (sSMOTE_ADASYN == "not minority"):
            min_indexList.append(min_index)
            min_indexList.append(max_index)
            if (typesData[0] == "safe"):
                allIndicesTogether = allIndicesTogether + safeInd
                sepIndicesSafe = safeInd
            else:
                for val in safeInd:
                    if yData[val] in min_indexList:
                        allIndicesTogether.append(val)
                        sepIndicesSafe.append(val)
            if (typesData[1] == "borderline"):
                allIndicesTogether = allIndicesTogether + borderlineInd
                sepIndicesBorder = borderlineInd
            else:
                for val in borderlineInd:
                    if yData[val] in min_indexList:
                        allIndicesTogether.append(val)
                        sepIndicesBorder.append(val)
            if (typesData[2] == "rare"):
                allIndicesTogether = allIndicesTogether + rareInd
                sepIndicesRare = rareInd
            else:
                for val in rareInd:
                    if yData[val] in min_indexList:
                        allIndicesTogether.append(val)
                        sepIndicesRare.append(val)
            if (typesData[3] == "outlier"):
                allIndicesTogether = allIndicesTogether + outInd
                sepIndicesOut = outInd
            else:
                for val in outInd:
                    if yData[val] in min_indexList:
                        allIndicesTogether.append(val)
                        sepIndicesOut.append(val)
        elif (sSMOTE_ADASYN == "not majority"):
            min_indexList.append(max_index)
            if (typesData[0] == "safe"):
                allIndicesTogether = allIndicesTogether + safeInd
                sepIndicesSafe = safeInd
            else:
                for val in safeInd:
                    if yData[val] in min_indexList:
                        allIndicesTogether.append(val)
                        sepIndicesSafe.append(val)
            if (typesData[1] == "borderline"):
                allIndicesTogether = allIndicesTogether + borderlineInd
                sepIndicesBorder = borderlineInd
            else:
                for val in borderlineInd:
                    if yData[val] in min_indexList:
                        allIndicesTogether.append(val)
                        sepIndicesBorder.append(val)
            if (typesData[2] == "rare"):
                allIndicesTogether = allIndicesTogether + rareInd
                sepIndicesRare = rareInd
            else:
                for val in rareInd:
                    if yData[val] in min_indexList:
                        allIndicesTogether.append(val)
                        sepIndicesRare.append(val)
            if (typesData[3] == "outlier"):
                allIndicesTogether = allIndicesTogether + outInd
                sepIndicesOut = outInd
            else:
                for val in outInd:
                    if yData[val] in min_indexList:
                        allIndicesTogether.append(val)
                        sepIndicesOut.append(val)
        else:
            for el in typesData:
                if (el == "safe"):
                    allIndicesTogether = allIndicesTogether + safeInd
                    sepIndicesSafe = safeInd
                elif (el == "borderline"):
                    allIndicesTogether = allIndicesTogether + borderlineInd
                    sepIndicesBorder = borderlineInd
                elif (el == "rare"):
                    allIndicesTogether = allIndicesTogether + rareInd
                    sepIndicesRare = rareInd
                elif (el == "outlier"):
                    allIndicesTogether = allIndicesTogether + outInd
                    sepIndicesOut = outInd
                else: 
                    pass

        for el in typesData:
            if el == '':
                allFlag = False

        if (overKey == 1):  
            boundarySampling = SMOTE(k_neighbors = kSMOTE_ADASYN, sampling_strategy=sSMOTE_ADASYN, random_state = RANDOM_SEED, n_jobs = -1)
        else:
            boundarySampling = ADASYN(n_neighbors = kSMOTE_ADASYN, sampling_strategy=sSMOTE_ADASYN, random_state = RANDOM_SEED, n_jobs = -1)
        if (allFlag):
            if (len(oversamplNow) == 0):
                X_resampled, y_resampled = boundarySampling.fit_resample(XData, yData)
                artificial = pd.concat([XData, X_resampled]).drop_duplicates(keep=False)
                overSamplInd = []
                for each in artificial.index.values:
                    overSamplInd.append(int(each))
                X_resampled.reset_index(drop=True)
                fit = estimator.fit(X_resampled, y_resampled)
                FI = fit.feature_importances_
                sortedInd = np.argsort(FI.tolist())
                for i in sortedInd:
                    columnsFeatures.append(columnsFeaturesOld[i])
                X_resampled = X_resampled.reindex(columns=columnsFeatures)
                X_test = X_test.reindex(columns=columnsFeatures)
                estimator.fit(X_resampled, y_resampled)
                yPredict = cross_val_predict(estimator, X_resampled, y_resampled, cv=crossValidation)
                yPredictProb = cross_val_predict(estimator, X_resampled, y_resampled, cv=crossValidation, method='predict_proba')
                conf = confusion_matrix(y_resampled, yPredict)
                BATrain = balanced_accuracy_score(y_resampled, yPredict)
                FSTrain = f1_score(y_resampled, yPredict, average='macro')
                yDataList = y_resampled[:]

                uniqueyData = list(set(y_resampled))
                occurrences = []
                for value in uniqueyData:
                    temp = y_resampled.count(value)
                    occurrences.append(temp)
                    
                XDataPandas = X_resampled.to_json(orient='records')  
                x = X_resampled.values #returns a numpy array
                min_max_scaler = preprocessing.MinMaxScaler()
                x_scaled = min_max_scaler.fit_transform(x)
                XDataNorm = pd.DataFrame(x_scaled)
                XDataNormPandas = XDataNorm.to_json(orient='records') 

                nbrs = NearestNeighbors(n_neighbors=kValuesAll[neigh], metric="euclidean", n_jobs = -1).fit(X_resampled)
                distances, indices = nbrs.kneighbors(X_resampled)
                summarizePerc = []
                for idx, el in enumerate(indices):
                    computePer = -1
                    for each in el:
                        if (y_resampled[idx] == y_resampled[each]):
                            computePer = computePer + 1
                    summarizePerc.append(computePer)
                ModelSpaceUMAP = FunUMAP(X_resampled, kValuesAll[neigh], minDist)
                ModelSpaceUMAPTest = FunUMAPTest(X_resampled, kValuesAll[neigh], minDist, X_test)
           
                yPredictTest = estimator.predict(X_test)
                yPredictProbTest = estimator.predict_proba(X_test)
                confTest = confusion_matrix(y_test, yPredictTest)
                BATest = balanced_accuracy_score(y_test, yPredictTest)
                FSTest = f1_score(y_test, yPredictTest, average='macro')
                XTestPandas = X_test.to_json(orient='records') 
            else:
                X_resampled, y_resampled = boundarySampling.fit_resample(XData, yData)
                XDataNewInverse = X_resampled.iloc[X_resampled.index.isin(oversamplNow)]
                XDataNewInverseAll = pd.concat([XData, XDataNewInverse])
                yDataNewInverse = []
                for idx, i in enumerate(y_resampled):
                    if (idx in oversamplNow):
                        yDataNewInverse.append(i)
                
                yDataNewInverseAll = yData + yDataNewInverse
                        
                XData = XDataNewInverseAll.copy()
                yData = yDataNewInverseAll.copy()
                XData = XData.reset_index(drop=True)
                # X_resampled, y_resampled = boundarySampling.fit_resample(XData, yData)
                # artificial = pd.concat([XData, X_resampled]).drop_duplicates(keep=False)
                overSamplInd = []
                # for each in artificial.index.values:
                #     overSamplInd.append(int(each))
                # X_resampled.reset_index(drop=True)
                fit = estimator.fit(XData, yData)
                FI = fit.feature_importances_
                sortedInd = np.argsort(FI.tolist())
                for i in sortedInd:
                    columnsFeatures.append(columnsFeaturesOld[i])
                XData = XData.reindex(columns=columnsFeatures)
                X_test = X_test.reindex(columns=columnsFeatures)
                estimator.fit(XData, yData)
                yPredict = cross_val_predict(estimator, XData, yData, cv=crossValidation)
                yPredictProb = cross_val_predict(estimator, XData, yData, cv=crossValidation, method='predict_proba')
                conf = confusion_matrix(yData, yPredict)
                BATrain = balanced_accuracy_score(yData, yPredict)
                FSTrain = f1_score(yData, yPredict, average='macro')
                yDataList = yData[:]

                uniqueyData = list(set(yData))
                occurrences = []
                for value in uniqueyData:
                    temp = yData.count(value)
                    occurrences.append(temp)
                    
                XDataPandas = XData.to_json(orient='records')  
                x = XData.values #returns a numpy array
                min_max_scaler = preprocessing.MinMaxScaler()
                x_scaled = min_max_scaler.fit_transform(x)
                XDataNorm = pd.DataFrame(x_scaled)
                XDataNormPandas = XDataNorm.to_json(orient='records') 

                nbrs = NearestNeighbors(n_neighbors=kValuesAll[neigh], metric="euclidean", n_jobs = -1).fit(XData)
                distances, indices = nbrs.kneighbors(XData)
                summarizePerc = []
                for idx, el in enumerate(indices):
                    computePer = -1
                    for each in el:
                        if (yData[idx] == yData[each]):
                            computePer = computePer + 1
                    summarizePerc.append(computePer)
                ModelSpaceUMAP = FunUMAP(XData, kValuesAll[neigh], minDist)
                ModelSpaceUMAPTest = FunUMAPTest(XData, kValuesAll[neigh], minDist, X_test)
                
                yPredictTest = estimator.predict(X_test)
                yPredictProbTest = estimator.predict_proba(X_test)
                confTest = confusion_matrix(y_test, yPredictTest)
                BATest = balanced_accuracy_score(y_test, yPredictTest)
                FSTest = f1_score(y_test, yPredictTest, average='macro')
                XTestPandas = X_test.to_json(orient='records') 
        else:
            if (len(oversamplNow) == 0):
                XDataNew = XData.copy()
                yDataNew = yData.copy()

                gatherEachClass = []
                class0 = 0
                class1 = 0
                class2 = 0
                for idx, i in enumerate(yDataNew):
                    if (i == 0):
                        if idx in sepIndicesSafe:
                            pass
                        elif idx in sepIndicesBorder:
                            pass
                        elif idx in sepIndicesRare:
                            pass
                        elif idx in sepIndicesOut:
                            pass
                        else:
                            class0 = class0 + 1
                    elif (i == 1):
                        if idx in sepIndicesSafe:
                            pass
                        elif idx in sepIndicesBorder:
                            pass
                        elif idx in sepIndicesRare:
                            pass
                        elif idx in sepIndicesOut:
                            pass
                        else:
                            class1 = class1 + 1
                    else:
                        if idx in sepIndicesSafe:
                            pass
                        elif idx in sepIndicesBorder:
                            pass
                        elif idx in sepIndicesRare:
                            pass
                        elif idx in sepIndicesOut:
                            pass
                        else:
                            class2 = class2 + 1
                
                gatherEachClass.append(class0)
                gatherEachClass.append(class1)
                gatherEachClass.append(class2)

                strategicTuples = {}
                counter = Counter(yDataNew)
                all_values = counter.values()
                maxVal = max(all_values)
                minVal = min(all_values)
                minInd = list(counter.keys())[list(counter.values()).index(minVal)]
                    
                if (sSMOTE_ADASYN == "minority"):
                    for k,v in counter.items():
                        if (k == minInd):
                            strategicTuples[k] = (maxVal - gatherEachClass[k])
                        else:
                            strategicTuples[k] = (counter[k] - gatherEachClass[k])
                elif (sSMOTE_ADASYN == "not minority"):
                    for k,v in counter.items():
                        if (k == minInd):
                            strategicTuples[k] = (counter[k] - gatherEachClass[k])
                        else:
                            strategicTuples[k] = (maxVal - gatherEachClass[k])
                elif (sSMOTE_ADASYN == "not majority"):
                    for k,v in counter.items():
                        strategicTuples[k] = (maxVal - gatherEachClass[k])
                else:
                    for k,v in counter.items():
                        strategicTuples[k] = (maxVal - gatherEachClass[k])

                if (overKey == 1):  
                    boundarySampling = SMOTE(k_neighbors = kSMOTE_ADASYN, sampling_strategy=strategicTuples, random_state = RANDOM_SEED, n_jobs = -1)
                else:
                    boundarySampling = ADASYN(n_neighbors = kSMOTE_ADASYN, sampling_strategy=strategicTuples, random_state = RANDOM_SEED, n_jobs = -1)

                XDataNew = XData.iloc[allIndicesTogether]
                XDataNewInverse = XData.iloc[~XData.index.isin(allIndicesTogether)]
                yDataNew = [yData[i] for i in allIndicesTogether]

                yDataNewInverse = []
                for idx, i in enumerate(yData):
                    if (idx in allIndicesTogether):
                        pass
                    else:
                        yDataNewInverse.append(i)

                X_resampled, y_resampled = boundarySampling.fit_resample(XDataNew, yDataNew)
                X_resampled.index += sum(gatherEachClass)
                X_resampledWithoutDupl = pd.concat([XDataNew, X_resampled]).drop_duplicates(keep=False)
                X_resampledAll = pd.concat([XData, X_resampledWithoutDupl])
                yDataWithoutDupl = []
                for idx, i in enumerate(y_resampled):
                    if ((sum(gatherEachClass)+idx) >= len(yData)):
                        yDataWithoutDupl.append(i)
                y_resampledAll = yData + yDataWithoutDupl
                artificial = X_resampledWithoutDupl
                overSamplInd = []
                for each in artificial.index.values:
                    overSamplInd.append(int(each))
                fit = estimator.fit(X_resampledAll, y_resampledAll)
                FI = fit.feature_importances_
                sortedInd = np.argsort(FI.tolist())
                for i in sortedInd:
                    columnsFeatures.append(columnsFeaturesOld[i])
                X_resampledAll = X_resampledAll.reindex(columns=columnsFeatures)
                X_test = X_test.reindex(columns=columnsFeatures)
                estimator.fit(X_resampledAll, y_resampledAll)
                yPredict = cross_val_predict(estimator, X_resampledAll, y_resampledAll, cv=crossValidation)
                yPredictProb = cross_val_predict(estimator, X_resampledAll, y_resampledAll, cv=crossValidation, method='predict_proba')
                conf = confusion_matrix(y_resampledAll, yPredict)
                BATrain = balanced_accuracy_score(y_resampledAll, yPredict)
                FSTrain = f1_score(y_resampledAll, yPredict, average='macro')
                yDataList = y_resampledAll[:]
                uniqueyData = list(set(y_resampledAll))
                occurrences = []
                for value in uniqueyData:
                    temp = y_resampledAll.count(value)
                    occurrences.append(temp)
                    
                XDataPandas = X_resampledAll.to_json(orient='records')  
                x = X_resampledAll.values #returns a numpy array
                min_max_scaler = preprocessing.MinMaxScaler()
                x_scaled = min_max_scaler.fit_transform(x)
                XDataNorm = pd.DataFrame(x_scaled)
                XDataNormPandas = XDataNorm.to_json(orient='records') 

                nbrs = NearestNeighbors(n_neighbors=kValuesAll[neigh], metric="euclidean", n_jobs = -1).fit(X_resampledAll)
                distances, indices = nbrs.kneighbors(X_resampledAll)
                summarizePerc = []
                for idx, el in enumerate(indices):
                    computePer = -1
                    for each in el:
                        if (y_resampledAll[idx] == y_resampledAll[each]):
                            computePer = computePer + 1
                    summarizePerc.append(computePer)
                ModelSpaceUMAP = FunUMAP(X_resampledAll, kValuesAll[neigh], minDist)
                ModelSpaceUMAPTest = FunUMAPTest(X_resampledAll, kValuesAll[neigh], minDist, X_test)

                yPredictTest = estimator.predict(X_test)
                yPredictProbTest = estimator.predict_proba(X_test)
                confTest = confusion_matrix(y_test, yPredictTest)
                BATest = balanced_accuracy_score(y_test, yPredictTest)
                FSTest = f1_score(y_test, yPredictTest, average='macro')
                XTestPandas = X_test.to_json(orient='records') 
            else:
                XDataNew = XData.copy()
                yDataNew = yData.copy()
                gatherEachClass = []
                class0 = 0
                class1 = 0
                class2 = 0
                for idx, i in enumerate(yDataNew):
                    if (i == 0):
                        if idx in sepIndicesSafe:
                            pass
                        elif idx in sepIndicesBorder:
                            pass
                        elif idx in sepIndicesRare:
                            pass
                        elif idx in sepIndicesOut:
                            pass
                        else:
                            class0 = class0 + 1
                    elif (i == 1):
                        if idx in sepIndicesSafe:
                            pass
                        elif idx in sepIndicesBorder:
                            pass
                        elif idx in sepIndicesRare:
                            pass
                        elif idx in sepIndicesOut:
                            pass
                        else:
                            class1 = class1 + 1
                    else:
                        if idx in sepIndicesSafe:
                            pass
                        elif idx in sepIndicesBorder:
                            pass
                        elif idx in sepIndicesRare:
                            pass
                        elif idx in sepIndicesOut:
                            pass
                        else:
                            class2 = class2 + 1
                
                gatherEachClass.append(class0)
                gatherEachClass.append(class1)
                gatherEachClass.append(class2)

                strategicTuples = {}
                counter = Counter(yDataNew)
                
                all_values = counter.values()
                maxVal = max(all_values)
                minVal = min(all_values)
                minInd = list(counter.keys())[list(counter.values()).index(minVal)]

                if (sSMOTE_ADASYN == "minority"):
                    for k,v in counter.items():
                        if (k == minInd):
                            strategicTuples[k] = (maxVal - gatherEachClass[k])
                        else:
                            strategicTuples[k] = (counter[k] - gatherEachClass[k])
                elif (sSMOTE_ADASYN == "not minority"):
                    for k,v in counter.items():
                        if (k == minInd):
                            strategicTuples[k] = (counter[k] - gatherEachClass[k])
                        else:
                            strategicTuples[k] = (maxVal - gatherEachClass[k])
                elif (sSMOTE_ADASYN == "not majority"):
                    for k,v in counter.items():
                        strategicTuples[k] = (maxVal - gatherEachClass[k])
                else:
                    for k,v in counter.items():
                        strategicTuples[k] = (maxVal - gatherEachClass[k])
                if (overKey == 1):  
                    boundarySampling = SMOTE(k_neighbors = kSMOTE_ADASYN, sampling_strategy=strategicTuples, random_state = RANDOM_SEED, n_jobs = -1)
                else:
                    boundarySampling = ADASYN(n_neighbors = kSMOTE_ADASYN, sampling_strategy=strategicTuples, random_state = RANDOM_SEED, n_jobs = -1)

                XDataNew = XData.iloc[allIndicesTogether]
                XDataNewInverse = XData.iloc[~XData.index.isin(allIndicesTogether)]
                yDataNew = [yData[i] for i in allIndicesTogether]

                yDataNewInverse = []
                for idx, i in enumerate(yData):
                    if (idx in allIndicesTogether):
                        pass
                    else:
                        yDataNewInverse.append(i)
                X_resampled, y_resampled = boundarySampling.fit_resample(XDataNew, yDataNew)
                X_resampled.index += sum(gatherEachClass)
                X_resampledWithoutDupl = pd.concat([XDataNew, X_resampled]).drop_duplicates(keep=False)
                XData = XData.reset_index(drop=True)
                X_resampledAll = pd.concat([XData, X_resampledWithoutDupl])
                yDataWithoutDupl = []
                for idx, i in enumerate(y_resampled):
                    if ((sum(gatherEachClass)+idx) >= len(yData)):
                        yDataWithoutDupl.append(i)
                y_resampledAll = yData + yDataWithoutDupl
                overSamplInd = []            
                XDataNewInverseLocal = X_resampledAll.iloc[X_resampledAll.index.isin(oversamplNow)]
                XDataNewInverseAll = pd.concat([XData, XDataNewInverseLocal])
                yDataNewInverseLocal = []
                for idx, i in enumerate(y_resampledAll):
                    if idx in oversamplNow:
                        yDataNewInverseLocal.append(i)
                yDataNewInverseAll = yData + yDataNewInverseLocal
                XData = XDataNewInverseAll.copy()
                yData = yDataNewInverseAll.copy()
                XData = XData.reset_index(drop=True)
                overSamplInd = []
                fit = estimator.fit(XData, yData)
                FI = fit.feature_importances_
                sortedInd = np.argsort(FI.tolist())
                for i in sortedInd:
                    columnsFeatures.append(columnsFeaturesOld[i])
                XData = XData.reindex(columns=columnsFeatures)
                X_test = X_test.reindex(columns=columnsFeatures)
                #estimator.fit(X_resampledAll, y_resampledAll)
                estimator.fit(XData, yData)
                yPredict = cross_val_predict(estimator, XData, yData, cv=crossValidation)
                yPredictProb = cross_val_predict(estimator, XData, yData, cv=crossValidation, method='predict_proba')
                conf = confusion_matrix(yData, yPredict)
                BATrain = balanced_accuracy_score(yData, yPredict)
                FSTrain = f1_score(yData, yPredict, average='macro')
                yDataList = yData[:]

                uniqueyData = list(set(yData))
                occurrences = []
                for value in uniqueyData:
                    temp = yData.count(value)
                    occurrences.append(temp)
                    
                XDataPandas = XData.to_json(orient='records')  
                x = XData.values #returns a numpy array
                min_max_scaler = preprocessing.MinMaxScaler()
                x_scaled = min_max_scaler.fit_transform(x)
                XDataNorm = pd.DataFrame(x_scaled)
                XDataNormPandas = XDataNorm.to_json(orient='records') 

                nbrs = NearestNeighbors(n_neighbors=kValuesAll[neigh], metric="euclidean", n_jobs = -1).fit(XData)
                distances, indices = nbrs.kneighbors(XData)
                summarizePerc = []
                for idx, el in enumerate(indices):
                    computePer = -1
                    for each in el:
                        if (yData[idx] == yData[each]):
                            computePer = computePer + 1
                    summarizePerc.append(computePer)
                ModelSpaceUMAP = FunUMAP(XData, kValuesAll[neigh], minDist)
                ModelSpaceUMAPTest = FunUMAPTest(XData, kValuesAll[neigh], minDist, X_test)
                
                yPredictTest = estimator.predict(X_test)
                yPredictProbTest = estimator.predict_proba(X_test)
                confTest = confusion_matrix(y_test, yPredictTest)
                BATest = balanced_accuracy_score(y_test, yPredictTest)
                FSTest = f1_score(y_test, yPredictTest, average='macro')
                XTestPandas = X_test.to_json(orient='records') 

    finalResultsData.append(json.dumps(yPredictProb.tolist())) # 0
    finalResultsData.append(json.dumps(target_names)) # 1
    finalResultsData.append(yDataList) # 2
    finalResultsData.append(occurrences) # 3
    finalResultsData.append(json.dumps(conf.tolist())) # 4
    finalResultsData.append(json.dumps(yPredict.tolist())) # 5
    finalResultsData.append(json.dumps(XDataPandas)) # 6
    finalResultsData.append(json.dumps(underSamplInd)) # 7
    finalResultsData.append(summarizePerc) # 8
    finalResultsData.append(ModelSpaceUMAP) # 9 
    finalResultsData.append(columnsFeatures) # 10
    finalResultsData.append(json.dumps(XDataNormPandas)) # 11
    finalResultsData.append(json.dumps(overSamplInd)) # 12
    finalResultsData.append(json.dumps(confTest.tolist())) # 13
    finalResultsData.append(json.dumps(countPercentageList)) # 14
    finalResultsData.append(json.dumps(storeAllMetricsList)) # 15
    finalResultsData.append(json.dumps(sortShepCorrList)) # 16
    finalResultsData.append(ModelSpaceUMAPTest) # 17
    finalResultsData.append(y_test) #18
    finalResultsData.append(json.dumps(yPredictTest.tolist())) #19
    finalResultsData.append(json.dumps(XTestPandas)) # 20
    finalResultsData.append(json.dumps(yPredictProbTest.tolist())) # 21
    finalResultsData.append(json.dumps(BATest.tolist())) # 22
    finalResultsData.append(json.dumps(FSTest.tolist())) # 23
    finalResultsData.append(json.dumps(GatherSafe)) # 24
    finalResultsData.append(json.dumps(GatherBorder)) # 25
    finalResultsData.append(json.dumps(GatherRare)) # 26
    finalResultsData.append(json.dumps(GatherOut)) # 27
    finalResultsData.append(json.dumps(UMAPModalStore)) # 28
    finalResultsData.append(json.dumps(MaxValue)) # 29
    finalResultsData.append(json.dumps(MaxIndex)) # 30
    finalResultsData.append(json.dumps(BATrain.tolist())) # 31
    finalResultsData.append(json.dumps(FSTrain.tolist())) # 32
    return 'Everything Okay'

@app.route('/data/PerformanceForEachModel', methods=["GET", "POST"])
def sendFinalResults():
    
    response = {    
        'PerformancePerModel': finalResultsData
    }
    return jsonify(response)    

def FunUMAPTest (data, neighbors, minDist, dataTest):
    trans = umap.UMAP(n_neighbors=neighbors+1, min_dist=minDist, random_state=RANDOM_SEED).fit(data)
    test_embedding = trans.transform(dataTest)
    Xpos = test_embedding[:, 0].tolist()
    Ypos = test_embedding[:, 1].tolist()
    return [Xpos,Ypos]

def FunUMAP (data, neighbors, minDist):
    trans = umap.UMAP(n_neighbors=neighbors+1, min_dist=minDist, random_state=RANDOM_SEED).fit(data)
    Xpos = trans.embedding_[:, 0].tolist()
    Ypos = trans.embedding_[:, 1].tolist()
    return [Xpos,Ypos]

def FunUMAPAll (data, neighbors, minDist):
    trans = umap.UMAP(n_neighbors=neighbors+1, min_dist=minDist, random_state=RANDOM_SEED).fit(data)
    All = trans.embedding_[:, :].tolist()
    return All

def shepard_diagram_correlation(D_high, D_low):
    if len(D_high.shape) > 1:
        D_high = spatial.distance.squareform(D_high)
    if len(D_low.shape) > 1:
        D_low = spatial.distance.squareform(D_low)

    return stats.spearmanr(D_high, D_low)[0]

@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
@app.route('/data/updateValues', methods=["GET", "POST"])
def updateValuesFun():

    RetrievedUpdate = request.get_data().decode('utf8').replace("'", '"')
    RetrievedUpdate = json.loads(RetrievedUpdate)

    key = 1
    undersamplNow = []
    neigh = RetrievedUpdate['neigh']
    underKey = RetrievedUpdate['underKey']
    kOSS_NCR = RetrievedUpdate['kOSS_NCR']
    sOSS_SSNCR = RetrievedUpdate['sOSS_SSNCR']
    NS = RetrievedUpdate['NS']
    TS = RetrievedUpdate['TS']
    oversamplNow = []
    overKey = RetrievedUpdate['overKey']
    kSMOTE_ADASYN = RetrievedUpdate['kSMOTE_ADASYN']
    sSMOTE_ADASYN = RetrievedUpdate['sSMOTE_ADASYN']
    typesData = RetrievedUpdate['typesData']
    minDist = RetrievedUpdate['minDist']
    typesDataUnder = RetrievedUpdate['typesDataUnder']
    executeSearch(key, undersamplNow, neigh, underKey, kOSS_NCR, sOSS_SSNCR, typesDataUnder, NS, TS, oversamplNow, overKey, kSMOTE_ADASYN, sSMOTE_ADASYN, minDist, typesData)
    #executeSearch(key, undersamplNow, neigh, underKey, kOSS_NCR, sOSS_SSNCR, typesDataUnder, NS, TS, oversamplNow, overKey, kSMOTE_ADASYN, sSMOTE_ADASYN, minDist, typesData)

    return 'Everything Okay'

@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
@app.route('/data/UnderS', methods=["GET", "POST"])
def UnderSFun():

    RetrievedUpdate = request.get_data().decode('utf8').replace("'", '"')
    RetrievedUpdate = json.loads(RetrievedUpdate)

    key = 1
    undersamplNow = RetrievedUpdate['actionUnder']
    neigh = RetrievedUpdate['neigh']
    underKey = RetrievedUpdate['underKey']
    kOSS_NCR = RetrievedUpdate['kOSS_NCR']
    sOSS_SSNCR = RetrievedUpdate['sOSS_SSNCR']
    NS = RetrievedUpdate['NS']
    TS = RetrievedUpdate['TS']
    oversamplNow = RetrievedUpdate['actionOver']
    overKey = RetrievedUpdate['overKey']
    kSMOTE_ADASYN = RetrievedUpdate['kSMOTE_ADASYN']
    sSMOTE_ADASYN = RetrievedUpdate['sSMOTE_ADASYN']
    typesData = RetrievedUpdate['typesData']
    minDist = RetrievedUpdate['minDist']
    typesDataUnder = RetrievedUpdate['typesDataUnder']

    executeSearch(key, undersamplNow, neigh, underKey, kOSS_NCR, sOSS_SSNCR, typesDataUnder, NS, TS, oversamplNow, overKey, kSMOTE_ADASYN, sSMOTE_ADASYN, minDist, typesData)
    
    return 'Everything Okay'

@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
@app.route('/data/OverS', methods=["GET", "POST"])
def OverSFun():

    RetrievedUpdate = request.get_data().decode('utf8').replace("'", '"')
    RetrievedUpdate = json.loads(RetrievedUpdate)

    key = 1
    undersamplNow = RetrievedUpdate['actionUnder']
    neigh = RetrievedUpdate['neigh']
    underKey = RetrievedUpdate['underKey']
    kOSS_NCR = RetrievedUpdate['kOSS_NCR']
    sOSS_SSNCR = RetrievedUpdate['sOSS_SSNCR']
    NS = RetrievedUpdate['NS']
    TS = RetrievedUpdate['TS']
    oversamplNow = RetrievedUpdate['actionOver']
    overKey = RetrievedUpdate['overKey']
    kSMOTE_ADASYN = RetrievedUpdate['kSMOTE_ADASYN']
    sSMOTE_ADASYN = RetrievedUpdate['sSMOTE_ADASYN']
    typesData = RetrievedUpdate['typesData']
    minDist = RetrievedUpdate['minDist']
    typesDataUnder = RetrievedUpdate['typesDataUnder']
    executeSearch(key, undersamplNow, neigh, underKey, kOSS_NCR, sOSS_SSNCR, typesDataUnder, NS, TS, oversamplNow, overKey, kSMOTE_ADASYN, sSMOTE_ADASYN, minDist, typesData)
    
    return 'Everything Okay'
