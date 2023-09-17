from tkinter.filedialog import askopenfilename, askdirectory
from cryptography.fernet import Fernet
import platform
import pwinput
import tkinter
import base64
import json
import os

encrypted_file_extension = ".user_enc"
sys_os = platform.system()


def clear_terminal() -> None:
    """
    The function clears the terminal screen.
    """
    os.system("cls") if sys_os == "Windows" else os.system('clear')


def can_file_be_renamed(path: str) -> bool:
    """
    The function `can_file_be_renamed` checks if a file can be renamed by attempting to rename it and
    returning True if successful, False otherwise.
    
    :param path: The `path` parameter is a string that represents the file path of the file that you
    want to check if it can be renamed
    :type path: str
    :return: a boolean value. It returns True if the file at the given path can be renamed, and False if
    it cannot be renamed.
    """
    try:
        os.rename(path, path)
        return True
    except Exception:
        return False


def can_file_be_written(path: str) -> bool:
    """
    The function `can_file_be_written` checks if a file can be opened for reading and writing.
    
    :param path: The `path` parameter is a string that represents the file path of the file you want to
    check if it can be written
    :type path: str
    :return: The function `can_file_be_written` returns a boolean value. It returns `True` if the file
    at the given path can be successfully opened and written to, and `False` if there is an exception or
    error encountered during the process.
    """
    try:
        with open(path, "rb") as f:
            data = f.read()
        
        with open(path, 'wb') as f:
            f.write(data)
        
        return True
    except Exception:
        return False

def encrypt(plaintext: str | bytes, key: str | bytes, return_bytes: bool = False) -> str | bytes:
    """
    The `encrypt` function takes a plaintext message and a key, and encrypts the message using the
    Fernet encryption algorithm, returning the encrypted message as a string or bytes depending on the
    `return_bytes` parameter.
    
    :param plaintext: The `plaintext` parameter represents the text or data that you want to encrypt. It
    can be either a string or bytes
    :type plaintext: str | bytes
    :param key: The `key` parameter is the encryption key used to encrypt the plaintext. It can be
    either a string or bytes. If it is a string, it will be encoded into bytes before encryption
    :type key: str | bytes
    :param return_bytes: The `return_bytes` parameter is a boolean flag that determines whether the
    encrypted result should be returned as bytes or as a string. If `return_bytes` is set to `True`, the
    function will return the encrypted result as bytes. If `return_bytes` is set to `False` (or,
    defaults to False
    :type return_bytes: bool (optional)
    :return: The function `encrypt` returns either a string or bytes, depending on the value of the
    `return_bytes` parameter. If `return_bytes` is `True`, it returns the encrypted result as bytes.
    Otherwise, it returns the encrypted result as a string.
    """
    try:
        if isinstance(key, str):
            key = key.encode()

        if not isinstance(plaintext, str) and not isinstance(plaintext, bytes):
            plaintext = str(plaintext)

        if isinstance(plaintext, str):
            plaintext = plaintext.encode()

        fernet = Fernet(key)
        result = fernet.encrypt(plaintext)

        if return_bytes:
            return result
        
        return result.decode()
    except Exception:
        return None


def decrypt(ciphertext: str | bytes, key: str | bytes, return_bytes: bool = False) -> str | bytes | None:
    """
    The `decrypt` function takes a ciphertext and a key, and attempts to decrypt the ciphertext using
    the key, returning the decrypted result as a string or bytes object, or None if decryption fails.
    
    :param ciphertext: The `ciphertext` parameter represents the encrypted message that needs to be
    decrypted. It can be either a string or bytes
    :type ciphertext: str | bytes
    :param key: The `key` parameter is the encryption key used to decrypt the ciphertext. It can be
    either a string or bytes. If it is a string, it will be encoded to bytes before decryption
    :type key: str | bytes
    :param return_bytes: The `return_bytes` parameter is a boolean flag that determines whether the
    decrypted result should be returned as bytes or as a string. If `return_bytes` is set to `True`, the
    function will return the decrypted result as bytes. If `return_bytes` is set to `False` (or,
    defaults to False
    :type return_bytes: bool (optional)
    :return: The function `decrypt` returns either a string, bytes, or `None`.
    """
    try:
        if isinstance(key, str):
            key = key.encode()
        
        if isinstance(ciphertext, str):
            ciphertext = base64.b64decode(ciphertext)
        
        try:
            fernet = Fernet(key)
            result = fernet.decrypt(ciphertext)
        except Exception:
            return None

        if return_bytes:
            return result
        
        return result.decode()
    except Exception:
        return None


def get_hidden_input(prompt: str, mask: str = "*") -> str:
    """
    The function `get_hidden_input` takes a prompt and an optional mask character as input, and returns
    a hidden input from the user.
    
    :param prompt: The prompt is a string that will be displayed to the user to ask for input. It is
    used to provide instructions or ask a question to the user
    :type prompt: str
    :param mask: The `mask` parameter is a string that specifies the character(s) to be used as a mask
    for hiding the input. By default, it is set to "*", defaults to *
    :type mask: str (optional)
    :return: a string.
    """
    return pwinput.pwinput(prompt=prompt, mask=mask)


# The `Config` class is a Python class that provides methods for reading and writing configuration
# data from a JSON file.
class Config:
    def __init__(self, config_path: str) -> None:
        self.config_path = config_path
        self._config = self.load_config()

    def _fix_config(self) -> None:
        """
        The function `_fix_config` checks if a config file exists, and if not, creates an empty one.
        :return: None.
        """
        if not os.path.exists(self.config_path):
            with open(self.config_path, 'w') as f:
                json.dump({}, f)
            
            return
            
        with open(self.config_path, 'r') as f:
            if f.read().strip() == '':
                with open(self.config_path, 'w') as f:
                    json.dump({}, f)
        
    def load_config(self):
        """
        The function loads a JSON configuration file and assigns it to the `_config` attribute after
        fixing it.
        """
        self._fix_config()
        with open(self.config_path, 'r') as f:
            self._config = json.load(f)
        
    def read(self) -> dict:
        """
        The function reads and returns the loaded configuration as a dictionary.
        :return: The method is returning a dictionary object.
        """
        self.load_config()
        return self._config
    
    def write(self, config: dict) -> None:
        """
        The function writes a dictionary object to a file in JSON format.
        
        :param config: The `config` parameter is a dictionary that contains the configuration data that
        you want to write to a file
        :type config: dict
        """
        self._config = config
        with open(self.config_path, 'w') as f:
            json.dump(self._config, f)


def list_files(directory: str) -> set:
    """
    The function `list_files` recursively lists all files in a given directory and its subdirectories.
    
    :param directory: The directory parameter is a string that represents the path to a directory
    :type directory: str
    :return: a set of file paths within the specified directory and its subdirectories.
    """
    files = set()
    
    for file in os.listdir(directory):
        path = os.path.join(directory, file)
        if os.path.isdir(path):
            for file in list_files(path):
                files.add(file)
        else:
            files.add(path)
    
    return files


def encrypt_file(file_path: str, key: str) -> bool:
    """
    The function encrypts a file using a given key and renames the file with an encrypted file
    extension.
    
    :param file_path: The `file_path` parameter is a string that represents the path to the file that
    needs to be encrypted
    :type file_path: str
    :param key: The `key` parameter is a string that represents the encryption key. This key is used to
    encrypt the data in the file
    :type key: str
    :return: a boolean value. It returns True if the file was successfully encrypted and renamed, and
    False otherwise.
    """
    if file_path.endswith(encrypted_file_extension):
        return False
    
    if not can_file_be_renamed(file_path) or not can_file_be_written(file_path):
        return False
    
    with open(file_path, 'rb') as f:
        data = f.read()
    
    encrypted_data = encrypt(data, key, True)
    
    with open(file_path, 'wb') as f:
        f.write(encrypted_data)

    os.rename(file_path, file_path + encrypted_file_extension)
    return True


def decrypt_file(file_path: str, key: str) -> bool:
    """
    The function decrypts a file using a given key and renames it to remove the encrypted file
    extension.
    
    :param file_path: The `file_path` parameter is a string that represents the path to the file that
    needs to be decrypted
    :type file_path: str
    :param key: The "key" parameter is a string that represents the encryption key used to decrypt the
    file
    :type key: str
    :return: a boolean value. It returns True if the file was successfully decrypted and renamed, and
    False otherwise.
    """
    if not file_path.endswith(encrypted_file_extension):
        return False
    
    if not can_file_be_renamed(file_path) or not can_file_be_written(file_path):
        return False
    
    with open(file_path, 'rb') as f:
        data = f.read()
    
    decrypted_data = decrypt(data, key, True)
    if decrypted_data is None:
        return False
    
    with open(file_path, 'wb') as f:
        f.write(decrypted_data)

    os.rename(file_path, file_path.removesuffix(encrypted_file_extension))
    return True


def select_file() -> str | None:
    """
    The `select_file` function opens a file dialog box for the user to select a file and returns the
    path of the selected file or `None` if no file is selected.
    :return: The function `select_file()` returns a string representing the path of the selected file,
    or `None` if no file was selected.
    """
    root = tkinter.Tk()
    root.title("Select File")
    root.geometry('0x0')
    path = askopenfilename() or None
    root.destroy()
    return path

def select_directory() -> str | None:
    """
    The function `select_directory` opens a file dialog to allow the user to select a directory and
    returns the selected directory path or `None` if no directory is selected.
    :return: The function `select_directory` returns a string representing the selected directory path,
    or `None` if no directory was selected.
    """
    root = tkinter.Tk()
    root.title("Select Directory")
    root.geometry('0x0')
    path = askdirectory() or None
    root.destroy()
    return path
