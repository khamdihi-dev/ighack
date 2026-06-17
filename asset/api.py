import re,os,uuid
import json
import requests
import base64

dump_list = []


class api:
    def __init__(self, cookie:str):
        self.useragent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Instagram 243.1.0.14.111 (iPhone13,3; iOS 15_5; en_US; en-US; scale=3.00; 1170x2532; 382468104) NW/3'
        self.app_endpoint = 'https://i.instagram.com/api/v1/'
        self.web_endpoint = 'https://www.instagram.com/api/v1/'
        self.web_query_endpoint = 'https://www.instagram.com/graphql/query/'
        self.cookie = cookie

    #  [ Creat Bearer token ]
    def GenerateBearerToken(self):
        try:
            self.userid = re.search('ds_user_id=(\d+)',self.cookie).group(1)
            self.session_token = re.search('sessionid=(.*?);',self.cookie).group(1)
            return base64.b64encode(json.dumps({
                "ds_user_id":self.userid,
                "sessionid":self.session_token
            }).encode()).decode()
        except AttributeError:
            print('[+] Cookie tidak valid..')
            return None
        
    # [ Get userid ]
    def public_userid(self, username:list):
        list_uid = set()
        for username in username:
            try:
                respon = requests.get(f'https://www.instagram.com/{username}/',cookies={'cookie':self.cookie}).text
                ds_user_id = re.search(r'"user_id":"(\d+)"', str(respon)).group(1)
                if ds_user_id:list_uid.add(ds_user_id)
            except:continue
        return list(list_uid)

    # [ Login with cookie ]
    def login(self):
        try:
            self.auth = self.GenerateBearerToken()
            self.uid = re.search(r'ds_user_id=(\d+)',self.cookie).group(1)
            self.respon = requests.get(self.app_endpoint+f'users/{self.uid}/info/',headers={
                'authorization': f'Bearer IGT:2:{self.auth}',
                'x-bloks-version-id': '81fef04dcfc8addef5254d2bc003dda43dcd582c4873d1d14ad8d63ca17e9cdb',
                'x-fb-client-ip': 'True',
                'x-fb-connection-type': 'WIFI',
                'x-fb-friendly-name': f'IgApi: users/{self.uid}/info/',
                'x-fb-request-analytics-tags': '{"network_tags":{"product":"567067343352427","surface":"undefined","request_category":"api","purpose":"fetch","retry_attempt":"0"}}',
                'x-fb-server-cluster': 'True',
                'x-ig-android-id':  f'android-{uuid.uuid4().hex[:16]}',
                'x-ig-app-id': '567067343352427',
                'x-ig-app-locale': 'en_US',
                'x-ig-bandwidth-speed-kbps': '-1.000',
                'x-ig-bandwidth-totalbytes-b': '0',
                'x-ig-bandwidth-totaltime-ms': '0',
                'x-ig-client-endpoint': 'com.bloks.www.caa.login.save-credentials:com.bloks.www.caa.login.save-credentials',
                'x-ig-capabilities': '3brTv10=',
                'x-ig-connection-type': 'WIFI',
                'user-agent': 'Instagram 430.0.0.53.80 Android (32/12; 220dpi; 960x540; OPPO; CPH1912; CPH1912; OPPO; en_US; 974607456)',
                'x-fb-http-engine': 'Tigon/MNS/TCP',
                'x-fb-rmd': 'state=URL_ELIGIBLE',
                'zero-http-network-interface': 'wifi',
            }).json()
            self.nama = self.respon['user']['full_name']
            return {'isvalid':True,'nama':self.nama}
        
        except Exception as e:
            os.remove('data/cookie.txt')
            exit(f'\n[!] {e}')
    
    def dump_users(self,userid,after,mode):
        try:
            self.variabel = 'variables={"id":"%s","first":150,"after":"%s"}'%(userid,after)
            self.params = "query_hash=58712303d941c6855d4e888c5f0cd22f&{}".format(self.variabel) if not mode else "query_hash=37479f2b8209594dde7facb0d904896a&{}".format(self.variabel)
            self.respon = requests.get(self.web_query_endpoint,params=self.params,
                                       headers={"user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36","accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7","cookie": self.cookie}).json()
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
            self.head = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7','accept-language': 'id,en-US;q=0.9,en;q=0.8,ms;q=0.7','cache-control': 'max-age=0','dpr': '1','priority': 'u=0, i','sec-ch-prefers-color-scheme': 'light','sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"','sec-ch-ua-full-version-list': '"Chromium";v="146.0.7680.178", "Not-A.Brand";v="24.0.0.0", "Google Chrome";v="146.0.7680.178"','sec-ch-ua-mobile': '?1','sec-ch-ua-model': '"Pixel 6"','sec-ch-ua-platform': '"Android"','sec-ch-ua-platform-version': '"12"','sec-fetch-dest': 'document','sec-fetch-mode': 'navigate','sec-fetch-site': 'none','sec-fetch-user': '?1','upgrade-insecure-requests': '1','sec-fetch-site': 'none','user-agent':'Mozilla/5.0 (Linux; Android 13; SM-A346M Build/TP1A.220624.014; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/144.0.7559.87 Mobile Safari/537.36 Instagram 413.0.0.41.84 Android (33/13; 401dpi; 1080x2340; samsung; SM-A346M; a34x; mt6877; pt_BR; 865356678; IABMV/1)'}
            if self.cookie:self.head.update({'cookie':self.cookie})
            respon1 = requests.get(f'https://www.instagram.com/api/v1/users/web_profile_info/?username={username}', headers=self.head)
            if respon1.status_code == 200:
                respon = respon1.json()['data']['user']
                followers,following,posting = respon['edge_followed_by']['count'],respon['edge_follow']['count'],respon['edge_owner_to_timeline_media']['count']
                return {
                    'followers':followers,'following':following,'postingan':posting
                }
            else:
                return {
                'followers':'','following':'','postingan':''
            }
        except Exception:

            return {
                'followers':'','following':'','postingan':''
            }
    
    def friends_user_chek(self, username):
        try:
            self.head = {'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Instagram 243.1.0.14.111 (iPhone13,3; iOS 15_5; en_US; en-US; scale=3.00; 1170x2532; 382468104) NW/3',}
           
            self.head.update({'Host': 'www.instagram.com','cache-control': 'max-age=0','upgrade-insecure-requests': '1','accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7','sec-fetch-site': 'none'})
            req = requests.get(f'https://www.instagram.com/api/v1/users/web_profile_info/?username={username}', headers=self.head).json()['data']['user']
            ikut,mengikut = req['edge_followed_by']['count'],req['edge_follow']['count']
            return(ikut,mengikut)
        except Exception as e:return('',e)
    
