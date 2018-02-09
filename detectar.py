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
            tar.extractall(tmpdirname)

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

        
