import json

def get_amount(username):
    x = None
    if not isinstance(username, int):
        with open("bank.json", 'r') as f:
            bank_values = json.load(f)
        if username not in bank_values:
            print(f"{username} is not in database")
            return False
        return int(bank_values[username][0])
    else:
        with open("bank.json", 'r') as f:
            bank_values = json.load(f)
        for user in bank_values:
            if int(bank_values[user][1]) == int(username):
                x = bank_values[user]
                break
        if x is None:
            print(f"{username} is not in database")
            return False
        return int(x[0])


def change_amount(username, amount):
    x = None
    if not isinstance(username, int):
        with open("bank.json", 'r') as f:
            bank_values = json.load(f)
        if username not in bank_values:
            print("Username is not in database, can't change value")
            return False
        bank_values[username] = [amount, bank_values[username][1]]
        with open("bank.json", 'w') as f:
            json.dump(bank_values, f)
        return True
    else:
        with open("bank.json", 'r') as f:
            bank_values = json.load(f)
        for user in bank_values:
            if bank_values[user][1] == username:
                x = user
        if not x:
            print("Username is not in database, can't change value")
            return False
        bank_values[x] = [amount, bank_values[x][1]]
        with open("bank.json", 'w') as f:
            json.dump(bank_values, f)
        return True


def new_account(username, discord):
    with open("bank.json", 'r') as f:
        bank_values = json.load(f)
        f.close()
    if username in bank_values:
        print("Account already in database")
        return False
    with open("bank.json", 'w') as f:
        bank_values[username] = [0, discord]
        json.dump(bank_values, f)
    print(f"{username}, {discord} has been added to database")
    return True
