import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.ensemble import RandomForestClassifier

# >>----

def average_confusion_matrices(confusion_matrices):
    avg_confusion_matrix = np.zeros_like(confusion_matrices[0])
    for conf_matrix in confusion_matrices:
        avg_confusion_matrix += conf_matrix
    avg_confusion_matrix = avg_confusion_matrix/len(confusion_matrices)
    return avg_confusion_matrix

def avg(float_list):
    return sum(float_list)/len(float_list)

# >>----
def initialize_model():
    # 1. Import a CSV file
    df = pd.read_csv("dermatology_database_1.csv")
    
    # 2. Split the imported file to X and Y where X include the attributes and Y is the result.
    X = df.iloc[:, :-1].values
    Y = df.iloc[:, -1].values
    
    # >>----
    confusion_matrices = []
    acc_avg = []
    # >>----
    
    # 3. Perform cross-validation split into both sets.
    kf = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
    for train_index, test_index in kf.split(X,Y):
        X_train, X_test = X[train_index], X[test_index]
        Y_train, Y_test = Y[train_index], Y[test_index]
        
        # 4. Implement DT and give a prediction.lll
        model = RandomForestClassifier()
        model.fit(X_train, Y_train)
        Y_pred = model.predict(X_test)
    
        # >>----
        acc = accuracy_score(Y_test, Y_pred)
        acc_avg.append(acc)
        # ----<<
        
        # 5. Perform a confusion matrix on the prediction and actual result
        cm = confusion_matrix(Y_test, Y_pred)
        # >>----
        confusion_matrices.append(cm)
        # ----<<
    
    avg_confusion_matrix = average_confusion_matrices(confusion_matrices)
    print(avg_confusion_matrix)
    print("Confusion Matrix: \n", avg_confusion_matrix)
    print("Average Accuracy:", avg(acc_avg))
    
    '''
    # 6. Plot the result
    classes=np.unique(Y)
    plt.imshow(avg_confusion_matrix, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title("Confusion Matrix")
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)
    
    thresh = avg_confusion_matrix.max() / 2.
    for i, j in np.ndindex(avg_confusion_matrix.shape):
        plt.text(j, i, avg_confusion_matrix[i, j],
                 horizontalalignment="center",
                 color="white" if avg_confusion_matrix[i, j] > thresh else "black")
    
    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.show()
    '''
    return model

def get_siverence(Dict):
    
    model = initialize_model()
    # Take in disctionary and convert values to list
    List = []
    
    for keys in Dict:
        List.append(Dict[keys])
    
    # Convert the list to a NumPy array
    List = np.array(List)
    
    # Reshape the NumPy array to have a shape of (1, -1)
    List = List.reshape(1, -1)
    
    pred = model.predict(List)
    
    return pred
