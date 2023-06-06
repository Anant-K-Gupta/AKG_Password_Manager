#PASSWORD MANAGER


import pickle
from tabulate import tabulate
from faker import Faker
from datetime import datetime, timedelta
import os


fake=Faker()
auth=False
name=''
file=''
p=[[1,'View all passwords'],[2,'Search for specific account'],[3, 'Add Account'],[4, 'Change Master Password'],[5, 'Remove an Account'],[6, 'Update'],[7, 'Backup'],[8, 'Exit']]
q=[[1,'Sign-in'], [2, 'Add new Account'], [3, 'Remove Account'], [4, 'Help']]
r=[[1,'Software Overview'], [2, 'How to use']]
printiboy1=tabulate(p, headers=['Number','Task'], tablefmt='fancy_grid')
printiboy2=tabulate(q, headers=['Number','Task'], tablefmt='fancy_grid')
printiboy3=tabulate(r, headers=['Number','Task'], tablefmt='fancy_grid')


#HELP
def helpuser():
    print(printiboy3)
    what=int(input('Enter an option from 1 to 2: '))
    if what==1:
        print('''Welcome to AKG Password Manager!
This software was created by Anant K. Gupta, a student of class XII-A at Modern School Vasant Vihar.
The password manager does the following for you:
- Safely encrypts all your passwords and stroes them for you.
- Has multi-user capabilties.
- Suggests very strong password.
''')
    elif what==2:
        print('''User Manual
-Account Type: This could be anything like work, social, bank etc. If account type is bank, the password will expire 3 months after entry.
-Password Entry: You can use your own password but the system will assess its strength and recommend you strong password if it feels it is required. You can accept or refuse by writing yes or no.
-Entering 404 in the main menu will erase all you account details.
''')

        
#READER
def read():
    f=open('akgpswd.dat','rb')
    record=[]
    while True:
        try:
            rec=pickle.load(f)
            if rec[0]==name:
                rec[4]=decrypt(rec[4])
                del rec[0] 
                record.append(rec)
        except EOFError:
            break
    table=tabulate(record, headers=['TYPE','NAME','USER ID','PASSWORD', '2FA', 'EXPIRY'], tablefmt='fancy_grid')
    print(table)
    f.close()


#WRITER
def write():
    f=open('akgpswd.dat','ab')
    rec=[]
    acc_typ=input('Enter account type: ')
    account=input('Enter account name: ')
    user_id=input('Enter User Id: ')
    sug=fake.password()
    pswd=input('Enter Password: ')
    if strength(pswd)<10:
        so=input('your password is a little weak, whould you rather use this - '+ sug+ '(yes/no): ')
        if so =='yes' or so=='Yes':
            pswd=sug
    pswd=encrypt(pswd)
    fa=input('Enter status of 2FA: ')
    exp='never'
    if acc_typ=='Bank' or acc_typ=='bank':
        exp=datetime.today() + timedelta(90)
        exp=exp.strftime("%d-%m-%y")    
    data=[name, acc_typ, account, user_id, pswd, fa, exp]
    pickle.dump(data, f)
    f.close()


#SEARCH
def search():
    f=open('akgpswd.dat','rb')
    a = input('enter account name: ')
    record=[]
    while True:
        try:
            rec=pickle.load(f)
            if rec[0]==name:
                if rec[2]==a:
                    rec[4]=decrypt(rec[4])
                    del rec[0]
                    record.append(rec) 
        except EOFError:
            break
    if len(record)>0:
        table=tabulate(record, headers=['TYPE','NAME','USER ID','PASSWORD', '2FA', 'EXPIRY'], tablefmt='fancy_grid')
        print(table)
    else:
        print('No such record found.')
    f.close()

    
#ENCRYPTER
def encrypt(a):
    a=a[::-1]
    enc=''
    for i in a:
        b=ord(i)+5
        enc+=chr(b)
    return enc


#DECRYPTER
def decrypt(a):
    dec=''
    for i in a:
        b=ord(i)-5
        dec+=chr(b)
    dec=dec[::-1]
    return dec


#MASTER PASSWORD CHANGER
def change():
    f=open('user.dat','rb')
    while True:
        try:
            rec=pickle.load(f)
            if rec[0]==name:          
                mpswd=rec[1]
                mpswd=decrypt(mpswd)
                break
        except EOFError:
            break
    f.close()
    
    p=input('enter current master password: ')
    if p==mpswd:
        n=input('enter new master password: ')
        n2=input('enter new master password again: ')
        if n==n2:
            n=encrypt(n)
            data=[]
            f=open('user.dat','rb')
            while True:
                try:
                    rec=pickle.load(f)
                    if rec[0]==name:          
                        rec[1]==n
                        data.append([name,n])
                    else:
                        data.append(rec)
                except EOFError:
                    break
            f.close()
            f=open('user.dat','wb')
            for i in data:
                pickle.dump(i,f)
            f.close()
            print('Master Password updated')
        else:
            print('Please try again.') 
    else:
        print('That is incorrect!')


#CHECK STRENGHT OF PASSWORD
def strength(pswd):
    c=0
    u=0
    l=0
    for i in pswd:
        if i.isupper():
            u=1
        if i.islower():
            l=1
        if i in '''<>?:"'}{[]\|=+-_/.,`~!@#$%^&*()''' :
            c+=1
        if i.isdigit():
            n=1
        c+=1
    points=c+u+l
    return points
            
#REMOVER
def remove():
    f=open('akgpswd.dat', 'rb')
    a=input('enter account name: ')
    u=input('enter user id: ')
    newrec=[]
    found=0
    while True:
        try:  
            rec=pickle.load(f)
            if rec[2]==a and rec[3]==u:
                print('record deleted')
                found=1  
            else:   
                newrec.append(rec)
        except EOFError:
            break
    if found==0:
        print('record not found')
    f=open('akgpswd.dat', 'wb')
    for i in newrec:
        pickle.dump(i,f)
    f.close()

#UPDATER
def update():
    f=open('akgpswd.dat', 'rb')
    a=input('enter account name: ')
    u=input('enter user id: ')
    newrec=[]
    found=0
    while True:
        try:  
            rec=pickle.load(f)
            if rec[2]==a and rec[3]==u:
                pswd=input('enter new password: ')
                rec[4]=encrypt(pswd)
                newrec.append(rec)
                print('record updated')
                found=1
            else:
                newrec.append(rec)
        except EOFError:
            break
    f.close()
    if found==0:
        print('record not found')
    f=open('akgpswd.dat', 'wb')
    for i in newrec:
        pickle.dump(i,f)
    f.close()
    
#DELETE DATABSE
def error404():
    f=open('akgpswd.dat','rb')
    data=[]
    while True:
        try:
            rec=pickle.load(f)
            if rec[0]!=name:
                data.append(rec)
        except EOFError:
            break
    f.close()
    f=open('akgpswd.dat','wb')
    for i in data:
        pickle.dump(i,f)
    f.close()
    
#BACKUP DATA
def backup():
    f=open('akgpswd.dat','rb')
    data=[]
    global file
    while True:
        try:
            rec=pickle.load(f)
            if rec[0]==name:
                data.append(rec)
        except EOFError:
            break
    f.close()
    fname=input('What would you like the file name to be?: ')
    floc=input('Where would you like to save the file?: ')
    file=floc+'\\'+fname+'.dat'
    print(file)
    f=open(file,'wb')
    for i in data:
        pickle.dump(i,f)
    f.close()

    
#CHECK USER(MASTER PASSWORD INPUT)
def signin():
    global auth
    global name
    mpswd=''
    f=open('user.dat','rb')
    name=input('Enter User name: ')
    while True:
        try:
            rec=pickle.load(f)
            if rec[0]==name:          
                mpswd=rec[1]
                mpswd=decrypt(mpswd)
                break
        except EOFError:
            break
    f.close()
    for i in range(1,6):
        p=input('enter master password: ')
        print()
        if p==mpswd:
            auth=True
            
            break
        if i==5:
            error404()
            break
        else:
            print('You have ',5-i,'tries left, if you fail to provide password all your data will be deleted.')
            host=False

        
#ADD USER
def adduser():
    global auth
    global name
    name=input('Enter User name: ')
    mpswd=input('Enter your master password: ')
    mpswd=encrypt(mpswd)
    f=open('user.dat','ab')
    rec=[name,mpswd]
    pickle.dump(rec,f)
    f.close()
    auth=True


#REMOVE USER
def removeuser():
    global auth
    global name
    mpswd=''
    f=open('user.dat','rb')
    name=input('Enter User name: ')
    while True:
        try:
            rec=pickle.load(f)
            if rec[0]==name:          
                mpswd=rec[1]
                mpswd=decrypt(mpswd)
                break
        except EOFError:
            break
    f.seek(0)
    sure=input('Are you sure you want to remove all data(yes/no): ')
    if sure=='yes' or sure=='Yes': 
        p=input('enter master password: ')
        if p==mpswd:
            error404()
            data=[]
            while True:
                try:
                    rec=pickle.load(f)
                    if rec[0]!=name:          
                        data.append(rec)
                except EOFError:
                    break
            f=open('user.dat','wb')
            for i in data:
                pickle.dump(i,f)
            f.close()                     
        else:
            print('The password is incorrect!!!')
    else:
        print('Phew! That was close! Your data is still with us.')

        
#MAIN LOOP
def main():
    while True:
        print(printiboy1)
        what=int(input('Enter an option from 1 to 7: '))
        if what==1:
            read()
        elif what==2:
            search()
        elif what==3:
            write()
        elif what==4:
            change()
        elif what==5:
            remove()
        elif what==6:
            update()
        elif what==7:
            backup()
        elif what==8:
            break
        elif what==404:
            error404()

def start_up():
    print(printiboy2)
    what=int(input('Enter an option from 1 to 4: '))
    while True:
            
        if what==1:
            signin()
            break
        elif what==2:
            adduser()
            break
        elif what==3:
            removeuser()
            break
        elif what==4:
            helpuser()
        print(printiboy2)
        what=int(input('Enter an option from 1 to 4: '))
start_up()
if auth:
    main()












    
