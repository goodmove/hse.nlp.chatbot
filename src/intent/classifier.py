import pickle
from sklearn.neighbors import KNeighborsClassifier

from src.language_model import preprocess_input


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