import numpy as np
import cv2
import joblib
from collections import Counter
from glob import glob

def process_image(img_path):
    img = cv2.imread(img_path, 0)
    img = cv2.resize(img, (200, 200))
    return img

def results_analysis(predictions):
    classes = {
        2: 'Actinic Keratosis Basal Cell Carcinoma',
        6: 'Eczema',
        15: 'Psoriasis, Lichen Planus',
        17: 'Seborrheic Keratoses',
        19: 'Tinea Ringworm Candidiasis'
    }
    
    # Tally the predictions
    prediction_counts = Counter(predictions)
    
    # Calculate total images
    total_images = len(predictions)
    
    # Prepare ranked results
    ranked_results = []
    for pred, count in prediction_counts.most_common():
        match_percentage = (count / total_images) * 100
        ranked_results.append((classes.get(pred, 'Not Found'), match_percentage))
    
    return ranked_results

def predict_images(image_paths):
    X = []
    for img_path in image_paths:
        X.append(process_image(img_path))
    X = np.array(X)
    X_updated = X.reshape(len(X), -1)
    xtrain = X_updated / 255

    # Load the trained model from the file
    rf = joblib.load('random_forest_model_archive.pkl')

    # Make predictions on new data
    predictions = rf.predict(xtrain)

    # Analyze and return results
    ranked_results = results_analysis(predictions)
    return ranked_results
