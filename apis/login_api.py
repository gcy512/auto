import requests

from config import projict_url
class LoginApi:
    @classmethod
    def login(cls,data):
        url_login = projict_url + "/login"
        res=requests.post(url_login,json=data)
        return res
    
    @classmethod
    def get_token(cls, data):
        """
        登录并获取token
        :param data: 登录数据，包含username和password
        :return: token字符串，如果登录失败返回None
        """
        res = cls.login(data)
        if res.status_code == 200 and res.json().get("code") == 200:
            token_data = res.json().get("data", {})
            token = token_data.get("token")
            token_head = token_data.get("tokenHead", "Bearer ")
            # 返回完整的token（包含tokenHead）
            return f"{token_head}{token}" if token else None
        return None
    
    @classmethod
    def get_token_with_head(cls, data):
        """
        登录并获取token和tokenHead
        :param data: 登录数据，包含username和password
        :return: 元组(token, tokenHead)，如果登录失败返回(None, None)
        """
        res = cls.login(data)
        if res.status_code == 200 and res.json().get("code") == 200:
            token_data = res.json().get("data", {})
            token = token_data.get("token")
            token_head = token_data.get("tokenHead", "Bearer ")
            return token, token_head
        return None, None

if __name__ == '__main__':
    res=LoginApi.login(data={"username":"admin","password":"<PASSWORD>"})
    print(res.json())
    token = LoginApi.get_token(data={"username":"admin","password":"<PASSWORD>"})
    print(f"Token: {token}")