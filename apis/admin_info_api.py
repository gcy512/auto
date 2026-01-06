import requests

from config import projict_url


class AdminInfoApi:
    @classmethod
    def get_admin_info(cls, token, keyword=None):
        """
        获取管理员信息，支持模糊查询
        :param token: 登录后获取的token（包含Bearer前缀）
        :param keyword: 可选，模糊查询的关键字
        :return: 响应对象
        """
        url = projict_url + "/info"
        headers = {
            "Authorization": token,
            "Content-Type": "application/json"
        }
        
        # 如果有关键字，添加到查询参数中
        params = {}
        if keyword:
            params["keyword"] = keyword
        
        res = requests.get(url, headers=headers, params=params)
        return res
    
    @classmethod
    def search_admin_info(cls, token, keyword):
        """
        在管理员信息中进行模糊查询
        :param token: 登录后获取的token（包含Bearer前缀）
        :param keyword: 查询关键字
        :return: 响应对象
        """
        return cls.get_admin_info(token, keyword)
    
    @classmethod
    def filter_info_by_keyword(cls, token, keyword):
        """
        获取管理员信息并在返回数据中过滤包含关键字的信息
        :param token: 登录后获取的token（包含Bearer前缀）
        :param keyword: 查询关键字
        :return: 包含关键字的过滤后的数据字典，如果没有匹配返回None
        """
        res = cls.get_admin_info(token)
        if res.status_code == 200:
            response_json = res.json()
            if response_json.get("code") == 200:
                data = response_json.get("data")
                if data:
                    # 递归搜索数据中是否包含关键字
                    def search_in_dict(d, keyword):
                        """递归搜索字典中是否包含关键字"""
                        if isinstance(d, dict):
                            for key, value in d.items():
                                if isinstance(value, (dict, list)):
                                    if search_in_dict(value, keyword):
                                        return True
                                elif isinstance(value, str) and keyword.lower() in value.lower():
                                    return True
                        elif isinstance(d, list):
                            for item in d:
                                if search_in_dict(item, keyword):
                                    return True
                        elif isinstance(d, str) and keyword.lower() in d.lower():
                            return True
                        return False
                    
                    if search_in_dict(data, keyword):
                        return data
        return None
    
    @classmethod
    def get_admin_list(cls, token, page_num=1, page_size=10, keyword=None):
        """
        获取管理员列表，支持分页和关键字模糊查询
        :param token: 登录后获取的token（包含Bearer前缀）
        :param page_num: 页码，默认1
        :param page_size: 每页数量，默认10
        :param keyword: 可选，模糊查询的关键字
        :return: 响应对象
        """
        url = projict_url + "/list"
        headers = {
            "Authorization": token,
            "Content-Type": "application/json"
        }
        
        params = {
            "pageNum": page_num,
            "pageSize": page_size
        }
        
        # 如果有关键字，添加到查询参数中
        if keyword:
            params["keyword"] = keyword
        
        res = requests.get(url, headers=headers, params=params)
        return res
    
    @classmethod
    def search_admin_list(cls, token, keyword, page_num=1, page_size=10):
        """
        在管理员列表中进行模糊查询
        :param token: 登录后获取的token（包含Bearer前缀）
        :param keyword: 查询关键字
        :param page_num: 页码，默认1
        :param page_size: 每页数量，默认10
        :return: 响应对象
        """
        return cls.get_admin_list(token, page_num, page_size, keyword)


if __name__ == '__main__':
    from apis.login_api import LoginApi
    
    # 测试登录并获取token
    login_data = {"username": "admin", "password": "macro123"}
    token = LoginApi.get_token(login_data)
    
    if token:
        print(f"获取到token: {token}")
        # 测试获取管理员信息
        res = AdminInfoApi.get_admin_info(token)
        print(f"管理员信息: {res.json()}")
        
        # 测试管理员列表接口（带关键字查询）
        print("\n=== 测试管理员列表接口 ===")
        list_res = AdminInfoApi.get_admin_list(token, page_num=1, page_size=10, keyword="测试")
        print(f"列表查询结果: {list_res.json()}")
        
        # 测试模糊查询
        if res.status_code == 200:
            search_res = AdminInfoApi.search_admin_list(token, "测试")
            print(f"模糊查询结果: {search_res.json()}")
    else:
        print("登录失败，无法获取token")

