import xgboost as xgb
import pandas
import sys
import numpy
path1 = '/home/data/FlareconML/static_file_analyzer/classifier/learning/'
file1 = 'M=xgbtree=home-data-TrendX-1layer-20160622_ATSE_1036_allfeats_dllapi_hb_100=xgb-n500-d15-fhb100-l0.05=23310838.xgboost_model'

def dodetect(modelname,X_test):
    if not modelname.endswith(".pkl"):
        model = xgb.Booster()
        model.load_model(modelname)
        dtest =xgb.DMatrix(X_test,missing=numpy.nan)
        predicted = model.predict(dtest)
    else:
        from sklearn.externals import joblib
        model = joblib.load(modelname) 
        predicted = model.predict(X_test)
    return predicted

def loaddata(model1,file2):
    fc = open(file2)
    ic = 0
    while True:
        line = fc.readline()
        if not line: break
        ic = ic +1
    fc.close()
    resultarr = []
    i = 0
    while i<ic:
        upb = min(i+1000000,ic)
        f1 = pandas.read_csv(file2,nrows=(upb-i),skiprows=i,header=None)
        X = f1.ix[:,1:]
        SHA1 = f1.ix[:,0]
        result = dodetect(model1,X)
        R1 = pandas.DataFrame({'sha1':SHA1,'PredictScore':result})
        R1["m"] = R1.PredictScore.map(lambda x:1 if float(x)>0.5 else 0)
        R2 = R1.ix[:,["sha1","PredictScore","m"]]
        dcount = sum(R2.m.tolist())
        dall = len(result)
        fw = open("__DETECTION.log",'a')
        fw.write(file2+"\t"+str(i)+"\t"+str(dcount)+"\t"+str(dall)+"\t"+str(round(dcount*1.0/dall,4))+"\n")
        fw.close()
        print R2.m.value_counts()
        i = i+1000000
        resultarr.append(R2)        
    return pandas.concat(resultarr,axis=0,ignore_index=True)
    

def loaddata_(model1,file2):
    f1 = pandas.read_csv(file2,header=None)
    resultarr = []
    i = 0
    while i<f1.shape[0]:
        upb = min(i+1000000,f1.shape[0]-1)
        X = f1.ix[i:upb,1:]
        SHA1 = f1.ix[i:upb,0]
        result = dodetect(model1,X)
        R1 = pandas.DataFrame({'sha1':SHA1,'PredictScore':result})
        R1["m"] = R1.PredictScore.map(lambda x:1 if float(x)>0.5 else 0)
        R2 = R1.ix[:,["sha1","PredictScore","m"]]
        dcount = sum(R2.m.tolist())
        dall = len(result)
        fw = open("__DETECTION.log",'a')
        fw.write(file2+"\t"+str(i)+"\t"+str(dcount)+"\t"+str(dall)+"\t"+str(round(dcount*1.0/dall,4))+"\n")
        fw.close()
        print R2.m.value_counts()
        i = i+1000000
        resultarr.append(R2)
    return pandas.concat(resultarr,axis=0,ignore_index=True)

"""

USE a MODEL(1) detect data(2) and output results(3)

"""

modelname = sys.argv[1]
testfile = sys.argv[2]   
result1 = sys.argv[3]

R1 = loaddata(modelname,testfile)
R1.to_csv(result1,index=False)

