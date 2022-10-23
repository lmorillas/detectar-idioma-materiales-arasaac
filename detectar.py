# coding: utf-8

import textract
import textblob
from textblob.exceptions import TranslatorError
import os
import zipfile
import tarfile
import tempfile
import shutil


def descomprimir(f):
    with tempfile.TemporaryDirectory() as tmpdirname:
        with zipfile.ZipFile(f,"r") as zip_ref:
            zip_ref.extractall(tmpdirname)
        with tarfile.open(f) as tar:
            def is_within_directory(directory, target):
                
                abs_directory = os.path.abspath(directory)
                abs_target = os.path.abspath(target)
            
                prefix = os.path.commonprefix([abs_directory, abs_target])
                
                return prefix == abs_directory
            
            def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
            
                for member in tar.getmembers():
                    member_path = os.path.join(path, member.name)
                    if not is_within_directory(path, member_path):
                        raise Exception("Attempted Path Traversal in Tar File")
            
                tar.extractall(path, members, numeric_owner=numeric_owner) 
                
            
            safe_extract(tar, tmpdirname)

def detectar(f):
    texto = textract.process(f)
    texto = texto.decode('utf-8')
    _texto = textblob.TextBlob(texto)
    try:
        lang = _texto.detect_language()
        return lang
    except TranslatorError:
        return None


def nombre_material(m):
    pass

materiales = []
extensiones = '.doc .docx .pdf .odt'.split()

def mover(path):
    for root, dirs, files in os.walk(path):
        _files = [f for f in files if os.path.splitext(f)[-1] in extensiones]
        for file_ in _files:
            lang = detectar(os.path.join(root, file_))
            if lang:
                if not os.path.exists(os.path.join(root, lang)):
                    os.mkdir(os.path.join(root, lang))
                shutil.move(os.path.join(root, file_), os.path.join(root, lang, file_))
            else:
                print (root, file_)

        
