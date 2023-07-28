import joblib 

with open('previous_encoder.pkl', 'rb') as f:
    previous_enc = joblib.load(f)

with open('icd_encoder.pkl', 'rb')  as f:
    icd_enc = joblib.load(f)

with open('lab_encoder.pkl', 'rb') as f:
    lab_enc = joblib.load(f)

with open('imaging_encoder.pkl', 'rb') as f:
    imaging_enc = joblib.load(f)

with open('best_model.pkl', 'rb') as f:
    model = joblib.load(f)