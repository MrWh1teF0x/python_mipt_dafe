def check_comand(user_comand: str, comands: list[str]) -> bool:
    flag = 0
    for comand in comands:
        f = False
        for a in comand:
            for i in range(len(user_comand)):
                uc = list(user_comand)
                uc[i] = a
                if ''.join(uc) == comand:
                    f = True
                    break
            for i in range(len(user_comand)+1):
                uc = list(user_comand)
                uc.insert(i, a)
                if ''.join(uc) == comand:
                    f = True
                    break
            for i in range(len(user_comand)):
                uc = list(user_comand)
                del uc[i]
                if ''.join(uc) == comand:
                    f = True
                    break
        flag += f
    if flag == 1:
        return True
    return False

print(check_comand('gt', ['cd', 'ls', 'git']) )
print(check_comand('gt', ['cd', 'ls', 'git', 'get']))
