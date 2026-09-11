import random
import string
import json
from pathlib import Path


class Bank:
    database = 'data.json'
    data = []

    try:
        if Path(database).exists():
            with open(database) as fs:
                data = json.loads(fs.read())
        else:
            print(f" no such file exists: {database}")
    except Exception as err:
        print(f"There is an error as {err}")

    @classmethod
    def __update(cls):
        with open(cls.database, 'w') as fs:
            fs.write(json.dumps(cls.data)) 

    @classmethod
    def __accountgenerate(cls): 
        alpha = random.choices(string.ascii_letters, k= 3)
        num = random.choices(string.digits, k= 3)
        spchar = random.choices("!@#$&*%^", k= 1)
        id = alpha + num + spchar
        random.shuffle(id)
        return "".join(id)


    def Createaccount(self):
        info = {
            "name": input("Enter your name: "),
            "age": int(input("Enter your age: ")),
            "email": input("Enter your email: "),
            "pin": int(input("Enter your 4 number pin: ")),
            "account number": Bank.__accountgenerate(),
            "balance": 0
        }

        if info['age'] < 18 or len(str(info['pin'])) !=4:
            print("Sorry you can't create your account")
        else:
            print("\nYour account has been created successfully!") 
            for i in info:
                print(f"{i} : {info[i]}")
            print("Please remember your account number ")

            Bank.data.append(info)

            Bank.__update()     

    def depositmoney(self):
        accnumber = input("Enter your account number: ")
        pin = int(input("Please enter your pin: "))

        userdata = [i for i in Bank.data if i['account number'] == accnumber and i ['pin'] == pin]

        if not userdata:  
            print("Sorry no data found or incorrect PIN")

        else:
            amount = int(input("How much money do you want to deposit? ")) 
            if amount > 15000 or amount < 0:
              print("Transaction Failed: Deposit amount must be between 1 and 15,000 PKR.")

            else:
                # print(userdata)
                userdata[0] ['balance'] += amount
                Bank.__update()
                print(f"Amount deposited successfully!\nNew Balance is: {userdata[0]['balance']}")

    def withdrawmoney(self):
            accnumber = input("Enter your account number: ")
            pin = int(input("Please enter your pin: "))
    
            userdata = [i for i in Bank.data if i['account number'] == accnumber and i ['pin'] == pin]
    
            if not userdata:  
                print("[ERROR] Account not found. Please verify your Account Number and PIN.")
    
            else:
                amount = int(input("How much money do you want to withdraw? ")) 
                if userdata[0] ['balance'] < amount:
                  print("Sorry! you don't have that much money.")
    
                else:
                    # print(userdata)
                    userdata[0] ['balance'] -= amount
                    Bank.__update()
                    print(f"Transaction Successful: {amount:,} PKR withdrawn.\nRemaining Balance: {userdata[0]['balance']:,} PKR")    

    def showdetails(self):
        accnumber = input("Enter your account number: ")
        pin = int(input("Please enter your pin: "))
            
        userdata = [i for i in Bank.data if i['account number'] == accnumber and i ['pin'] == pin]

        print("\nYour account informations are:\n")
        for i in userdata[0]:
            print(f"{i} : {userdata[0][i]}")

    def updatedetails(self):
                accnumber = input("Enter your account number: ")
                pin = int(input("Please enter your pin: "))
                         
                userdata = [i for i in Bank.data if i['account number'] == accnumber and i ['pin'] == pin]   

                if not userdata:
                    print("[ERROR] Account not found. Please verify your Account Number and PIN.")
                else:
                    print("\nNote: Age, Account Number, and Balance cannot be modified.")
                    print("Enter new details below, or press Enter to skip.\n")

                    newdata = {
                        "name": input("Enter a new name or press enter to skip: "),
                        "email":input("Enter a new email or press enter to skip: "),
                        "pin": input("Enter a new pin or press enter to skip: ")
                    }

                    if newdata["name"] == "":
                        newdata["name"] = userdata[0]['name']

                    if newdata["email"] == "":
                        newdata["email"] = userdata[0]['email']

                    if newdata["pin"] == "":
                        newdata["pin"] = userdata[0]['pin']

                    newdata['age'] = userdata[0]['age']
                    newdata['account number'] = userdata[0]['account number']
                    newdata['balance'] = userdata[0]['balance']

                    if type(newdata['pin']) == str:
                        newdata['pin'] = int(newdata['pin'])

                    for i in newdata:
                        if newdata[i] == userdata[0][i]:
                            continue
                        else:
                            userdata[0][i] = newdata[i]

                    Bank.__update()
                    print("Details updated successfully! ")   

    def Delete(self):
        accnumber = input("Enter your account number: ")
        pin = int(input("Please enter your pin: "))

        userdata = [i for i in Bank.data if i['account number'] == accnumber and i ['pin'] == pin] 

        if not userdata:
            print("[ERROR] Account not found. Please verify your Account Number and PIN.")

        else:
            confirm = input("Are you sure you want to permanently delete this account? (Y/N): ").strip().upper()

            if confirm == 'Y':
                Bank.data.remove(userdata[0])  
                Bank.__update()
                print("Your account has been permanently deleted.")
            else:
                print("Account deletion request cancelled.")

                # Bank .__update()
                    
    
user = Bank()    

print("Press 1 for Account Creation ")
print("Press 2 for deposit money ")
print("Press 3 for withdraw money ")
print("Press 4 for details of account ")
print("press 5 for updating account ")
print("Press 6 for deleting account ")

check = int(input("Enter your choice: "))

if check == 1:
    user.Createaccount()

if check == 2:
    user.depositmoney() 

if check == 3:
    user.withdrawmoney()    

if check == 4:
    user.showdetails()

if check == 5:
    user.updatedetails()   

if check == 6:
    user.Delete()     