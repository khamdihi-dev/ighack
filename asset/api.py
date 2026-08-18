import re,os,uuid,time
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
                header_={  'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'id,en-US;q=0.9,en;q=0.8,ms;q=0.7',
    'dpr': '1',
    'priority': 'u=0, i',
    'sec-ch-prefers-color-scheme': 'light',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
    'viewport-width': '360',
}
                respon = requests.get(f'https://www.instagram.com/{username}/',headers=header_,cookies={'cookie':self.cookie}).text
                open('debug.html','w').write(respon)
                ds_user_id = re.search(r'"target_id":"(\d+)"', str(respon)).group(1)
                if ds_user_id:list_uid.add(ds_user_id)
            except Exception as e:exit(e)
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
        
        except KeyError:
            exit('\n[!] Gunakan cookie yang lain')
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

    def profile_info(self,username,userid):
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
                fallback=self.Instagam_user_info(userid)
                return {
                'followers':fallback[0],'following':fallback[1],'postingan':fallback[2]
            }
        except Exception:

            return {
                'followers':'','following':'','postingan':''
            }
    
    def friends_user_chek(self, username):
        try:
            cookies = {'csrftoken': 'y8uDTfrY7Phu2KUu5A6rH6','datr': 'VmxHapOV3XWD5-rwuV-IsfZF','ig_did': str(uuid.uuid4()).upper(),'mid': 'akdsWQALAAGtTiFKVa7iCE_9hm-x','ig_nrcb': '1','wd': '773x777',}
            headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'id',
                'cache-control': 'max-age=0',
                'dpr': '1',
                'priority': 'u=0, i',
                'sec-ch-prefers-color-scheme': 'light',
                'sec-ch-ua': '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
                'sec-ch-ua-full-version-list': '"Google Chrome";v="149.0.7827.198", "Chromium";v="149.0.7827.198", "Not)A;Brand";v="24.0.0.0"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-model': '""',
                'sec-ch-ua-platform': '"Windows"',
                'sec-ch-ua-platform-version': '"14.0.0"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36',
                'viewport-width': '773',
            }
            response = requests.get(f'https://www.instagram.com/{username}', cookies=cookies, headers=headers).text
            data=re.findall('<meta content="(.*?) Pengikut, (.*?) Mengikuti, (.*?) Postingan',response)[0]
            pengikut,mengikuti,post=data
            return pengikut,mengikuti,post
        except Exception as e:return '','',''

    def Instagram_load(self):
        try:
            headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7','accept-language': 'id,en-US;q=0.9,en;q=0.8,ms;q=0.7','dpr': '1','priority': 'u=0, i','sec-ch-prefers-color-scheme': 'light','sec-ch-ua': '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"','sec-ch-ua-full-version-list': '"Google Chrome";v="149.0.7827.198", "Chromium";v="149.0.7827.198", "Not)A;Brand";v="24.0.0.0"','sec-ch-ua-mobile': '?0','sec-ch-ua-model': '""','sec-ch-ua-platform': '"Windows"','sec-ch-ua-platform-version': '"14.0.0"','sec-fetch-dest': 'document','sec-fetch-mode': 'navigate','sec-fetch-site': 'none','sec-fetch-user': '?1','upgrade-insecure-requests': '1','user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36','viewport-width': '773','cookie': self.cookie}
            response = requests.get('https://www.instagram.com/', headers=headers).text
            av_=re.search('"NON_FACEBOOK_USER_ID":"(.*?)"',response).group(1)
            spin_r=re.search('"__spin_r":(\d+),',response).group(1)
            spin_t=re.search('"__spin_t":(\d+),',response).group(1)
            hsi=re.search('"hsi":"(\d+)"',response).group(1)
            dtsg=re.search('"DTSGInitialData",\[\],{"token":"(.*?)"',response).group(1)
            lsd=re.search('"LSD",\[\],{"token":"(.*?)"',response).group(1)
            haste=re.search('"haste_session":"(.*?)"',response).group(1)
            csrf=re.search('"csrf_token":"(.*?)"',response).group(1)
            return (
                av_,spin_r,spin_t,hsi,dtsg,lsd,haste,csrf
            )
        except Exception as e:
            return (
                '',
                str(int(time.time())),
                str(int(time.time())),
                '7658196461970859807',
                'NAfyvj66eSmTPTxlP1LScFYld206EJKvO0C5rH6KcDnUk1qQqhUX4Vw:17864955220006059:1783062519',
                'lXx1C-NPCQRwo6SoQmwpgV',
                'f55wFgpvrG40rHU4AEA4CzFDsayTvFYU'
            )
    def Instagam_user_info(self, userid):
        try:

            av_,spin_r,spin_t,hsi,dtsg,lsd,haste,csrftoken=self.Instagram_load()
            headers = {
                'accept': '*/*',
                'accept-language': 'id,en-US;q=0.9,en;q=0.8,ms;q=0.7',
                'content-type': 'application/x-www-form-urlencoded',
                'dpr': '1',
                'origin': 'https://www.instagram.com',
                'priority': 'u=1, i',
                'referer': 'https://www.instagram.com/dermagaby_/',
                'sec-ch-prefers-color-scheme': 'light',
                'sec-ch-ua': '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
                'sec-ch-ua-full-version-list': '"Google Chrome";v="149.0.7827.198", "Chromium";v="149.0.7827.198", "Not)A;Brand";v="24.0.0.0"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-model': '""',
                'sec-ch-ua-platform': '"Windows"',
                'sec-ch-ua-platform-version': '"14.0.0"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
                'viewport-width': '773',
                'x-asbd-id': '359341',
                'x-csrftoken': csrftoken,
                'x-fb-friendly-name': 'PolarisProfilePageContentQuery',
                'x-fb-lsd': lsd,
                'x-ig-app-id': '936619743392459',
                'x-ig-max-touch-points': '0',
                'cookie': self.cookie
            }

            data = {
                'av': av_,
                '__user': '0',
                '__a': '1',
                '__req': '1',
                '__hs': haste,
                'dpr': '1',
                '__ccg': 'MODERATE',
                '__rev': spin_r,
                '__s': '4f4an8:ti1yf1:q8fjtg',
                '__hsi': hsi,
                '__dyn': '7xeUjG1mxu1syUbFp41twpUnwgU7SbzEdF8aUco2qwJxS0k24o0B-q1ew6ywaq0yE462mcw5Mx62G5UswoEcE7O2l0Fwqo5W1yw9O1lwxwQzXwae4UaEW2G0AEco5G0zK5o4q0HU1wEbUGdwtUeo9UaQ0Lo6-bwHwKG1pg2fwxyo6O1FwlAcwBwUQp1yU426V8aUuwm8jxK0-8KmUhw4rwXyEcE4y16wAwj83KwRyrg',
                '__csr': 'glMohQQZiNrBOvRO4AqGDRHbRXaaUNkQAiV24_VFG-GpqhGhtaWHhe9y4LHghhfZ6GEx5uGDhoSWSOkAIylrleAibSbA8TiSiVDyqACKJK8HzEWmmup3et4AKUy58_pVKaKbyVrDGpa8gClaGUvxei8xC22ueJKmrRyKAEpAl5ht2uA9AzUCi448S2S4bypGUC4Kq4ECiEWGD-4VpUgxyl6zoSqaxa2y08dweO7o07Ai030K00Mbe08syUeU0tfe0xU1yo6jzU5GdxG1rw39iw5fw11Ou2O8weu1pxok0UrwsO0ywgo0xi0EEg80ct8m9yaCU6N0iFDe0NU2loqa5U0hBQ0gqi01aFw1Pa0eyw3Ro2ro',
                '__hsdp': 'l0NgjOtR1wya88IhrIjpXFPtGPMWu_ByeeAylzQ2Un5h0kDx0AC3G1jZ0pKdwyO0Gg4W6o4p0zymbhoSECcj9DG2S3Si1dxq2O0zUjwsk12zUaFodWwVyoaU622G2C4obUcFEeazK3636dyo4a4Gz9UB0bt06Ywvo0nhw9e3m067E1fE1lU0Mi5o18ovU0xd04uw2DU7G0hOhU8Efo2fw5Qw86E',
                '__hblp': '0gE6G7E7i3-bx5wb-fwhF8G1jCxu78d84aUpwhFRxqGg-azqyomFQEmz8Ciq36i1dxq4EpwICxle36aK4U4C2t0BzES9BwGByUaWxy229wHwj8G8wGwFDyo98G3aq3yF8DwNxC49ES9wgE8FVGgC2ibwv46U4y8U1j89onw_we-0m6581Mo1G82jwRw1xW0GU2iwRwn826wZyo88kwgEeo0Au5o18rxLwhE1P40hW0uO15g6K2u1aDK0OU4OhUSayofo2fw9y3W1uG3G0wqw',
                '__sjsp': 'l0NgjOvR2sdIyy2bpdKNdDKDdSHf3FX-m8Ujylw_40',
                '__comet_req': '7',
                'fb_dtsg': dtsg,
                'jazoest': '26153',
                'lsd': lsd,
                '__spin_r': spin_r,
                '__spin_b': 'trunk',
                '__spin_t': spin_t,
                'fb_api_caller_class': 'RelayModern',
                'fb_api_req_friendly_name': 'PolarisProfilePageContentQuery',
                'server_timestamps': 'true',
                'variables': '{"enable_integrity_filters":true,"id":"'+userid+'","__relay_internal__pv__PolarisCannesGuardianExperienceEnabledrelayprovider":true,"__relay_internal__pv__PolarisCASB976ProfileEnabledrelayprovider":false,"__relay_internal__pv__PolarisWebSchoolsEnabledrelayprovider":false,"__relay_internal__pv__PolarisRepostsConsumptionEnabledrelayprovider":true}',
                'doc_id': '26672929172408668',
            }
            response = requests.post('https://www.instagram.com/api/graphql', headers=headers, data=data).json()['data']['user']
            follower=response['follower_count']
            following_count=response['following_count']
            media_count=response['media_count']
            return follower,following_count,media_count
        except:return '','',''
