from data_reader import read_Nstr_from_Csv
from split_for_validation import split_for_validation
from config import CONFIG
import numpy as np
from preliminary_statistics import filter_text_and_categorical_values
from encoders_generation import generate_settings, get_categorical_encoders
from crossValidation import crossValidation, full_file_processing
from auxil import clean_files
import sys
   
def check_stratification(data,k_fold_files,hold_out_files):
    print('Ratio is_bad "1" to "0" in original file:')
    original_count = data['is_bad'].value_counts()
    print('\t0: {0:d}'.format(original_count['0']))
    print('\t1: {0:d}'.format(original_count['1']))
    print('\tratio: {0:.3f}'.format(original_count['0'] * 1.0 / original_count['1']))
    print('Ratio is_bad "1" to "0" in holdout train file:')
    data_train = read_Nstr_from_Csv(hold_out_files['train_files'][0])
    train_count = data_train['is_bad'].value_counts()
    print('\t0: {0:d}'.format(train_count['0']))
    print('\t1: {0:d}'.format(train_count['1']))
    print('\tratio: {0:.3f}'.format(train_count['0'] * 1.0 / train_count['1']))
    print('Ratio is_bad "1" to "0" in  holdout validation file:')
    data_validation = read_Nstr_from_Csv(hold_out_files['validation_files'][0])
    validation_count = data_validation['is_bad'].value_counts()
    print('\t0: {0:d}'.format(validation_count['0']))
    print('\t1: {0:d}'.format(validation_count['1']))
    print('\tratio: {0:.3f}'.format(validation_count['0'] * 1.0 / validation_count['1']))

    print('Ratio is_bad "1" to "0" in  k-fold files:')
    for name in (k_fold_files['train_files'] + k_fold_files['validation_files']):
        data_current = read_Nstr_from_Csv(name)
        current_count = data_current['is_bad'].value_counts()
        print('\tname: {0:s}'.format(name))
        print('\t0: {0:d}'.format(current_count['0']))
        print('\t1: {0:d}'.format(current_count['1']))
        print('\tratio: {0:.3f}'.format(current_count['0'] * 1.0 / current_count['1']))

import matplotlib
matplotlib.use('agg')
from matplotlib import pyplot as plt


def display_importances(importances, vertical=False, show=False,
                    save_path='../data/importance_tree.png', save_inches=[15,10]):


    #print("Feature ranking:")

    lable_list = []
    value_list = []
    for f in range(len(importances)):
        #print("%d. feature %s (%f)" % (f + 1,importances[f][0], importances[f][1]))
        lable_list.append(importances[f][0])
        value_list.append(importances[f][1])

    if vertical:
        # Plot the feature importances of the forest
        plt.figure()
        plt.title("Feature importances")
        plt.bar(range(len(importances)), value_list,
                color="r", align="center")

        plt.xticks(range(len(importances)), lable_list)
        plt.xticks(rotation=90,labelsize=16)
        plt.xlim([-1, len(importances)])

    else:
        _, ax = plt.subplots()

        y_pos = range(len(importances))
        ax.barh(y_pos, value_list,
                color="r", align="center")

        ax.set_yticks(y_pos)
        ax.set_yticklabels(lable_list)
        ax.invert_yaxis()  # top-to-bottom
        ax.set_xlabel('Importance')
        ax.set_title("Feature importances")

    if show:
        plt.show()
    if save_path:
        figure = plt.gcf() # get current figure
        figure.set_size_inches(*save_inches)
        plt.savefig(save_path)

        #print('The plot was saved to: {}'.format(save_path))


if __name__ == '__main__':
    if not sys.warnoptions:
        import warnings
        warnings.simplefilter("ignore")
        
    # input dataset file
    data_path = '../data/dataset.csv'
    data_dict_path = '../data/data_dictionary.csv'

    # where to save preliminary version after columns removal and
    preprocessed_data_path = '../data/preprocessed_dataset.csv'
    filter_text_and_categorical_values(data_path, preprocessed_data_path)
    data = read_Nstr_from_Csv(preprocessed_data_path)
    k_fold_files = split_for_validation(data, CONFIG['target_column'], 'k-fold',
                                        CONFIG['k_fold_k'], CONFIG['hold_out_train_size'])
    hold_out_files = split_for_validation(data, CONFIG['target_column'], 'random',
                                         CONFIG['k_fold_k'], CONFIG['hold_out_train_size'])

    k_fold_files["statistics"] = []
    k_fold_files["encoders"] = []
    for path in k_fold_files['train_files']:
        current_statistics = generate_settings(data_dict_path, path)
        #current_statistics["selectedColumns"] = ['addr_state','is_bad','zip_code']
        k_fold_files["statistics"].append(current_statistics)
        k_fold_files["encoders"].append(get_categorical_encoders(k_fold_files["statistics"][-1]))

    hold_out_files["statistics"] = []
    hold_out_files["encoders"] = []
    for path in hold_out_files['train_files']:
        current_statistics = generate_settings(data_dict_path, path)
        #current_statistics["selectedColumns"] = ['addr_state','is_bad','zip_code']
        hold_out_files["statistics"].append(current_statistics)
        hold_out_files["encoders"].append(get_categorical_encoders(hold_out_files["statistics"][-1]))

    full_variable_statisitics = generate_settings(data_dict_path, preprocessed_data_path)
    full_encoders = get_categorical_encoders(full_variable_statisitics)

    saved_model_path, variable_importance = full_file_processing(preprocessed_data_path,
                                                                 full_variable_statisitics, full_encoders)
    display_importances(variable_importance, show=False)

    subsets_result = {}
    all_columns = current_statistics["selectedColumns"]
    all_columns.remove('is_bad')

    selected_element = {}
    best_logloss = {}
    best_result_holdout = {}
    best_result_kfold = {}
    iterations = 0
    while len(selected_element) < min(3,len(all_columns)) and iterations < 3:
        current_best = {}
        current_best_logloss = {}
        current_best_results = {}
        for column_name in all_columns:
            if column_name == CONFIG['target_column']:
                continue
            for algorithm_name in CONFIG['supported_algorithms']:
                if column_name in selected_element.get(algorithm_name,[]):
                    continue
                print("Algorithm: " + algorithm_name)
                current_selection = selected_element.get(algorithm_name,[]) + [column_name]
                print("Testing combination: " + str(current_selection))
                for i in range(len(hold_out_files['statistics'])):
                    hold_out_files["statistics"][i]["selectedColumns"] = current_selection
                current_result = crossValidation(hold_out_files,algorithm_list=[algorithm_name])
                current_algorithm = current_result["algorithms"][0]
                print("LogLoss: " + str(current_algorithm['logLoss']))
                if current_best_logloss.get(algorithm_name, best_logloss.get(algorithm_name,
                                                                     np.inf)) > current_algorithm['logLoss']:
                    current_best_logloss[algorithm_name] = current_algorithm['logLoss']
                    current_best[algorithm_name] = current_selection
                    current_best_results[algorithm_name] = current_result
        for algorithm_name in CONFIG['supported_algorithms']:
            if best_logloss.get(algorithm_name,np.inf) > current_best_logloss.get(algorithm_name,
                                                                       best_logloss.get(algorithm_name, np.inf)):
                best_logloss[algorithm_name] = current_best_logloss[algorithm_name]
                selected_element[algorithm_name] = current_best[algorithm_name]
                best_result_holdout[algorithm_name] = current_best_results[algorithm_name]
        print('Iteration result: ' + str(selected_element))
        iterations += 1

    for algorithm_name in CONFIG['supported_algorithms']:
        for i in range(len(k_fold_files['statistics'])):
            k_fold_files["statistics"][i]["selectedColumns"] = selected_element[algorithm_name]
        best_result_kfold[algorithm_name] = crossValidation(k_fold_files, algorithm_list=[algorithm_name])
    print(best_result_holdout)
    print(best_result_kfold)
    
    best_result_kfold_tree = {}
    best_result_holdout_tree = {}
    selected_element_tree =['addr_state','policy_code', 'purpose_cat']
    for algorithm_name in CONFIG['supported_algorithms']:
        for i in range(len(k_fold_files['statistics'])):
            k_fold_files["statistics"][i]["selectedColumns"] =selected_element_tree
        best_result_kfold_tree[algorithm_name] = crossValidation(k_fold_files, algorithm_list=[algorithm_name])
        best_result_holdout_tree[algorithm_name] = crossValidation(hold_out_files,algorithm_list=[algorithm_name])
    print(best_result_kfold_tree)
    print(best_result_holdout_tree)
    clean_files(k_fold_files)
    clean_files(hold_out_files)