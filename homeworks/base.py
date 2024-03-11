from datetime import datetime
from string import punctuation

class User:
    def __init__(self, nickname, password, mail, birth) -> None:
        self.nickname = nickname
        self.mail = mail
        self.birth = birth
        self.password = password
        self.last_action = datetime.today().strftime('%Y-%m-%d')

    def update_action(self):
        self.last_action = datetime.today().strftime('%Y-%m-%d')
    
    def get_info(self):
        print(  f'Nickname = {self.nickname} \n' \
                f'Mail = {self.mail} \n' \
                f'Birth = {self.birth} \n' \
                f'Last action = {self.last_action}')
        
        self.update_action()

class DataBase:
    def __init__(self):
        self.data = []
        self.nicknames = set()
        self.mails = set()
    
    def check_nickname(self, nickname: str):
        if nickname.lower() in self.nicknames:
            raise ValueError("not unique nickname")
        
        if not (2 <= len(nickname) <= 10): 
            raise ValueError("wrong size")

        if nickname[0].isdigit() or \
           not (nickname.isalnum() and nickname.isascii()):
            raise ValueError("invalid user")
        
    def check_password(self, password: str):
        upper = False
        digit = False
        lower = False
        punct = False

        for char in password:
            if char.isascii():    
                if char.isupper():
                    upper = True
                elif char.islower():
                    lower = True
                elif char.isdigit():
                    digit = True
                elif char in punctuation:
                    punct = True
                else:
                    raise ValueError("invalid password")
            else:
                raise ValueError("invalid password")
            
        if not (upper and digit and lower and punct):
            raise ValueError("invalid password")
        
        if len(password) < 8:
            raise ValueError("invalid password")
        
    def check_mail(self, mail):        
        if mail[-13:] != "@phystech.edu":
            raise ValueError("MAI detection")
        
        if mail.count("@") != 1:
            raise ValueError("invalid mail")
        
        if mail in self.mails:
            raise ValueError("not unique mail")
        
    def check_birth(self, birth):
        today = datetime.today().date()

        if (today - birth).days / 365 < 18:
            raise ValueError("too young")

    def add_user(self, nickname, password, mail, birth):
        birth = datetime.strptime(birth, '%Y-%m-%d').date()
        
        self.check_nickname(nickname)
        self.check_birth(birth)
        self.check_mail(mail)
        self.check_password(password)

        self.mails.add(mail)
        self.nicknames.add(nickname)

        self.data.append(User(nickname, password, mail, birth))
        print(len(self.data))

    def del_user(self, id):
        self.data[id] = None

    def user_info(self, id):
        print(self.data)
        self.data[id].get_info()

    def change_data(self, id, changes):
        user = self.data[id]
        for key, value in changes.items():
            if key == 'nickname':
                self.check_nickname(value)
                self.nicknames.remove(user.nickname)

                user.nickname = value
                self.nicknames.add(value)
            elif key == 'password':
                self.check_password(value)
                user.password = value
            elif key == 'mail':
                self.check_mail(value)
                self.mails.remove(user.mail)

                self.user.mail = value
                self.mails.add(value)
    
        self.data[id] = user

        self.update(id)

    def update(self, id):
        self.data[id].update_action()