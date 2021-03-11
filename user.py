import mysql.connector

#connecting to the database
cnx = mysql.connector.connect(user = 'root', password = 'password', host = '127.0.0.1', database = 'fortysevyn')
cursor = cnx.cursor()

#creating user class, it holds all functions for each account
class User:
    #defining attribute user name and password which will be used for logins
    def __init__(self, uname, passw):
        self.uname = uname
        self.passw = passw
    
    #deposit method to increase the balance of the user in the database
    def deposit(self, amt):
        dep = (f'update Users set balance = balance + {amt} where userName = \'{self.uname}\'')
        cursor.execute(dep)
        cnx.commit()
    
    #withdraw method to decrease balance of the user in the database
    def withdraw(self, amt):
        wd = (f'update Users set balance = balance - {amt} where username = \'{self.uname}\'')
        cursor.execute(wd)
        cnx.commit()

    #transfer method to decrease from the logged in user and add to a user with the given account number in the database
    def transfer(self, amt, acct_n):
        #calls the withdraw method for subtracting from user in the database
        self.withdraw(amt)
        trans = (f'update Users set balance = balance + {amt} where accountNumber = \'{acct_n}\'')
        cursor.execute(trans)
        cnx.commit()

    #change password method to change user password in the database
    def change_passw(self, new_passw):
        c_pass = (f'update Users set password = \'{new_passw}\' where userName = \'{self.uname}\'')
        cursor.execute(c_pass)
        cnx.commit()

    #check balance method to display user balance from database
    def balance (self):
        bal = (f'select balance from Users where userName = \'{self.uname}\'')
        cursor.execute(bal)

        self.lst = cursor.fetchone()
        for x in self.lst:
            return x