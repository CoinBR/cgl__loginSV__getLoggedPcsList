from . import main as m
import pytest
import os


class Test_get_img_path():
    
    def test_invalid_folder(self):
        with pytest.raises(ValueError):
            m.get_img_path('invalid', 'max') 

    def test_invalid_img_name(self):
        with pytest.raises(ValueError):
            m.get_img_path('ref', 'invalid') 

    def test_valid_case(self):
        assert m.get_img_path('tmp', 'max') == 'img/tmp/maximize_icon.jpg' 


class Test_take_ss():

    def test_invalid_img_name(self):
        with pytest.raises(ValueError):
            m.take_ss('invalid') 

    def test_valid_img_name(self):
        m.take_ss('start') 



def test_list_pcs_n_loggedstatus():
    assert m.list_pcs_n_loggedstatus() == tuple(False for i in range(50))
