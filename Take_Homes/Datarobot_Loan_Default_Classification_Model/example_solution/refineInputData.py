from pandas import DataFrame, concat, to_numeric
import numpy
from auxil import check_extra_values, normalize_numeric


def replace_name_property(variable_assignment,name, new_properties):
    for i in range(len(variable_assignment["description"])):
        if variable_assignment["description"][i]["name"] == name:
            variable_assignment["description"][i] = new_properties
    return variable_assignment


def refineInputData(data, variable_assignment, encoders, is_deployed=False):
    """
    Encodes raw input from CSV to appropriate representation replacing categorical values with numbers.
    If required code permutes the data in selected column before encoding

    :param data: dataframe, raw data uploaded from CSV file
    :param variable_assignment: schema of the data file
    :param encoders: encoders for categorial columns (label and one hot encoders according to scheme)
    :param is_deployed: if model already deployed we don't need target column
    :return: encoded data (X and target column y)
    """
    variable_assignment = variable_assignment.copy()

    used_columns_list = set([variable_assignment['target']]).union(variable_assignment['selectedColumns'])

    drop_columns_list = data.columns
    drop_columns_list = drop_columns_list.difference(used_columns_list)

    if len(drop_columns_list) > 0:
        data.drop(drop_columns_list, axis=1, inplace=True)

    important_columns = set(variable_assignment['selectedColumns'])
    important_columns_missing = important_columns.difference(data.columns)
    if len(important_columns_missing) > 0:
        exception_message = 'This list of the columns: ' + str(list(important_columns_missing)) +\
                            ' is not available in file.'
        raise Exception(exception_message)

    ordered_columns = variable_assignment['selectedColumns'].copy()
    if variable_assignment['target'] in data.columns and variable_assignment['target'] not in ordered_columns:
        ordered_columns.append(variable_assignment['target'])

    def sort_by_name_key(x):
        index = ordered_columns.index(x["name"])
        return index

    new_description = []
    old_description = variable_assignment["description"]
    for element in variable_assignment["description"]:
        if element["name"] in ordered_columns:
            new_description.append(element)
    variable_assignment["description"] = new_description

    ordered_description = sorted(variable_assignment["description"], key=sort_by_name_key)
    data = data.reindex(ordered_columns, axis=1)

    X = DataFrame()
    y = DataFrame()

    counting_dictionary = {}
    i = 0
    true_index_arr = None
    data_values_matrix = data.values
    for column_description in ordered_description:
        column_data = data_values_matrix[:, i]
        i += 1
        good_index = numpy.not_equal(column_data,"")
        bad_index = numpy.bitwise_not(good_index)
        if column_description["type"] == "numerical":
            if "mean" not in column_description.keys():
                column_description["mean"] = numpy.mean(
                    to_numeric(column_data[good_index], errors='coerce', downcast='float'))
            if "std" not in column_description.keys():
                column_description["std"] = numpy.std(
                    to_numeric(column_data[good_index], errors='coerce', downcast='float'))
            variable_assignment = replace_name_property(variable_assignment, column_description["name"], column_description)
            column_data[bad_index] = str(column_description["mean"])
        try:
            if column_description["type"] in ["categorical","binary"]:
                column_data_before = column_data
                column_data_before.shape = (column_data_before.size, 1)

                no_extra_flag, true_index_arr = check_extra_values(column_data_before, encoders["label"][column_description['name']])
                column_data = numpy.empty((column_data_before.size,), dtype=numpy.int64)
                column_data.fill(numpy.nan)
                column_data_before.shape =(column_data_before.size,)
                column_data[true_index_arr, ] = encoders["label"][column_description["name"]].transform(column_data_before[true_index_arr, ])
            else:
                column_data_before = column_data
                column_data = to_numeric(column_data_before,errors='coerce',downcast='float')
                column_data = numpy.asarray(column_data)
                if ("mean" in column_description.keys()) and ("std" in column_description.keys()):
                    column_data = normalize_numeric(column_data, column_description)

        except Exception as e:
            exception_message = 'Conversion of the column "' + column_description["name"] + '" of type "' +\
                                column_description["type"] + '" according to schema failed.'
            reason = str(e).replace('[','').replace(']','')
            exception_message += ' Failure reason: ' + reason
            raise Exception(exception_message)

        if ((column_description["name"] == variable_assignment["target"] and (not is_deployed)) or (column_description["type"] in ["numerical"])) and \
            (sum(numpy.isnan(column_data)) > 0 or sum(numpy.isinf(column_data)) > 0):
            exception_message = 'Conversion of the column "' + column_description["name"] + '" of type "' + \
                                column_description["type"] + '" contains nan or infinity values after conversion.'
            raise Exception(exception_message)

        if column_description["name"] == variable_assignment["target"]:
            if len(column_data.shape) < 2:
                column_data.shape = (column_data.shape[0], 1)
            y = DataFrame(column_data)
            y.columns = [column_description["name"]]
            continue

        if column_description["type"] in ["categorical","binary"]:
            try:
                column_data_extended = numpy.empty((column_data.size,len(encoders["label"][column_description['name']].classes_)))
                column_data_extended.fill(0)
                column_data_extended[true_index_arr, ] = encoders["onehot"][column_description["name"]].\
                                          transform(column_data[true_index_arr, ].reshape(sum(true_index_arr), 1))
                column_data = column_data_extended
            except Exception as e:
                exception_message = 'Conversion of the column "' + column_description["name"] + '" of type "' + \
                                    column_description["type"] + '" as categorical according to schema failed.'
                reason = str(e).replace('[','').replace(']','')
                exception_message += ' Failure reason: ' + reason
                raise Exception(exception_message)
        if len(column_data.shape) < 2:
            column_data.shape = (column_data.shape[0],1)
        if numpy.any(sum(numpy.isnan(column_data))) > 0:
            exception_message = 'Conversion of the column "' + column_description["name"] + '" of type "' + \
                                column_description["type"] + '" contains nan values after conversion.'
            raise Exception(exception_message)
        if numpy.any(sum(numpy.isinf(column_data))) > 0:
            exception_message = 'Conversion of the column "' + column_description["name"] + '" of type "' + \
                                column_description["type"] + '" contains nan values after conversion.'
            raise Exception(exception_message)
        start_position = X.shape[1]
        size_column = column_data.shape[1]
        counting_dictionary[column_description["name"]] = (start_position,size_column)
        X = concat([X, DataFrame(column_data)], axis=1)
    variable_assignment["description"] = old_description
    return [X,y,counting_dictionary,variable_assignment]
