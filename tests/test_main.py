import os
import sys
import pytest

from .. import main

file_name = 'temp.json'
file_data = {
    'test': {
        'msg': 'hello',
        'usr': 'world'
    }
}


def setup_module(module):
    """ create tepm file """
    if os.path.exists(file_name):
        os.remove(file_name)

    with open('temp.json', 'w') as file:
        file.write(str(file_data))


def teardown(module):
    """ remove file """
    if os.path.exists(file_name):
        os.remove(file_name)


def test_config_build():
    config = main.build_config_json(file_name)
    assert config['test']['msg'] == 'hello'
    assert config['test']['usr'] == 'world'


def test_config_not_found():
    with pytest.raises(ValueError) as exept_info:
        main.build_config_json('nofileexists.json')
    assert str(exept_info.value) == 'Configuration build failed'
