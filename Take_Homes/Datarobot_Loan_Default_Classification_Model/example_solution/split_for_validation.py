import os
import numpy
# MAIN FUNCTION #
def split_for_validation(data, target_name='is_bad', split_type='k-fold', k=5,train_size = 0.8):
    """
    Splits input data dictionary for validation

    :param data: input data
    :return: List of file names with the splitted data
    """

    column_name = target_name
    counts = data[target_name].value_counts()

    categoryHistogram = {}
    for key in counts.keys():
        categoryHistogram[key] = counts[key]

    min_element = min([float(x) for x in categoryHistogram.values()])
    totlaRows = sum([float(x) for x in categoryHistogram.values()])
    if split_type == "k-fold":
        if k < 0 or k > min_element:
            error_message = "Split parameter k should be positive number not greater than " + str(min_element)
            raise Exception(error_message)
        if split_type == "k-fold" and k < 2:
            error_message = "You need to select at least 2 folds for k-fold split method"
            raise Exception(error_message)
    min_count = numpy.inf
    min_value = ""
    for v in categoryHistogram:
        if float(categoryHistogram[v]) < min_count:
            min_count = float(categoryHistogram[v])
            min_value = v

    if split_type == "random":
        if float(train_size) < (2.0/totlaRows) or \
                        train_size >= ((totlaRows - 2.0)/totlaRows):
            error_message = "Selected percentage do not allow each fraction to contain at least 2 elements"
            raise Exception(error_message)

    if split_type == "random":
        nk = 2
    else:
        nk = k

    if split_type == "k-fold":
        train_size = 0.0

    if nk > min_count:
        raise Exception(
            "Target column  " + column_name + '  contains only ' + str(min_count) + ' rows of parameter ' + str(
                min_value) + ' with expected number of parts ' + str(nk))
    current_unique = list(categoryHistogram.keys())

    def init_one_dict(_nk):
        empty_dict = dict.fromkeys(current_unique, 0)
        _res = {k: empty_dict.copy() for k in range(0, _nk)}
        return _res

    all_Partition_Dict = init_one_dict(nk)

    iteration = 0
    total_count = 0
    file_names_dict = generate_names('dataset', nk, split_type, '../data/')
    read_data = data.shape[0]
    if read_data > 0:
        cd = data.loc[:, column_name]
        column_data = cd.values
        curr_partition_dict, all_Partition_Dict = split_data(column_data, categoryHistogram, all_Partition_Dict,
                                                                 split_algorithm=split_type, nk=nk,
                                                                 train_size=train_size)

        if split_type == 'k-fold':
            write_Partitions_K(data, curr_partition_dict, iteration, file_names_dict)
        else:
            write_Partitions_Two(data, curr_partition_dict, iteration, file_names_dict)
        total_count += read_data

    for ind in all_Partition_Dict:
        for key in all_Partition_Dict[ind]:
            if all_Partition_Dict[ind][key] < 1:
                raise Exception("Selected split parameters do not allow select enough data for validation")

    return file_names_dict


def get_base_name(file_name):
    """
    Helper function to get base name of all the files created

    :param file_name: original file name
    :return: new file name
    """
    path, name = os.path.split(file_name)

    base_list = name.split(".")
    if len(base_list) > 1:
        base_name = "".join(base_list[:-1])
    else:
        base_name = name
    return base_name


def generate_names(csv_file_name, n, splitparam, working_directory, ext='.csv'):
    """
    Generates list of names by the source file

    :param csv_file_name: Original CSV file name
    :param n: number of parts to split
    :param splitparam: One of ['random', 'k_fold']
    :param working_directory: Directory to save newly created files
    :param ext: Extension of newly created files
    :return: List of file names
    """
    rezult_dict = dict()
    path, name = os.path.split(csv_file_name)

    base_list = name.split(".")
    if len(base_list) > 1:
        base_name = "".join(base_list[:-1])
    else:
        base_name = name

    if splitparam in ['sequential', 'random']:
        train_list = [correct_path(base_name, None, True, working_directory)]
        validation_list = [correct_path(base_name, None, False, working_directory)]
    else:
        train_list = list()
        validation_list = list()
        for i in range(1, n+1):
            train_path = correct_path(base_name, i, True, working_directory)
            train_list.append(train_path)
            validation_path = correct_path(base_name, i, False, working_directory)
            validation_list.append(validation_path)

    rezult_dict["train_files"] = train_list
    rezult_dict["validation_files"] = validation_list
    return rezult_dict


# UNIVERSAL #
def correct_path(base_name, i, tv, working_directory,ext=".csv",apply_remove=True):
    """
    Forms correct file path from the given pieces

    :param base_name: Base file name
    :param i: Number of file
    :param tv: Flag that determines the prefix
    :param working_directory: directory to save file
    :param ext: File extension
    :return: string, correct path to a new file
    """
    if tv:
        out_name = base_name + '_train_file'
    else:
        out_name = base_name + '_validation_file'

    if not (i is None):
        out_name += str(i)

    default_path = working_directory
    if not os.path.isdir(default_path):
        os.mkdir(default_path)
    out_path_ini = os.path.join(default_path, out_name)

    out_path = out_path_ini
    iteration = 1
    while os.path.isfile(out_path + ext):
        if apply_remove:
            try:
                os.remove(out_path+ext)
                if os.path.isfile(out_path):
                    raise FileExistsError
            except:
                out_path = out_path_ini + '('+str(iteration)+')'
                iteration += 1
        else:
            out_path = out_path_ini + '(' + str(iteration) + ')'
            iteration += 1

    out_path += ext
    return out_path


def split_data(column_data, category_histogram, all_Partition_Dict, split_algorithm="random", nk=2, train_size=0.7):
    """
    Splits data into several files

    :param column_data: vector with column data
    :param category_histogram: category histogram
    :param all_Partition_Dict: dictionary with the all partitions specified
    :param split_algorithm: string, name of a split algorithm
    :param nk: number of pieces
    :param train_size: the part of data used for train
    :return: available_indices, all_Partition_Dict
    """
    category_left = category_histogram.copy()
    available_indices = {}
    for ind in all_Partition_Dict:
        available_indices[ind] = list()
        for key in category_histogram:
            category_left[key] = float(category_left[key])
            category_left[key] -= all_Partition_Dict[ind][key]

    expected_elements = {i: {} for i in range(nk)}

    for key in category_histogram:
        curentAmount = float(category_histogram[key])
        if split_algorithm == "random":
            expected_elements[0][key] = max(float(category_histogram[key]) * train_size, 1)
            expected_elements[1][key] = float(category_histogram[key]) - expected_elements[0][key]
            if expected_elements[0][key] < 1 or expected_elements[1][key] < 1:
                raise Exception("Selected split parameters does not allow select enough data for validation")
            expected_elements[0][key] -= all_Partition_Dict[0][key]
            expected_elements[1][key] -= all_Partition_Dict[1][key]
        else:
            currentAmount_old = curentAmount
            while curentAmount > 0:
                for ind in range(0, len(all_Partition_Dict)):
                    expected_elements[ind].setdefault(key,0)
                    selected_value = min(curentAmount, max(numpy.floor(float(category_histogram[key])/(1.0*nk)), 1))
                    expected_elements[ind][key] += selected_value
                    if expected_elements[ind][key] == 0:
                        raise Exception("Selected split parameters does not allow select enough data for validation")
                    curentAmount -= selected_value
                if currentAmount_old == curentAmount:
                    if curentAmount > 0:
                        expected_elements[len(all_Partition_Dict)-1][key] += curentAmount
                        curentAmount = 0
                currentAmount_old = curentAmount
            for ind in range(0, len(all_Partition_Dict)):
                expected_elements[ind][key] -= all_Partition_Dict[ind][key]
    for key in category_histogram:
        valindexes = numpy.where(column_data.ravel() == key)[0]
        index_count = valindexes.size
        while index_count > 0:
            index_count_left = index_count
            for ind in expected_elements:
                    selected_count = int(numpy.floor(index_count*(expected_elements[ind][key] / category_left[key])))
                    index_count_left -= selected_count
                    expected_elements[ind][key] -= selected_count
                    if split_algorithm == "random":
                        choice = numpy.random.choice(valindexes, size=selected_count, replace=False)
                        valindexes = numpy.asarray(list(set(valindexes).difference(choice)), dtype=numpy.int32)
                    else:
                        choice = valindexes[0:selected_count]
                        if selected_count < len(valindexes):
                            valindexes = valindexes[selected_count:valindexes.size]
                        else:
                            valindexes = numpy.asarray([],dtype=numpy.int32)

                    available_indices[ind].extend(list(choice))
                    all_Partition_Dict[ind][key] += selected_count
                    if index_count_left < 1:
                        break
            category_left[key] -= (index_count-index_count_left)
            if index_count == index_count_left:
                break
            index_count = index_count_left
        while index_count > 0:
            order = (numpy.argsort([expected_elements[ind][key] / category_left[key] for ind in expected_elements])).tolist()
            for ind in order:
                if expected_elements[ind][key] > 0:
                    available_indices[ind].extend([valindexes[0]])
                    if len(valindexes) > 1:
                        valindexes = valindexes[1:valindexes.size]
                    else:
                        valindexes = numpy.asarray([], dtype=numpy.int32)
                    all_Partition_Dict[ind][key] += 1
                    expected_elements[ind][key] -= 1
                    index_count_left -= 1
                if index_count_left < 1:
                    break
            if index_count == index_count_left:
                #print("Something wrong with statistics")
                break
            index_count = index_count_left
    return available_indices, all_Partition_Dict


def write_Partitions_Two(data, partition_dict, iteration, file_names_dict):
    """
    Write two partitions to files

    :param data: Input data frame
    :param partition_dict: Dictionary of partitions calculated
    :param iteration: Number of iteration
    :param file_names_dict: Dictionary of file names
    :return: None
    """
    train_file_name = file_names_dict["train_files"][0]
    valid_file_name = file_names_dict["validation_files"][0]

    for ind in partition_dict:
        if len(partition_dict[ind]) < 1:
            continue

        data_write = data.iloc[partition_dict[ind]]
        if ind == 0:
            write_To_Csv(data_write, train_file_name, iteration)
        else:
            write_To_Csv(data_write, valid_file_name, iteration)
    return


def write_Partitions_K(data, partition_dict, iteration, file_names_dict):
    """
    Write K = len(file_names_dict["train_files"]) partitions to files

    :param data: Input data frame
    :param partition_dict: Dictionary of partitions calculated
    :param iteration: Number of iteration
    :param file_names_dict: Dictionary of file names
    :return: None
    """
    train_names_list = file_names_dict["train_files"]
    eval_names_list = file_names_dict["validation_files"]
    iteration_local = {}
    for ind in partition_dict:
        if len(partition_dict[ind]) < 1:
            continue
        data_write = data.iloc[partition_dict[ind]]
        for k in range(len(train_names_list)):
            if not (k in iteration_local.keys()):
                iteration_local[k] = iteration
            if k == ind:
                write_To_Csv(data_write, eval_names_list[k], iteration)
            else:
                write_To_Csv(data_write, train_names_list[k], iteration_local[k])
                iteration_local[k] += 1
    return


# UNIVERSAL #
def write_To_Csv(data,file_name,iteration):
    """Writes data to csv files

    :param data: Input data frame
    :param file_name: file name to write in
    :param iteration: number of iteration

    :return: None

    """

    if iteration == 0:
        with open(file_name, mode='w', encoding='utf-8') as f:
            data.to_csv(f, header=True, sep=',', index=False, encoding='utf-8')
    else:
        with open(file_name, mode='a', encoding='utf-8') as f:
            data.to_csv(f, header=False, sep=',', mode='a', index=False, encoding='utf-8')
