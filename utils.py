import os
import pickle
import json


class SaverError(Exception):
    pass


# pickle
def save_pickle(obj, path):
    """ Pickles objectt to file under path """
    with open(str(path), 'wb+') as saveFile:
        pickle.dump(obj, saveFile)
    return True


def load_pickle(path):
    """ Loads object from file under path """
    with open(str(path), 'rb') as loadFile:
        obj = pickle.load(loadFile)
    return obj


# json
def save_json(obj, path):
    with open(f'{path}.json', 'w') as saveFile:
        json.dump(obj, saveFile)
    return True


def load_json(path):
    path = str(path)
    if not path.endswith('.json'):
        raise ValueError('load_json can only load files with json extension.')
    with open(str(path), 'r') as loadFile:
        obj = json.load(loadFile)
    return obj

# folder
def path_exists(path):
    """ Asserts path existance """
    assert os.path.exists(path), f'Folder {path} cannot be found.'


def assert_type(obj, name, t):
    ''' Asserts obj with name has type t '''
    assert isinstance(obj, t), (f'{name} expected type {name}, ',
                                f'but found type {t}.')


def delete_folder(folderPath):
    """ Recursively deletes folderPath and contents """
    if os.path.exists(folderPath):
        for file in os.listdir(folderPath):
            try:
                os.remove(f'{folderPath}/{file}')
            except PermissionError:
                delete_folder(f'{folderPath}/{file}')
        os.rmdir(folderPath)
        return True
    else:
        return False


def delete_and_make_folder(folderPath):
    """ Deletes folder if already exists and makes folder """
    delete_folder(folderPath)
    os.mkdir(folderPath)


def safe_make_folder(folderPath):
    """ Wraps delete_and_make_folder but checks with the user first """
    if os.path.exists(folderPath):
        warn_checkpoint(f'{folderPath} already exists. '
                        'Are you sure you want to delete it?')
        delete_folder(folderPath)
    os.mkdir(folderPath)


# warnings
def warn_checkpoint(message):
    commitAction = input(f'{message} (y/n): ').lower().strip()
    if (commitAction=='y'):
        return True
    elif (commitAction=='n'):
        raise RuntimeError('Action safely prevented.')
    else:
        print("Must input either 'y' or 'n'.")
        warn_checkpoint(message)
