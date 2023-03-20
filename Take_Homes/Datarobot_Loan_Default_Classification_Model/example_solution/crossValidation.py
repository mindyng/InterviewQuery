import numpy
import os
import collections
import pickle
from config import CONFIG
from data_reader import read_Nstr_from_Csv
from refineInputData import refineInputData
from get_function_by_name import get_function_by_name
from tree_importance import get_tree_importance
from save_load import save_obj
from pandas import to_numeric
from split_for_validation import correct_path, get_base_name
from decimal import Decimal
from scores_computations import get_confusion_matrix, accuracy_confusion_binary, log_loss
import warnings


def full_file_processing(full_train_file, variable_assignment,
                         encoders, algorithm_list=['logistic_regression','gradient_boosting_classifier']):
    data_from_file = read_Nstr_from_Csv(full_train_file)
    _data = data_from_file.copy()
    x, y, counting_dictionary, variable_assignment = refineInputData(_data, variable_assignment, encoders,False)
    if y.shape[0] == 0:
        raise ValueError('Target column with name: "' + variable_assignment["target"] + '" is not provided')
    importance_val_pairs = get_tree_importance(x, y.values.reshape(x.shape[0]), counting_dictionary, encoders, )

    all_saved_models = []
    for algorithm_name in algorithm_list:
        if not (algorithm_name in CONFIG["supported_algorithms"]):
            error_message = "Algorithm with name " + str(algorithm_name) + " is not supported." +\
                            "Select one from the list " + str(CONFIG["supported_algorithms"])
            raise Exception(error_message)
        train_method = get_function_by_name(function_name=algorithm_name + '_train',
                                                module_name=algorithm_name)
        model = train_method(x, y)
        model_path = '../data/full_model_' + str(algorithm_name) + '.bin'
        save_obj(algorithm_name, model_path)
        save_obj(encoders, model_path)
        save_obj(variable_assignment, model_path)
        save_obj(model, model_path)
        all_saved_models.append(model_path)
    return all_saved_models, importance_val_pairs


def crossValidation(split_parameters,
                    algorithm_list=['logistic_regression', 'gradient_boosting_classifier'],
                    threshold_step=0.01):

    working_directory = '../data/'

    if len(algorithm_list) < 1:
        raise ValueError("At least 1 algorithm should be selected for training")

    train_names_list = split_parameters["train_files"]
    valid_names_list = split_parameters["validation_files"]
    encoders_list = split_parameters["encoders"]
    description_list = split_parameters["statistics"]

    all_files = train_names_list.copy()
    all_files.extend(valid_names_list)
    for file_name in all_files:
        if not os.path.isfile(file_name):
            error_message = 'File "' + file_name + '" with input data does not exist.'
            raise ValueError(error_message)

    if threshold_step <= 0 or threshold_step >= 1:
        error_message = '"threshold_step" parameter should be a float number between 0.0' \
                        ' and 1.0. Current value is "' \
                        + str(threshold_step) + '" with input data does not exist.'
        raise ValueError(error_message)

    thresholds = numpy.arange(0, 1 + threshold_step, threshold_step)
    thresholds = numpy.concatenate((thresholds, numpy.array([0, 0.5, 1])))
    thresholds = numpy.unique(thresholds)

    for algorithm_description in algorithm_list:
        if not (algorithm_description in CONFIG["supported_algorithms"]):
            error_message = "Algorithm with name " + str(algorithm_description) + " is not supported." +\
                            "Select one from the list " + str(CONFIG["supported_algorithms"])
            raise Exception(error_message)

    all_saved_models = {}
    file_index = 0
    for train_name in train_names_list:
        base_name = get_base_name(train_name)
        data_from_file = read_Nstr_from_Csv(train_name)
        _data = data_from_file.copy()
        current_variables = description_list[file_index].copy()
        x, y, counting_dictionary,current_variables = refineInputData(_data, current_variables, encoders_list[file_index])
        description_list[file_index] = current_variables
        if y.shape[0] == 0:
            raise ValueError('Target column with name: "' + CONFIG["target_column"] + '" is not provided')
        for algorithm_description in algorithm_list:
            all_saved_models.setdefault(algorithm_description,[])
            train_method = get_function_by_name(function_name=algorithm_description + '_train',
                                                module_name=algorithm_description)
            model_path = correct_path(base_name + algorithm_description, None, True,
                                      working_directory, ".bin",False)
            model = train_method(x, y)
            all_saved_models[algorithm_description].append(model_path)
            save_list = model
            save_obj(save_list, model_path, is_first=True)
        file_index += 1
    final_validation = None

    for algorithm_description in algorithm_list:
        predict_method = get_function_by_name(function_name=algorithm_description + '_predict',
                                                module_name=algorithm_description)

        validation_results, total_count = cross_modelEvaluation(description_list,valid_names_list,
                                                   encoders_list, predict_method,
                                                   thresholds,
                                                   all_saved_models[algorithm_description],
                                                   algorithm_description)
        if final_validation is None:
            final_validation = {"thresholds": [float(Decimal("%.2f" % elem)) for elem in list(thresholds)],
                                "totalCount": total_count,
                                "algorithms": []
                                }
        final_validation["algorithms"].append(validation_results)

    for key in all_saved_models:
        for path_element in all_saved_models[key]:
            try:
                os.remove(path_element)
            except Exception as e:
                print(e)

    return final_validation


def cross_modelEvaluation(scheme_data,eval_names_list,encoders,predict_method,
                          thresholds, trained_models,
                          algorithm_name):
        main_models = []
        for train_name in trained_models:
            with open(train_name, 'rb') as model_binary:
                main_model = pickle.load(model_binary)
                main_models.append(main_model)

        for item in scheme_data[0]["description"]:
            if item["name"] == scheme_data[0]["target"]:
                if "uniqueValues" in item.keys():
                    current_unique = item["uniqueValues"]
                else:
                    error_message = "Scheme is corrupted. Cannot find unique values for target column."
                    raise Exception(error_message)
                break
        class_names = [str(element) for element in current_unique]

        classes_number = len(class_names)
        initial_confusion = []
        confusion_threshold = []

        zero_matrix = numpy.zeros((classes_number, classes_number), dtype=numpy.int32)
        for j in range(len(thresholds)):
            confusion_threshold.append(zero_matrix.copy())

        importance_accuracy = {}
        initial_correct_accuracy = 0
        importance_logloss = {}
        initial_correct_logloss = 0
        total_count = 0
        logLoss_value = 0

        for i0 in range(0,len(eval_names_list)):
            current_description = scheme_data[i0]
            current_encoders = encoders[i0]
            current_eval_name = eval_names_list[i0]

            [current_count, curr_initial_confusion, curr_confusion_threshold,
             curr_initial_correct_accuracy, curr_importance_accuracy,
             curr_initial_correct_logloss, curr_importance_logloss, curr_logLoss] =\
                one_fileEvaluation(current_description, main_models[i0],
                                   current_eval_name, current_encoders, thresholds,predict_method)
            total_count += current_count

            if i0 == 0:
                initial_confusion = curr_initial_confusion
                confusion_threshold = curr_confusion_threshold
                initial_correct_accuracy = curr_initial_correct_accuracy
                initial_correct_logloss = curr_initial_correct_logloss
                importance_accuracy = curr_importance_accuracy
                importance_logloss = curr_importance_logloss
                logLoss_value = curr_logLoss

            else:

                initial_confusion += curr_initial_confusion
                logLoss_value += curr_logLoss
                for j in range(len(thresholds)):
                    confusion_threshold[j] += curr_confusion_threshold[j]

                initial_correct_accuracy += curr_initial_correct_accuracy
                initial_correct_logloss += curr_initial_correct_logloss
                for column_name in curr_importance_accuracy:
                    importance_logloss[column_name] = importance_logloss.get(column_name,0) +\
                                                    curr_importance_logloss[column_name]
                    importance_accuracy[column_name] = importance_accuracy.get(column_name, 0) +\
                                                     curr_importance_accuracy[column_name]

        confusion_labels = []
        accuracy_label, precision_label, recall_label, f1_label = accuracy_confusion_binary(initial_confusion)

        accuracy_threshold = []
        precision_threshold = []
        recall_threshold = []
        f1_threshold = []
        for j in range(len(thresholds)):
            accuracy_th, precision_th,\
            recall_th, f1_th = accuracy_confusion_binary(confusion_threshold[j])
            accuracy_threshold.append(accuracy_th)
            precision_threshold.append(precision_th)
            recall_threshold.append(recall_th)
            f1_threshold.append(f1_th)

        accuracy_change = {}
        logloss_change = {}
        initial_accuracy = float(initial_correct_accuracy)
        initial_logloss = float(initial_correct_logloss)
        for key in importance_accuracy:
            accuracy_change[key] = initial_accuracy - float(importance_accuracy[key])
            if initial_accuracy != 0:
                accuracy_change[key] /= initial_accuracy
            logloss_change[key] = float(importance_logloss[key]) - initial_logloss
            if initial_logloss != 0:
                logloss_change[key] /= initial_logloss
            accuracy_change[key] *= 100
            logloss_change[key] *= 100
            logloss_change[key] /= total_count
        resulting_list_accuracy = list(accuracy_change.items())
        resulting_list_logloss = list(logloss_change.items())
        resulting_list_accuracy.sort(key=lambda z: -z[1])
        resulting_list_logloss.sort(key=lambda z: -z[1])
        importance_accuracy_result = {"importanceNames": [], "importanceValues": []}
        importance_logloss_result = {"importanceNames": [], "importanceValues": []}

        for j in range(len(resulting_list_accuracy)):
           importance_accuracy_result["importanceNames"].append(resulting_list_accuracy[j][0])
           importance_accuracy_result["importanceValues"].append(resulting_list_accuracy[j][1])
           importance_logloss_result["importanceNames"].append(resulting_list_logloss[j][0])
           importance_logloss_result["importanceValues"].append(resulting_list_logloss[j][1])

        out_dictionary = get_response_dictionary(algorithm_name, importance_accuracy_result, importance_logloss_result,
                                                 accuracy_threshold, accuracy_label,
                                                 precision_threshold, precision_label,
                                                 recall_threshold, recall_label, f1_threshold, f1_label,
                                                 confusion_labels, logLoss_value/total_count)
        return out_dictionary, total_count


def get_response_dictionary(algorithm_name, importance_accuracy, importance_logloss,
                            accuracy_threshold, accuracy_label, precision_threshold, precision_label,
                            recall_threshold, recall_label,
                            F1_threshold, F1_label, confusion_labels,
                            logLoss):

    response_dictionary = {
            "algorithmName": algorithm_name,
            "ACC": accuracy_label,
            "precision": precision_label,
            "recall": recall_label,
            "F1": F1_label,
            "confusionLabel": confusion_labels,
            "importanceAccruacyNames": importance_accuracy["importanceNames"],
            "importanceAccuracyValues": importance_accuracy["importanceValues"],
            "importanceLogLossNames": importance_logloss['importanceNames'],
            "importanceLogLossValues": importance_logloss["importanceValues"],
            "accuracies": accuracy_threshold,
            "precisions": precision_threshold,
            "recalls": recall_threshold,
            "F1s": F1_threshold,
            "logLoss": logLoss
    }

    return response_dictionary


def one_fileEvaluation(scheme_data,model,
                       load_file_name,encoders,thresholds,
                       predict_method):


    selected_encoder = encoders["label"][scheme_data["target"]]

    for item in scheme_data["description"]:
        if item["name"] == scheme_data["target"]:
            if "uniqueValues" in item.keys():
                current_unique = item["uniqueValues"]
            else:
                error_message = "Scheme is corrupted. Cannot find unique values for tatget column."
                raise Exception(error_message)
            break
    class_names = [str(element) for element in current_unique]
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    model_names = selected_encoder.inverse_transform(model.classes_)
    warnings.resetwarnings()
    model_names = [class_names.index(i) for i in model_names]
    classes_number = len(class_names)
    positive_index = class_names.index('1')
    zero_matrix = numpy.zeros((classes_number, classes_number), dtype=numpy.int32)

    confusion_threshold = []

    for j in range(len(thresholds)):
        confusion_threshold.append(zero_matrix.copy())

    total_count = 0

    data_from_file = read_Nstr_from_Csv(load_file_name)

    columns = data_from_file.columns
    columns = [c.strip() for c in columns]
    missing_columns = set(scheme_data["selectedColumns"])
    missing_columns = missing_columns.difference(columns)

    if len(missing_columns) > 0:
        exception_string = 'Columns: ' + str(missing_columns) + \
                           ' required for prediction are not provided in description.'
        raise ValueError(exception_string)

    if data_from_file.shape[0] < 1:
        exception_string = 'Empty file was provided for validation. Try adjusting data partition parameters.'
        raise ValueError(exception_string)

    read_data = data_from_file.shape[0]
    total_count += read_data

    x, y, counting_dictionary, _ = refineInputData(data_from_file.copy(), scheme_data, encoders)

    old_shape = y.shape
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    predicted_y_name = encoders["label"][scheme_data["target"]].inverse_transform(y)
    warnings.resetwarnings()
    y = numpy.asarray([class_names.index(i) for i in predicted_y_name], dtype=numpy.int32)
    y.shape = old_shape

    importance_accuracy = {key: 0.0 for key in scheme_data["selectedColumns"] if key != scheme_data['target']}
    initial_correct_accuracy = 0.0
    importance_logloss = {key: 0.0 for key in scheme_data["selectedColumns"] if key != scheme_data['target']}
    initial_correct_logloss = 0.0

    logLoss_value = 0.0
    importance_check_names = [None] + list(scheme_data["selectedColumns"])
    if scheme_data['target'] in importance_check_names:
        importance_check_names.remove(scheme_data['target'])
    for column_name in importance_check_names:
        if column_name is None:
            predicted_y, predicted_score = predict_method(x, classifier=model)
            predicted_score = predicted_score[:,model_names]
            warnings.filterwarnings("ignore", category=DeprecationWarning)
            predicted_y_name = encoders["label"][scheme_data["target"]].inverse_transform(predicted_y)
            warnings.resetwarnings()
            predicted_y = numpy.asarray([class_names.index(i) for i in predicted_y_name],dtype=numpy.int32)
            old_shape = predicted_y.shape
            predicted_y.shape = (predicted_y.size, 1)
            initial_correct_accuracy += numpy.sum(numpy.equal(y, predicted_y))
            logLoss_value = log_loss(predicted_score,y,positive_index)
            predicted_y.shape = old_shape
        else:
            current_description = None
            for elem in scheme_data["description"]:
               if elem["name"] == column_name:
                   current_description = elem
                   break
            start_column = counting_dictionary[column_name][0]
            end_column = counting_dictionary[column_name][1]
            end_column += start_column
            old_value = x.values[:, start_column:end_column]
            if ("mean" in current_description.keys()) and (
                       "std" in current_description.keys()):
               x.values[:, start_column] = numpy.random.normal(0.0, 1.0, size=x.shape[0])
            else:
               if "uniqueValues" in current_description.keys():
                   current_unique = current_description["uniqueValues"]
               else:
                   current_unique = []
               if len(current_unique) > 0:
                   selected_ind = numpy.asarray(
                       numpy.random.choice(len(current_unique), size=x.shape[0],
                                          replace=True), dtype=int)
                   generated = numpy.asarray(current_unique)[selected_ind]
                   if current_description["type"] == "numerical":
                       labeled_code = to_numeric(generated,errors='coerce',downcast='float')
                       labeled_code.shape = (labeled_code.size, 1)
                       x.values[:, start_column:end_column] = labeled_code
                   elif current_description["type"] in ["categorical", "binary"]:
                       labeled_code = encoders["label"][column_name].transform(generated)
                       labeled_code.shape = (labeled_code.size, 1)
                       if current_description["type"] == "categorical":
                           labeled_code = encoders["onehot"][column_name].transform(labeled_code)
                           x.values[:, start_column:end_column] = labeled_code
               else:
                   permutation_index = numpy.random.permutation(x.shape[0])
                   x.values[:, start_column:end_column] = x.values[permutation_index,
                                                          start_column:end_column]

            predicted_y_column, predicted_score_column = predict_method(x,classifier=model)
            predicted_score_column = predicted_score_column[:, model_names]
            warnings.filterwarnings("ignore", category=DeprecationWarning)
            predicted_y_name = encoders["label"][scheme_data["target"]].inverse_transform(predicted_y_column)
            warnings.resetwarnings()
            predicted_y_column = numpy.asarray([class_names.index(i) for i in predicted_y_name],dtype=numpy.int32)
            x.values[:, start_column:end_column] = old_value

            if len(predicted_y_column.shape) < 2:
               predicted_y_column.shape = (predicted_y_column.size, 1)
            importance_accuracy[column_name] += numpy.sum(numpy.equal(y, predicted_y_column))
            importance_logloss[column_name] += log_loss(predicted_score_column, y, positive_index)

    initial_confusion = zero_matrix.copy()
    initial_confusion += get_confusion_matrix(y, predicted_y, classes_number)

    for j in range(len(thresholds)):
        for l in range(len(y)):
            threshold_mask = predicted_score[l, :] >= thresholds[j]
            if numpy.count_nonzero(threshold_mask) > 1 and classes_number > 2:
                ind = numpy.min(numpy.argmax(predicted_score[l, :]))
            elif numpy.count_nonzero(threshold_mask) > 1:
                ind = 0
            elif numpy.count_nonzero(threshold_mask) == 0:
                ind = classes_number - 1
            else:
                ind = numpy.argmax(threshold_mask)
            if y[l] >= classes_number:
                continue
            confusion_threshold[j][ind, y[l]] += 1
    return [total_count, initial_confusion, confusion_threshold,
            initial_correct_accuracy, importance_accuracy,
            initial_correct_logloss, importance_logloss,
            logLoss_value]
