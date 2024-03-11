from datetime import datetime
from string import punctuation

class User:
    def __init__(self, nickname, password, birth, last_action, mail) -> None:
        self.nickname = nickname
        self.email = mail
        self.birth = birth
        self.password = password
        self.last_action = datetime.today().strftime('%Y-%m-%d')

    def update_action(self):
        self.last_action = datetime.today().strftime('%Y-%m-%d')

    def get_info(self):
        self.update_action()

        return f'Nick = {self.nickname} \n' \
               f'Mail = {self.mail} \n' \
               f'Birth = {self.birth}' \
               f'Last action = {self.last_action}'
class DataBase:
    def __init__(self):
        self.data = {}
        self.nicknames = set()
    
    def check_nickname(self, nickname):
        if nickname.lower() in self.nicknames:
            raise ValueError
        
        if (not 2 <= len(nickname) <= 10):
            raise ValueError("wrong size")
        
        if nickname[0].isdigit() or \
        not (nickname.isalnum() and nickname.isascii()):
            raise ValueError("invalid user")
            
    def check_password(self, password):
        if not password.isascii() \
        or " " in password:
            raise ValueError("invalid password")
        
        upper = False
        digit = False
        lower = False
        punct = False

        for char in password:
            if char.ascii():
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
        
        if upper + digit + lower + punct == 4:
            raise ValueError("invalid password")
        
        if len(password) < 8:
            raise("invalid password")

    def check_mail(self, mail):
        if mail[-13:] != "@phystech.edu":
            raise ValueError("MAI detection")
        
        if mail.count('@') != 1:
            raise ValueError("invalid mail")
        
        if mail in self.mails:
            raise ValueError("not unique mail")
        
    def check_birth(self, birth):
        today = datetime.today().strftime("%Y-%m-%d")

        if (today - birth) / 365 < 18:
            raise ValueError("too young")


    def add_user(self, nickname, birth, password, mail):
        birth = datetime.strptime(birth, "%Y-'%m-%d")

        self.check_nickname()
        self.check_password()
        self.check_birth()
        self.check_mail()

        self.mails.add()
        self.nicknames.add()

        self.data.append(User(nickname, password, mail, birth))

    def del_user(self, id):
        self.data[id] = None

    def user_info(self):
        pass

    def change_data(self):
        pass

    def update(self):
        pass

