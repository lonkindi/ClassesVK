import requests
import time
import key_storage

access_token = key_storage.get_token()


class UserVK:
    def __init__(self, vk_token, user_id):
        self.token = vk_token
        self.user_id = user_id
        self.friend_set = self.get_friends()
        user_info = self.get_user_info()['response'][0]
        self.first_name = user_info['first_name']
        self.last_name = user_info['last_name']

    def __and__(self, other):
        result_list = []
        result_set = self.friend_set & other.friend_set
        for result_id in result_set:
            result_list.append(UserVK(access_token, result_id))
        return result_list

    def __str__(self):
        return f'https://vk.com/id{self.user_id}'

    def __repr__(self):
        return f'https://vk.com/id{self.user_id}'

    def get_params(self):
        return dict(
            access_token=self.token,
            v='5.89'
        )

    def get_user_info(self):
        params = self.get_params()
        params['user_id'] = self.user_id
        response = requests.get('https://api.vk.com/method/users.get', params)
        return response.json()

    def get_friends(self):
        time.sleep(1 / 3)
        print('*', end='')
        params = self.get_params()
        params['user_id'] = self.user_id
        response = requests.get('https://api.vk.com/method/friends.get', params)
        friend_list = set(response.json()['response']['items'])
        return friend_list

    def get_mutual(self, target_uid):
        params = self.get_params()
        params['source_uid'] = self.user_id
        params['target_uid'] = target_uid
        response = requests.get('https://api.vk.com/method/friends.getMutual', params)
        return response.json()


print('Задача №1')
user_1 = UserVK(access_token, user_id=24863449)
user_2 = UserVK(access_token, user_id=327379059)
print(
    f'\nПользователь ВК id={user_1.user_id}, фамилия: {user_1.last_name}, имя: {user_1.first_name}, в друзьях: {len(user_1.friend_set)} чел. ')
print(
    f'Пользователь ВК id={user_2.user_id}, фамилия: {user_2.last_name}, имя: {user_2.first_name}, в друзьях: {len(user_2.friend_set)} чел. ')
mutual_list = user_1.get_mutual(327379059)
m_dict = {}
for m_friend in mutual_list['response']:
    m_dict[m_friend] = UserVK(access_token, m_friend)
print(
    f'\nПо данным функции API BK у пользователей {user_1.first_name} {user_1.last_name} и {user_2.first_name} {user_2.last_name} общих друзей - {len(mutual_list["response"])}, вот они:')
for friend in m_dict:
    cur_friend = m_dict.get(friend)
    print(f'- {cur_friend.first_name} {cur_friend.last_name}')
print(f'\nЗадача №2')
mutual_list = user_1 & user_2
print(
    f'\nСогласно результата вычисления "user_1 & user_2" у пользователей {user_1.first_name} {user_1.last_name} и {user_2.first_name} {user_2.last_name} общих друзей - {len(mutual_list)}, вот они:')
for friend in mutual_list:
    print(f'- {friend.first_name} {friend.last_name}')
print(f'\nЗадача №3')
print(user_1)
print(user_2)
# 'af9c7f37dc361ad97***e979d4be8143d4e6bc1c2466a4722c1f3fefc185e107719ebaa66a8ff92cdf3d8'
