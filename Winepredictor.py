import logging
import pandas as pd
import pickle
from google.cloud import storage
import json
from io import StringIO
class WinePredictor:
    def __init__(self, model_file):
        self.model = None

    def RetrieveModel(self,filename):
        #variables
        project_id = "your-gcp-project-id"
        model_bucket_name = "your-model-bucket"

        # Initialize the GCS client
        client = storage.Client(project=project_id)
        bucket = client.bucket(model_bucket_name)
        blob = bucket.blob(filename)

        # Download scaler_model.pkl
        scaler_blob = bucket.blob('scaler_model.pkl')
        scaler_blob.download_to_filename('models/scaler_model.pkl')
    
        # Download the file to the component's output path
        blob.download_to_filename('models/'+filename)
        bestmodel = pickle.load(open('models/'+filename, 'rb'))    
        return bestmodel
    
    def predict_single_record(self, df):
        if self.model is None:
            try:
                self.model= self.RetrieveModel('model.pkl')
            except RuntimeError as err:
                print(err)
        
        #scale the data
        with open('models/scaler_model.pkl', 'rb') as file:
            scaler = pickle.load(file)
        scaled_data = scaler.transform(df)
        y_pred = self.model.predict(scaled_data)
        return y_pred
