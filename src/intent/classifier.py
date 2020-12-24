import pickle
from sklearn.neighbors import KNeighborsClassifier

from src.language_model import preprocess_input
import numpy as np


class IntentClassifier:

    def __init__(self, path_to_model):
        self.model = get_model(path_to_model)


    def classify(self, text):
        emb = preprocess_input(text)
        predictions = self.model.predict_proba([emb])[0]
        print(predictions)
        max_index = np.argmax(predictions)
        print(max_index)

        if predictions[max_index] < 0.6:
            return None
        else:
            return max_index


def get_model(path_to_model):
    model = None
    with open(path_to_model, 'rb') as model_fd:
        model = pickle.load(model_fd)

    return model

def classify(path_to_model):
    model = get_model(path_to_model)
    print('ready')

    while True:
        text = input()
        emb = preprocess_input(text)
        print(model.predict_proba([emb]))

if __name__ == "__main__":
    classify('data/models/knn')