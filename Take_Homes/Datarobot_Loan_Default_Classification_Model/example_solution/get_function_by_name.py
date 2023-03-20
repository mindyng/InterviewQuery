from importlib import import_module


def get_function_by_name(function_name, module_name=None):
    """
    Returns function (as a source) by its name and module name

    :param function_name: string
    :param module_name: string, defaults to function_name
    :return: function source
    """
    if module_name is None:
        module_name = function_name
    try:
        module = import_module(module_name)
        try:
            function = getattr(module, function_name)
            return function
        except Exception as e:
            print(e)
            raise EnvironmentError('Function "' + function_name + '" can not be imported from file.')
    except Exception as e:
        print(e)
        raise EnvironmentError('File with method "' + function_name + '.py"  does not exists or can not be imported.')

