import requests

access_token = 'af9c7f37dc361ad97888e979d4be8143d4e6bc1c2466a4722c1f3fefc185e107719ebaa66a8ff92cdf3d8'
"""
 API_ID, APP_ID, client_id, = 7331927 
 user_id=24863449 
 https://oauth.vk.com/blank.html#access_token=af9c7f37dc361ad97888e979d4be8143d4e6bc1c2466a4722c1f3fefc185e107719ebaa66a8ff92cdf3d8&expires_in=0&user_id=24863449&state=123456
 
 https://oauth.vk.com/authorize?client_id=7331927&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=friends,offline&response_type=token&v=5.103&state=123456
"""

class UserVK:
    def __init__(self, vk_token, user_id):
        self.token = vk_token
        self.user_id = user_id
        self.friend_set = self.get_friends()
        user_info = self.get_user_info()['response'][0]
        #print('self.get_user_info()["response"]', self.get_user_info()['response'])
        self.first_name = user_info['first_name']
        self.last_name = user_info['last_name']

    def get_params(self):
        return dict(
            access_token=self.token,
            v='5.89'
        )

    def get_user_info(self):
        params = self.get_params()
        params['user_id'] = self.user_id
        #params['fields'] = 'friend_status'
        #print(params)
        response = requests.get('https://api.vk.com/method/users.get', params)
        #print(response)
        return response.json()

    def get_friends(self):
        params = self.get_params()
        params['user_id'] = self.user_id
        # params['fields'] = 'friend_status'
        # print(params)
        response = requests.get('https://api.vk.com/method/friends.get', params)
        friend_list = set(response.json()['response']['items'])
        #print('friend_list', friend_list)
        return friend_list

    def get_mutual(self, target_uid):
        params = self.get_params()
        params['source_uid'] = self.user_id
        params['target_uid'] = target_uid
        response = requests.get('https://api.vk.com/method/friends.getMutual', params)
        #print(response)
        return response.json()

print('Задача №1')
user_1 = UserVK(access_token, user_id=24863449)
user_2 = UserVK(access_token, user_id=327379059)
print(f'Пользователь ВК id={user_2.user_id}, фамилия: {user_2.last_name}, имя: {user_2.first_name}, в друзьях: {len(user_2.friend_set)} чел. ')
mutual_list = user_1.get_mutual(327379059)
m_dict = {}
for m_friend in mutual_list['response']:
    #print(m_friend)
    m_dict[m_friend] = UserVK(access_token, m_friend)
print(f'Согласно данным функции API BK у пользователей {user_1.first_name} {user_1.last_name} и {user_2.first_name} {user_2.last_name} общих друзей - {len(mutual_list["response"])}, вот они:')
for friend in m_dict:
    cur_friend = m_dict.get(friend)
    print(f'- {cur_friend.first_name} {cur_friend.last_name}')
print('Задача №2')

#print(user_1.friend_set & user_2.friend_set)

#print(user_2.get_mutual(24863449))
#print(second_user.friend_list)
#first_user.get_Mutual(327379059)
#first_user.get_users(24863449)
#second_user.get_users(327379059)
