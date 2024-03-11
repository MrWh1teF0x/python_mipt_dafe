from base import DataBase
data = DataBase()
while True:

    cmd = input()

    try:
        if cmd == "add":
            nickname, password, mail, birth = input().split()
            data.add_user(nickname, password, mail, birth)
        elif cmd == "del":
            id = int(input())
            data.del_user(id)
        elif cmd == "change":
            id, key, value = input().split()
            data.change_data(int(id), {key: value})
        elif cmd == "info":
            id = int(input())
            data.user_info(id)
        elif cmd == "update":
            id = int(input())
            data.update(id)
    except ValueError as error:
        print(error)