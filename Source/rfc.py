from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
import pandas as pd
import numpy as np
import os
import pathlib

datasets_path = os.path.join('.', 'CMANGOES-2.0', 'Data', 'Encodings')
datasets_folder = pathlib.Path(datasets_path)
datasets_list = list(datasets_folder.iterdir())
datasets_list = [os.path.basename(dataset) for dataset in datasets_list]

n_runs = 100

mean_accuracy_df = pd.DataFrame(np.nan, index=datasets_list, columns=range(n_runs))
f1_score_df = pd.DataFrame(np.nan, index=datasets_list, columns=range(n_runs))

for level in [1, 2]:
    for alphabet_mode in ['without_hydrogen', 'with_hydrogen', 'data_driven']:
        for data_idx in range(len(datasets_list)):
            dataset = datasets_list[data_idx]
            print('Running dataset', data_idx + 1, '/', len(datasets_list))

            encoding_data_path = os.path.join('.', 'CMANGOES-2.0', 'Data', 'Encodings', dataset,
                                              'CENACT_level_' + str(level) + '_' + alphabet_mode + '.csv')
            classes_path = os.path.join('.', 'CMANGOES-2.0', 'Data', 'Original_datasets',
                                        dataset, 'classes.txt')

            X = pd.read_csv(encoding_data_path)
            y = pd.read_csv(classes_path, header=None)
            y = y.astype('category')
            y = y.to_numpy().ravel()

            for n in range(n_runs):
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, train_size=0.8,
                                                                    random_state=n, shuffle=True, stratify=None)
                rfc = RandomForestClassifier(n_jobs=-1)
                rfc.fit(X_train, y_train)
                mean_accuracy = rfc.score(X_test, y_test)
                y_pred = rfc.predict(X_test)
                f1 = f1_score(y_test, y_pred)

                mean_accuracy_df.iat[data_idx, n] = mean_accuracy
                f1_score_df.iat[data_idx, n] = f1

        results_path = os.path.join('.', 'CMANGOES-2.0', 'Results')
        if os.path.exists(results_path) == False:
            os.mkdir(results_path)

        mean_accuracy_path = os.path.join(results_path,
                                          'mean_accuracy_level_' + str(level) + '_' + alphabet_mode + '.csv')
        f1_score_path = os.path.join(results_path, 'f1_score_level_' + str(level) + '_' + alphabet_mode + '.csv')

        mean_accuracy_df.to_csv(mean_accuracy_path, index=True, header=True)
        f1_score_df.to_csv(f1_score_path, index=True, header=True)
