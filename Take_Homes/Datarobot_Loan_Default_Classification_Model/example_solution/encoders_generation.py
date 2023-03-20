import numpy
from sklearn import preprocessing
from config import CONFIG
from data_reader import read_Nstr_from_Csv


def generate_settings(data_dict_path, train_path):
    preprocessed_data = read_Nstr_from_Csv(train_path)
    selected_columns = []
    variable_assignment = {"target": CONFIG['target_column'],"description":[]}
    data_dict = read_Nstr_from_Csv(data_dict_path)
    processed = []
    for i in range(data_dict.shape[0]):
        current_variable = data_dict.at[i,'Column Name']
        if current_variable not in CONFIG['remove_columns']:
            current_variable = current_variable.lower().strip().replace('-','_')
            counts = preprocessed_data[current_variable].value_counts()
            unique_values = list(counts.keys())
            if '' in unique_values:
                unique_values.remove('')
            if len(unique_values) >= 2:
                selected_columns.append(current_variable)
            if data_dict.at[i, 'Type'] == 'Categorical' or data_dict.at[i,'Column Name'] in ['emp_title','is_bad']:
                if current_variable == variable_assignment["target"]:
                    type_current = "binary"
                else:
                    type_current = "categorical"
                variable_assignment["description"].append({"name":current_variable,"type":type_current,"uniqueValues":unique_values})
            else:
                variable_assignment["description"].append(
                    {"name": current_variable, "type": "numerical", "uniqueValues": unique_values})
            processed.append(current_variable)
    all_columns = set(preprocessed_data.columns)
    remaining = all_columns.difference(processed)
    for key in remaining:
        counts = preprocessed_data[key].value_counts()
        unique_values = list(counts.keys())
        if '' in unique_values:
            unique_values.remove('')
        if len(unique_values) >= 2:
            selected_columns.append(key)
        variable_assignment["description"].append(
            {"name": key, "type": "binary", "uniqueValues": ['0','1']})
    variable_assignment["selectedColumns"] = selected_columns
    return variable_assignment

def get_categorical_encoders(variable_assignment):
    """
    Returns categorical encoders according to data type prediction.
    Input file with data is not verified on this stage

    :param variable_assignment: dictionary with the json schema loaded from the corresponding files

    :return: dictionary with 2 lists of encoders: label encoder for both “binary” and category type followed by one
             hot encoder for “category” type
    """
    encoders = {}
    encodersLabel = {}
    encodersOneHot = {}
    for current_element in variable_assignment['description']:
        if "name" not in current_element.keys():
            continue
        if current_element['type'] in ["categorical","binary"]:
            column_name = current_element['name']
            encodersLabel[column_name] = preprocessing.LabelEncoder()
            if "uniqueValues" in current_element.keys():
                current_unique = current_element["uniqueValues"]
            else:
                error_message = "Scheme is corrupted. Cannot find unique values for column " + current_element["name"]
                raise Exception(error_message)
            sample = numpy.asarray(current_unique)
            if column_name != variable_assignment['target'] and current_element['type'] != "binary":
                missing_value = get_missing_value_name(sample)
                sample = numpy.append(sample, missing_value)
            encodersLabel[column_name].fit(sample)
            sample = encodersLabel[column_name].transform(sample)
            encodersOneHot[column_name] = preprocessing.OneHotEncoder(sparse=False)
            encodersOneHot[column_name].fit(sample.reshape(sample.size, 1))
    encoders["label"] = encodersLabel
    encoders["onehot"] = encodersOneHot
    return encoders


def get_missing_value_name(sample):
    """
    Returns missing value name
    :param sample: data sample

    :return: missing value name string
    """
    missing_value_default = "nan"
    iteration = 0
    missing_value = missing_value_default
    while missing_value in sample:
        missing_value = missing_value_default + "_" + str(iteration)
        iteration += 1
    return missing_value



if __name__ == '__main__':
    path_dict = '../data/data_dictionary.csv'
    data_path = '../data/preprocessed_dataset.csv'
    #print(data.columns)
    variable_assignment = generate_settings(path_dict,data_path)
    encoders = get_categorical_encoders(variable_assignment)