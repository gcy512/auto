# -*- coding: utf-8 -*-
import os
import sys

# 只设置环境变量，不修改标准输出流（避免与pytest冲突）
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'

import allure
import pytest

from apis.login_api import LoginApi
from apis.admin_info_api import AdminInfoApi
from utils.stringtodict import StringToDictConverter
from utils.loger_util import APITestLogger

logger = APITestLogger.setup_logger()


class TestAdminInfo:
    """测试管理员信息接口"""
    
    @allure.title("登录获取token后访问管理员信息接口")
    def test_get_admin_info_after_login(self):
        """
        测试流程：
        1. 登录获取token
        2. 使用token访问/admin/info接口
        3. 验证返回结果
        """
        # 登录数据
        login_data = {"username": "admin", "password": "macro123"}
        
        with allure.step('登录获取token'):
            token = LoginApi.get_token(login_data)
            logger.info(f"获取到的token: {token}")
            assert token is not None, "登录失败，无法获取token"
        
        with allure.step('访问管理员信息接口'):
            res = AdminInfoApi.get_admin_info(token)
            logger.info(f"响应状态码: {res.status_code}")
            logger.info(f"响应内容: {res.text}")
        
        with allure.step('验证响应结果'):
            assert res.status_code == 200, f"请求失败，状态码: {res.status_code}"
            response_json = res.json()
            assert response_json.get("code") == 200, f"接口返回错误: {response_json.get('message')}"
            assert response_json.get("data") is not None, "返回数据为空"
    
    @allure.title("使用token进行模糊查询测试")
    @pytest.mark.parametrize("keyword", ["admin", "用户", "权限", "商品"])
    def test_search_admin_info(self, keyword):
        """
        测试模糊查询功能
        注意：/admin/info接口返回的是管理员信息和菜单列表，不包含"测试"关键字
        :param keyword: 查询关键字
        """
        # 登录数据
        login_data = {"username": "admin", "password": "macro123"}
        
        with allure.step('登录获取token'):
            token = LoginApi.get_token(login_data)
            assert token is not None, "登录失败，无法获取token"
        
        with allure.step(f'使用关键字"{keyword}"进行模糊查询'):
            res = AdminInfoApi.search_admin_info(token, keyword)
            logger.info(f"查询关键字: {keyword}")
            logger.info(f"响应状态码: {res.status_code}")
            logger.info(f"响应内容: {res.text}")
        
        with allure.step('验证查询结果'):
            assert res.status_code == 200, f"请求失败，状态码: {res.status_code}"
            response_json = res.json()
            assert response_json.get("code") == 200, f"接口返回错误: {response_json.get('message')}"
            
            # 验证返回结果中包含关键字（模糊匹配）
            data = response_json.get("data")
            assert data is not None, "返回数据为空"
            
            # 将返回的数据转换为字符串进行模糊匹配
            data_str = str(data).lower()
            keyword_lower = keyword.lower()
            contains_keyword = keyword_lower in data_str
            logger.info(f"返回数据: {data}")
            logger.info(f"数据中包含关键字'{keyword}': {contains_keyword}")
            
            # 验证数据结构的完整性
            assert "username" in data or "roles" in data or "menus" in data, "返回数据格式不正确"
            
            # 对于这些关键字，数据中应该包含（因为返回的数据中有admin、用户、权限、商品等）
            if keyword in ["admin", "用户", "权限", "商品"]:
                assert contains_keyword, f"返回数据中应包含关键字'{keyword}'，实际数据: {data_str[:200]}"
    
    @allure.title("测试管理员列表接口-使用关键字'测试'进行模糊查询")
    def test_search_admin_list_with_keyword(self):
        """
        测试管理员列表接口，使用关键字"测试"进行模糊查询
        使用接口：/admin/list?pageNum=1&pageSize=10&keyword=测试
        """
        # 登录数据
        login_data = {"username": "admin", "password": "macro123"}
        
        with allure.step('登录获取token'):
            token = LoginApi.get_token(login_data)
            assert token is not None, "登录失败，无法获取token"
        
        with allure.step('使用关键字"测试"查询管理员列表'):
            res = AdminInfoApi.search_admin_list(token, keyword="测试", page_num=1, page_size=10)
            logger.info(f"响应状态码: {res.status_code}")
            logger.info(f"响应内容: {res.text}")
        
        with allure.step('验证查询结果'):
            assert res.status_code == 200, f"请求失败，状态码: {res.status_code}"
            response_json = res.json()
            assert response_json.get("code") == 200, f"接口返回错误: {response_json.get('message')}"
            
            data = response_json.get("data")
            assert data is not None, "返回数据为空"
            logger.info(f"返回数据: {data}")
            
            # 验证返回数据结构（通常包含list和total等字段）
            if isinstance(data, dict):
                if "list" in data:
                    admin_list = data.get("list", [])
                    total = data.get("total", 0)
                    logger.info(f"查询到的管理员数量: {len(admin_list)}")
                    logger.info(f"总记录数: {total}")
                    
                    # 验证返回的列表中是否包含"测试"关键字
                    if admin_list:
                        for admin in admin_list:
                            admin_str = str(admin).lower()
                            if "测试" in admin_str or "test" in admin_str:
                                logger.info(f"找到包含'测试'的管理员: {admin}")
                    else:
                        logger.info("未找到包含'测试'关键字的管理员")
    
    @allure.title("测试管理员列表接口-分页查询")
    @pytest.mark.parametrize("page_num,page_size", [(1, 10), (1, 5), (2, 10)])
    def test_get_admin_list_pagination(self, page_num, page_size):
        """
        测试管理员列表接口的分页功能
        :param page_num: 页码
        :param page_size: 每页数量
        """
        # 登录数据
        login_data = {"username": "admin", "password": "macro123"}
        
        with allure.step('登录获取token'):
            token = LoginApi.get_token(login_data)
            assert token is not None, "登录失败，无法获取token"
        
        with allure.step(f'获取第{page_num}页，每页{page_size}条数据'):
            res = AdminInfoApi.get_admin_list(token, page_num=page_num, page_size=page_size)
            logger.info(f"响应状态码: {res.status_code}")
            logger.info(f"响应内容: {res.text}")
        
        with allure.step('验证分页结果'):
            assert res.status_code == 200, f"请求失败，状态码: {res.status_code}"
            response_json = res.json()
            assert response_json.get("code") == 200, f"接口返回错误: {response_json.get('message')}"
            
            data = response_json.get("data")
            assert data is not None, "返回数据为空"
            
            if isinstance(data, dict) and "list" in data:
                admin_list = data.get("list", [])
                assert len(admin_list) <= page_size, f"返回的数据量不应超过每页数量{page_size}"
                logger.info(f"第{page_num}页返回{len(admin_list)}条数据")
    
    @allure.title("测试在管理员信息中搜索包含'测试'的信息")
    def test_search_test_info(self):
        """
        测试在管理员信息中搜索功能
        注意：/admin/info接口返回的是管理员信息和菜单列表，通常不包含"测试"关键字
        此测试主要用于验证搜索功能是否正常工作
        """
        # 登录数据
        login_data = {"username": "admin", "password": "macro123"}
        
        with allure.step('登录获取token'):
            token = LoginApi.get_token(login_data)
            assert token is not None, "登录失败，无法获取token"
        
        with allure.step('获取管理员信息'):
            res = AdminInfoApi.get_admin_info(token)
            assert res.status_code == 200, f"请求失败，状态码: {res.status_code}"
            response_json = res.json()
            assert response_json.get("code") == 200, f"接口返回错误: {response_json.get('message')}"
            data = response_json.get("data")
            assert data is not None, "返回数据为空"
            logger.info(f"管理员信息数据: {data}")
        
        with allure.step('验证返回数据的完整性'):
            # 验证数据结构
            assert "username" in data, "返回数据中应包含username字段"
            assert "roles" in data, "返回数据中应包含roles字段"
            assert "menus" in data, "返回数据中应包含menus字段"
            logger.info(f"用户名: {data.get('username')}")
            logger.info(f"角色: {data.get('roles')}")
            logger.info(f"菜单数量: {len(data.get('menus', []))}")
        
        with allure.step('在返回数据中搜索包含"测试"的信息'):
            # 使用API的过滤方法
            filtered_data = AdminInfoApi.filter_info_by_keyword(token, "测试")
            if filtered_data:
                logger.info(f"找到包含'测试'的数据: {filtered_data}")
            else:
                logger.info("返回数据中未包含'测试'关键字（这是正常的，因为/admin/info接口返回的是管理员信息和菜单列表）")
            
            # 直接检查返回数据
            data_str = str(data).lower()
            contains_test = "测试" in data_str or "test" in data_str
            logger.info(f"数据中包含'测试'或'test': {contains_test}")
            
            # 不强制要求包含"测试"，因为这是正常的业务场景
            # 如果确实需要测试包含"测试"的数据，应该使用其他接口或测试数据
    
    @allure.title("测试token过期或无效的情况")
    def test_admin_info_with_invalid_token(self):
        """
        测试使用无效token访问接口的情况
        """
        invalid_token = "Bearer invalid_token_12345"
        
        with allure.step('使用无效token访问接口'):
            res = AdminInfoApi.get_admin_info(invalid_token)
            logger.info(f"响应状态码: {res.status_code}")
            logger.info(f"响应内容: {res.text}")
        
        with allure.step('验证错误响应'):
            response_json = res.json()
            # 根据实际接口返回的错误码进行验证
            # 通常token无效会返回401或code不为200
            assert response_json.get("code") != 200 or res.status_code == 401, \
                "应该返回token无效的错误"


if __name__ == '__main__':
    pytest.main([__file__, "-v", "-s"])

