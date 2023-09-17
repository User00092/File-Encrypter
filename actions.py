import utils
import color
import sys
import os

config = utils.Config("config.json")
gradient = color.create_gradient((65, 105, 225), (65, 105, 225))
info_gradient = color.create_gradient((191, 0, 255), (191, 0, 255))

directory_gradient = color.create_gradient((0, 128, 0), (0, 128, 0))
file_gradient = color.create_gradient((0, 0, 255), (0, 0, 255))


def key_cryption_key() -> bytes | None:
    try:
        key_input: str = utils.get_hidden_input("Enter your key: ")
        key_len: int = len(key_input)
        if key_len < 1 or key_len > 32:
            return {
                "status": False,
                "message": "Invalid key length! Must be no more than 32 characters."
            }

        key_input = utils.base64.urlsafe_b64encode((key_input + ("w" * (32 - key_len))).encode('utf-8'))

        utils.Fernet(key_input)
    
        return key_input
    except Exception:
        return None


def encrypt_paths(paths: tuple) -> dict:
    try:
        if isinstance(paths, str):
            return {
                "status": False,
                "message": "Config is corrupt."
            }
        
        key_input: dict = key_cryption_key()
        if not key_input:
            return {
                "status": False,
                "message": "Key cannot be used."
            }
        
        print(color.get_text_with_gradient("Please be patient... Process may seem frozen.", info_gradient))

        file_paths = list()
        for path in paths:
            filep = os.path.abspath(path)
            if os.path.isdir(path):
                for file in utils.list_files(filep):
                    filep = os.path.abspath(file)
                    file_paths.append(filep)
            else:
                file_paths.append(filep)
        
        file_path_count = len(file_paths)
        processed_paths = 0

        for file in file_paths:
            result = utils.encrypt_file(file, key_input)
            if result:
                processed_paths += 1

        
            sys.stdout.write(color.get_text_with_gradient(f'Encrypting files... {round(color.divide(processed_paths, file_path_count) * 100, 2)}% ({processed_paths} of {file_path_count})', gradient))
            sys.stdout.write('\r')
            sys.stdout.flush()
        print()
        return {
            "status": True,
            "message": "Successfully encrypted files."
        }
    except Exception:
        print()
        return {
            "status": False,
            "message": "An unexpected error occurred."
        }


def decrypt_paths(paths: tuple) -> dict:
    try:
        if isinstance(paths, str):
            return {
                "status": False,
                "message": "Config is corrupt."
            }
        
        key_input: dict = key_cryption_key()
        if not key_input:
            return {
                "status": False,
                "message": "Key cannot be used."
            }
        
        print(color.get_text_with_gradient("Please be patient... Process may seem frozen.", info_gradient))

        file_paths = list()
        for path in paths:
            filep = os.path.abspath(path)
            if os.path.isdir(path):
                for file in utils.list_files(filep):
                    filep = os.path.abspath(file)
                    file_paths.append(filep)
            else:
                file_paths.append(filep)
        
        file_path_count = len(file_paths)
        processed_paths = 0

        for file in file_paths:
            result = utils.decrypt_file(file, key_input)
            if result:
                processed_paths += 1

            sys.stdout.write(color.get_text_with_gradient(f'Decrypting files... {round(color.divide(processed_paths, file_path_count) * 100, 2)}% ({processed_paths} of {file_path_count})', gradient))
            sys.stdout.write('\r')
            sys.stdout.flush()
        
        print()
        return {
            "status": True,
            "message": "Successfully decrypted files."
        }
    except Exception:
        print()
        return {
            "status": False,
            "message": "An unexpected error occurred."
        }


def add_file_to_config() -> dict:
    file_path = utils.select_file()
    if not file_path:
        return {
            "status": False,
            "message": "No file selected."
        }
    
    if file_path.endswith(utils.encrypted_file_extension):
        return {
            "status": False,
            "message": "This file is already encrypted."
        }
    
    config_data: dict = config.read()

    if config_data.get("paths") is None:
        config_data["paths"] = list()
    
    if file_path in config_data["paths"]:
        return {
            "status": False,
            "message": "File already exists in config."
        }
    
    config_data["paths"].append(file_path)
    config.write(config_data)

    return {
        "status": True,
        "message": "Successfully added file to config."
    }


def remove_file_from_config() -> dict:
    file_path = utils.select_file()
    if not file_path:
        return {
            "status": False,
            "message": "No file selected."
        }

    config_data: dict = config.read()

    if config_data.get("paths") is None:
        config_data["paths"] = list()
    
    if file_path not in config_data["paths"]:
        return {
            "status": False,
            "message": "File does not exists in config."
        }
    
    config_data["paths"].remove(file_path)
    config.write(config_data)

    return {
        "status": True,
        "message": "Successfully removed file from config."
    }


def add_folder_to_config() -> dict:
    directory_path = utils.select_directory()
    if not directory_path:
        return {
            "status": False,
            "message": "No directory selected."
        }
    
    config_data: dict = config.read()

    if config_data.get("paths") is None:
        config_data["paths"] = list()
    
    if directory_path in config_data["paths"]:
        return {
            "status": False,
            "message": "Directory already exists in config."
        }
    
    config_data["paths"].append(directory_path)
    config.write(config_data)

    return {
        "status": True,
        "message": "Successfully added directory to config."
    }


def remove_folder_from_config() -> dict:
    directory_path = utils.select_directory()
    if not directory_path:
        return {
            "status": False,
            "message": "No directory selected."
        }

    config_data: dict = config.read()

    if config_data.get("paths") is None:
        config_data["paths"] = list()
    
    if directory_path not in config_data["paths"]:
        return {
            "status": False,
            "message": "Directory does not exists in config."
        }
    
    config_data["paths"].remove(directory_path)
    config.write(config_data)

    return {
        "status": True,
        "message": "Successfully removed directory from config."
    }


def list_paths_in_config() -> dict:
    config_data: dict = config.read()

    if config_data.get("paths") is None:
        config_data["paths"] = list()
        config.write(config_data)
    
    print(color.get_text_with_gradient("Paths in config:", info_gradient))
    for path in config_data["paths"]:
        if not path:
            continue

        if os.path.isdir(path):
            print("\t" + color.get_text_with_gradient(path, directory_gradient))
        else:
            print("\t" + color.get_text_with_gradient(path, file_gradient))
