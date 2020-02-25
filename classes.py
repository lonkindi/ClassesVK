import requests

access_token = 'af9c7f37dc361ad97888e979d4be8143d4e6bc1c2466a4722c1f3fefc185e107719ebaa66a8ff92cdf3d8'
"""
 API_ID, APP_ID, client_id, = 7331927 
 user_id=24863449 
 https://oauth.vk.com/blank.html#access_token=af9c7f37dc361ad97888e979d4be8143d4e6bc1c2466a4722c1f3fefc185e107719ebaa66a8ff92cdf3d8&expires_in=0&user_id=24863449&state=123456
 
 https://oauth.vk.com/authorize?client_id=7331927&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=friends,offline&response_type=token&v=5.103&state=123456
"""

class UserVK:
    def __init__(self, vk_token, user_id=None):
        self.token = vk_token
        self.user_id = user_id

    def get_params(self):
        return dict(
            access_token=self.token,
            v='5.103'
        )

    def get_users(self, user_id):
        params = self.get_params()
        params['user_id'] = user_id
        params['fields'] = 'friend_status'
        print(params)
        response = requests.get('https://api.vk.com/method/users.get', params)
        print(response)
        print(response.json())

    def get_Mutual(self, target_uid):
        params = self.get_params()
        params['source_uid'] = self.user_id
        params['target_uid'] = target_uid
        response = requests.get('https://api.vk.com/method/friends.getMutual', params)
        print(response)
        print(response.json())


first_user = UserVK(access_token, user_id=24863449)
second_user = UserVK(access_token, user_id=327379059)
first_user.get_Mutual(327379059)
#first_user.get_users(24863449)
#second_user.get_users(327379059)
