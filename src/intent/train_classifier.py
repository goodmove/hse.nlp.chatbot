import pickle
import yaml
import csv
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import recall_score, precision_score, accuracy_score


from src.language_model import preprocess_input

def train_knn(path_to_dataset, path_to_model):
    dataset = pd.read_csv(path_to_dataset)

    X = dataset.drop(['intent_code', 'intent_name'], axis=1)
    y = dataset['intent_code']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, stratify=y)

    def fit(X, y, n):
        model = KNeighborsClassifier(n_neighbors=n)
        model.fit(X, y)
        return model

    best_score = 0
    n_neighbors_best = None

    for n_neighbors in range(3,10,2):
        model = fit(X_train, y_train, n_neighbors)

        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred, average='weighted')
        precision = precision_score(y_test, y_pred, average='weighted')

        print(f"N: {n_neighbors}, accuracy: {accuracy}, precision: {precision}, recall: {recall}")

        if accuracy > best_score:
            best_score = accuracy
            n_neighbors_best = n_neighbors


    print(f"Best score: {best_score}; Best neighbors: {n_neighbors_best}")
    model = fit(X_train, y_train, n_neighbors_best)

    with open(path_to_model, 'wb+') as model_output:
        pickle.dump(model, model_output)


def prepare_dataset(path_to_intent_config, path_to_dataset):
    dataset_list = []

    with open(path_to_intent_config, 'r') as intent_config_fd:
        intents_config = yaml.safe_load(intent_config_fd)

        for intent in intents_config['intents']:
            intent_code = intent['code']
            intent_name = intent['name']
            intent_dataset_file = intent['dataset_file']

            with open(intent_dataset_file, 'r') as intent_dataset_fd:
                lines = intent_dataset_fd.readlines()
                
                for line in lines:
                    line = preprocess_input(line)
                    row = {'intent_code': intent_code, 'intent_name': intent_name}

                    for i in range(len(line)):
                        row[f'd_{i}'] = line[i]

                    dataset_list.append(row)
    

    with open(path_to_dataset, 'w+') as csv_output:
        fieldnames = dataset_list[0].keys()
        writer = csv.DictWriter(csv_output, fieldnames=fieldnames)
        writer.writeheader()
    
        for r in dataset_list:
            writer.writerow(r)

if __name__ == "__main__":
    prepare_dataset('data/intents.yaml', 'data/datasets/intents.csv')
    train_knn('data/datasets/intents.csv', 'data/models/knn')
    print('done')
