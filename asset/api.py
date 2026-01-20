import re,os
import json
import requests

dump_list = []
class InvalidCookieNya(Exception):
    pass

class api:
    def __init__(self, cookie:str):
        self.useragent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Instagram 243.1.0.14.111 (iPhone13,3; iOS 15_5; en_US; en-US; scale=3.00; 1170x2532; 382468104) NW/3'
        self.app_endpoint = 'https://i.instagram.com/api/v1/'
        self.web_endpoint = 'https://www.instagram.com/api/v1/'
        self.web_query_endpoint = 'https://www.instagram.com/graphql/query/'
        self.cookie = cookie

    def public_userid(self, username:list):
        list_uid = set()
        for username in username:
            try:
                respon = requests.get(f'https://www.instagram.com/{username}/',cookies={'cookie':self.cookie}).text
                ds_user_id = re.search(r'"user_id":"(\d+)"', str(respon)).group(1)
                if ds_user_id:list_uid.add(ds_user_id)
            except:continue
        return list(list_uid)
            
    def cookie_isvalid(self):
        if 'ds_user_id' not in self.cookie or 'sessionid' not in self.cookie:
            raise InvalidCookieNya('Cookie tidak valid')
        self.ds_user_id = re.search(r'ds_user_id=(\d+)',self.cookie).group(1)
        return self.ds_user_id

    def login(self):
        try:
            self.uid = self.cookie_isvalid()
            self.respon = requests.get(self.app_endpoint+f'users/{self.uid}/info/',headers={
                'user-agent':self.useragent,
                'cookie':self.cookie
            }).json()
            self.nama = self.respon['user']['full_name']
            return {'isvalid':True,'nama':self.nama}
        except InvalidCookieNya as e:
            os.remove('data/cookie.txt')
            exit(f'\n[!] {e}')
        except Exception as e:
            os.remove('data/cookie.txt')
            exit(f'\n[!] {e}')
    
    def dump_users(self,userid,after,mode):
        try:
            self.variabel = 'variables={"id":"%s","first":150,"after":"%s"}'%(userid,after)
            self.params = "query_hash=58712303d941c6855d4e888c5f0cd22f&{}".format(self.variabel) if not mode else "query_hash=37479f2b8209594dde7facb0d904896a&{}".format(self.variabel)
            self.respon = requests.get(self.web_query_endpoint,params=self.params,headers={"user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36","accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7","cookie": self.cookie}).json()
            self.edges_type = 'edge_followed_by' if mode else 'edge_follow'
            for a in self.respon['data']['user'][self.edges_type]['edges']:
                dump_list.append(json.dumps(a))
            print(f'\r[+] {len(dump_list)} saved',end='',flush=True)
            next = self.respon['data']['user'][self.edges_type]['page_info']['has_next_page']
            if next:
                cursor = self.respon['data']['user'][self.edges_type]['page_info']['end_cursor']
                self.dump_users(userid,cursor,mode)
            return {
                'yamete_id_list':dump_list,
                'error_message':None
            }
        except (Exception,KeyboardInterrupt) as e:
            return {
                'yamete_id_list':dump_list,
                'error_message':e
            }

    def profile_info(self,username):
        try:
            self.head = {'Host': 'www.instagram.com','cache-control': 'max-age=0','upgrade-insecure-requests': '1','accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7','sec-fetch-site': 'none','user-agent':self.useragent}
            respon = requests.get(f'https://www.instagram.com/api/v1/users/web_profile_info/?username={username}', headers=self.head).json()['data']['user']
            followers,following,posting = respon['edge_followed_by']['count'],respon['edge_follow']['count'],respon['edge_owner_to_timeline_media']['count']
            return {
                'followers':followers,'following':following,'postingan':posting
            }
        except Exception as e:
            return {
                'followers':'-1','following':'-1','postingan':'-1'
            }
    