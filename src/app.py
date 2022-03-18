import json
import pickle
import numpy as np
import boto3
import subprocess
import librosa
import os

from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler


s3 = boto3.resource('s3')
bucket = s3.Bucket('jovi-ser')




def extract_features(data, sample_rate):

    mfccs = librosa.feature.mfcc(y=data, sr=22050, n_mfcc=58)
    mfccs_processed = np.mean(mfccs.T, axis=0)
    return np.array(mfccs_processed)


def handler(event, context):
    
    Key= event['Key']
    if not os.path.exists('/tmp/recording'):
        os.mkdir('/tmp/recording')

    bucket.download_file(Key, '/tmp/'+Key)
  
    data, sample_rate = librosa.load('/tmp/'+Key, duration=2.5, offset=0.6)
    scaler= pickle.load(open('model/stdscaler.pickle', 'rb'))
    encoder = pickle.load(open('model/encoder.pickle', 'rb'))
    X = extract_features(data, sample_rate)
    x_test = scaler.transform(X.reshape(1,58))
    data = np.expand_dims(x_test, axis=2)
    
    model = load_model('model/SER_model.h5')
    res = model(data)
    prob=np.array(res[0])
    
    res =dict(sorted(zip(prob,encoder.get_feature_names()), reverse=True)[:2])
    flag=0
    if sorted(list(res.values()))==['x0_angry','x0_fear']:
        model = load_model('model/AF_model.h5')
        encoder = pickle.load(open('model/AF_encoder.pickle', 'rb'))
        flag=1
    elif sorted(list(res.values()))==['x0_surprise','x0_happy']:
        model = load_model('model/SH_model.h5')
        encoder = pickle.load(open('model/SH_encoder.pickle', 'rb'))
        flag=1
    elif sorted(list(res.values()))==['x0_sad','x0_disgust']:
        model = load_model('model/SD_model.h5')
        encoder = pickle.load(open('model/SD_encoder.pickle', 'rb'))
        flag=1
    if flag==1:
        res = model(data)
        prob=np.array(res[0])
        res =dict(sorted(zip(prob,encoder.get_feature_names()), reverse=True)[:2])
    res = {v: str(round((k*100), 2)) for k, v in res.items()}
    print(res)
        
    response = {"statusCode": 200, "body": json.dumps(res)}
    return response
