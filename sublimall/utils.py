# -*- coding:utf-8 -*-
import os
import sys
import uuid
import shutil
import sublime
import tempfile
import platform
from subprocess import PIPE
from subprocess import Popen
from . import SETTINGS_USER_FILE
from .logger import logger


def is_linux():
    return platform.system().lower() == 'linux'


def is_osx():
    return platform.system().lower() == 'darwin'


def is_win():
    return ('win32' in str(sys.platform).lower())


def humansize(nbytes):
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    if nbytes == 0:
        return '0 B'
    i = 0
    while nbytes >= 1024 and i < len(suffixes) - 1:
        nbytes /= 1024.
        i += 1
    f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
    return '%s %s' % (f, suffixes[i])


def get_7za_bin():
    settings = sublime.load_settings(SETTINGS_USER_FILE)
    zip_bin = None

    if settings.get('7za_path') and os.path.exists(settings.get('7za_path')):
        zip_bin = settings.get('7za_path')
    elif shutil.which('7za'):
        zip_bin = shutil.which('7za')
    elif shutil.which('7z'):
        zip_bin = shutil.which('7z')
    elif shutil.which('p7zip'):
        zip_bin = shutil.which('p7zip')
    elif is_win():
        if os.path.exists(os.path.join(os.environ.get('ProgramFiles'), '7-Zip', '7z.exe')):
            zip_bin = os.path.join(os.environ.get('ProgramFiles'), '7-Zip', '7z.exe')
        if os.path.exists(os.path.join(os.environ.get('ProgramFiles(x86)'), '7-Zip', '7z.exe')):
            zip_bin = os.path.join(os.environ.get('ProgramFiles(x86)'), '7-Zip', '7z.exe')
    elif is_osx():
        basename_cmd = "readlink -m /usr/local/Cellar/p7zip/*/bin/7za"
        c = Popen(basename_cmd, shell=True, stdin=PIPE)
        zip_path = c.communicate()[0].replace('\n', '')
        if zip_path:
            zip_bin = zip_path

    logger.info('7za_path detected: %s' % zip_bin)
    return zip_bin


def generate_temp_filename():
    return os.path.join(tempfile.gettempdir(), 'sublime-sync_%s.zip' % str(uuid.uuid4()))
