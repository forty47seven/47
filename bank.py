#imports functionalities from user.py
from user import User
#imports mysql
import mysql.connector

#connects to database
cnx = mysql.connector.connect(user = 'root', password = 'password', host = '127.0.0.1', database = 'fortysevyn')
cursor = cnx.cursor()

print ('Hello, Welcome')

#Intializes tries which increases in the while loop to limit tries to 3
tries = 0
while tries < 3:
    #takes users user name and password
    un = input ('Enter User Name: ')
    pas = input ('Enter Password: ')

    #checks for password that matches the provided user name in database
    find = (f'select password from Users where userName = \'{un}\'')
    cursor.execute(find)
    lst = cursor.fetchone()
    
    #assigns the password from the database to variable 'pw' if it exists
    if lst is None:
        pw = 1
    else:
        for x in lst:
            pw = x
    
    #gives an 'ok' if password found in the database matches the provided password
    check = 'not ok'
    if pas == pw:
        check = 'ok'
        #set tries = 3 so the prosses does not repeat because of the while loop up top
        tries = 3
    

    if check == 'ok':
        #creates a user with functionalities from user.py
        guy = User(un, pas)
        
        #requests input to choose know user action
        checker = int(input ('Enter\n     1 for Deposit\n     2 for Withdrawal\n     3 for Transfer\n     4 for Balance Check\n     5 for Password Change\n     0 to exit\n'))

        #sets default for variable'go'
        go = 'y'
        #loops while checker is not '0' which means exit and go = y which means user wants to perform an action
        while checker != 0 and go == 'y':
            #1 is for deposit
            if checker == 1:
                #request for deposit amount
                amt = int(input('Enter Amount: '))

                #checks if deposit amount is greater than zero
                if amt > 0:
                    #calls deposit method fron user.py
                    guy.deposit(amt)
                else:
                    #if deposit amt is less than or equal to zero
                    print ('Invalid Entry')
                #takes new value for 'go' and sets it to lowercase
                go = input('Do you want to perform another transaction? (y for YES, n for NO): ').lower()
            
            #2 for withdraw
            elif checker == 2:
                amt = int(input('Enter Amount: '))

                #check if withdraw amount is greater than zero
                if amt > 0:
                    #calls balance method from user.py and set equal to variable 'bal'
                    bal = int(guy.balance())
                    #check that withdraw amount is not less than balance
                    if amt <= bal:
                        guy.withdraw(amt)
                    else:
                        print ('Insufficient Funds')
                else:
                    print ('Invalid Entry')
                ##takes new value for 'go' and sets it to lowercase
                go = input('Do you want to perform another transaction? (y for YES, n for NO): ').lower()

            #3 for transfer
            elif checker == 3:
                #requests for account number of reciepient and amount to be transfered
                a_number = input('Enter Account Number: ')
                amt = int(input('Enter Amount: '))

                #checks for account number in database
                acct_nums = (f'select userName from Users where accountNumber = \'{a_number}\'')
                cursor.execute(acct_nums)
                #assign username to variable 'usr'
                usr = cursor.fetchone()

                #check if account number by having a user name that coresponds to provided account number
                if usr is None:
                    print ('Invalid Account Number')
                elif amt <= 0:
                    print ('Invalid Amount')
                else:
                    #calls balance method from user.py and compare with transfer amount before transfer, ouput 'insufficient funds' if less
                    bal = guy.balance()
                    if amt <= bal:
                        guy.transfer(amt, a_number)
                    else:
                        print('Insufficient Funds')

                #takes new value for 'go' and sets it to lowercase
                go = input('Do you want to perform another transaction? (y for YES, n for NO): ')

            #4 for balance
            elif checker == 4:
                #calls balance method from user.py
                print(guy.balance())
                #takes new value for 'go' and sets it to lowercase
                go = input('Do you want to perform another transaction? (y for YES, n for NO): ').lower()

            #5 for password change
            elif checker == 5:
                #*check for same password
                #Requests for new password twice for confirmation
                pass1 = input('Enter new password: ')
                pass2 = input('Enter password again: ')
                
                #Initializes error as zero, and repeat password request twice if passwords don't match
                error = 0
                while pass1 != pass2 and error != 2:
                    print ('New passwords don\'t match, try again')
                    pass1 = input('Enter new password: ')
                    pass2 = input('Enter password again: ')

                    #icreases variable 'error' to limit tries
                    error += 1
                
                #calls change password method from user.py
                if pass2 == pass1:
                    guy.change_passw(pass1)

                ##takes new value for variable 'go' and sets it to lowercase
                go = input(('Do you want to perform another Action? (y for YES, n for NO): ')).lower()

            #for wrong entry, anything not 1, 2, 3, 4, 5 or 0
            else:
                print ('Wrong entry, try again')
            
            #check for values of 'go' variable for response
            if go == 'y':
                checker = int(input ('Enter\n     1 for Deposit\n     2 for Withdrawal\n     3 for Transfer\n     4 for Balance Check\n     5 for Password Change\n     0 to exit\n'))
            elif go == 'n':
                print ('Goodbye')
            else:
                print('Invalid Input, Goodbye')

    #checks the valuse of variable 'tries' and report the number of tries left
    elif tries == 0:
        print('Wrong Username or Password\nTry Again(2 tries left)')
    
    elif tries == 1:
        print('Wrong Username or Password\nTry Again(1 try left)')

    else:
        print('Goodbye, Three tries exceeded')

    #increses the value of variable 'tries'
    tries += 1

#closes connection to database
cursor.close()
cnx.close()