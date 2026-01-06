import allure
import pytest

from apis.login_api import LoginApi
from utils.read_excel import ExcelReader
from utils.str_to_int import StrToInt
from utils.stringtodict import StringToDictConverter

reader = ExcelReader().read_excel("mall登录.xlsx", 1)  # 指定文件名称和工作表编号
class TestLogin:
    @pytest.mark.parametrize("title,data,zhuangtaima, code, yuqi",reader)
    @allure.title('{title}')
    def test_login(self,title,data,zhuangtaima, code, yuqi):
        with allure.step('将data转换为字典'):
            data = StringToDictConverter.convert(data)
        with allure.step('登录'):
            res=LoginApi.login(data)
            print(res.text)
        with allure.step('将zhuangtaima,code转换为int'):
            zhuangtaima=StrToInt.str_to_int(zhuangtaima)
            code=StrToInt.str_to_int(code)
        with allure.step('断言'):

            assert zhuangtaima == res.status_code
            assert code == res.json()["code"]
            assert yuqi in res.json()["message"]

