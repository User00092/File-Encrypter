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
    os.system("cls") if sys_os == "Windows" else os.system('clear')


def can_file_be_renamed(path: str) -> bool:
    try:
        os.rename(path, path)
        return True
    except Exception:
        return False


def can_file_be_written(path: str) -> bool:
    try:
        with open(path, "rb") as f:
            data = f.read()
        
        with open(path, 'wb') as f:
            f.write(data)
        
        return True
    except Exception:
        return False

def encrypt(plaintext: str | bytes, key: str | bytes, return_bytes: bool = False) -> str | bytes:
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
    return pwinput.pwinput(prompt=prompt, mask=mask)


class Config:
    def __init__(self, config_path: str) -> None:
        self.config_path = config_path
        self._config = self.load_config()

    def _fix_config(self) -> None:
        if not os.path.exists(self.config_path):
            with open(self.config_path, 'w') as f:
                json.dump({}, f)
            
            return
            
        with open(self.config_path, 'r') as f:
            if f.read().strip() == '':
                with open(self.config_path, 'w') as f:
                    json.dump({}, f)
        
    def load_config(self):
        self._fix_config()
        with open(self.config_path, 'r') as f:
            self._config = json.load(f)
        
    def read(self) -> dict:
        self.load_config()
        return self._config
    
    def write(self, config: dict) -> None:
        self._config = config
        with open(self.config_path, 'w') as f:
            json.dump(self._config, f)
        



def list_files(directory: str) -> set:
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
    root = tkinter.Tk()
    root.geometry('0x0')
    path = askopenfilename() or None
    root.destroy()
    return path

def select_directory() -> str | None:
    root = tkinter.Tk()
    root.geometry('0x0')
    path = askdirectory() or None
    root.destroy()
    return path

