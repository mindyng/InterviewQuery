import pickle, os


def save_obj(obj, name, is_first=False):
    """
    Saves pickle dump of object *obj* to file with name *name*

    :param obj: object
    :param name: str, filename
    :param is_first: Is this object first in the file?
    :return: None
    """
    if is_first and os.path.isfile(name):
        try:
            os.remove(name)
        except:
            with open(name, mode="w", encoding="utf-8") as del_file:
                pass
    with open(name, 'a+b') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def save_objects(objects, name):
    """
    Saves pickle dump of objects *objects* to file with name *name*

    :param objects: objects to save in file
    :param name: str, filename
    :return: None
    """
    with open(name, 'a+b') as f:
        for obj in objects:
            pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    """
    Loads pickle object from the specified file

    :param name: str, filename
    :return: object
    """
    with open(name, 'rb') as f:
        return pickle.load(f)


def load_objects(name):
    """
    Loads pickle objects (so much as written) from the specified file

    :param name: str, filename
    :return: objects
    """
    objects = []
    with open(name, 'rb') as f:
        while True:
            try:
                objects.append(pickle.load(f))
            except EOFError:
                return objects
