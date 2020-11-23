import os
from flask import Flask,request,redirect,url_for,render_template

from sympy import mod_inverse
import numpy as np

from decimal import Decimal





app = Flask(__name__)

def encryption(entry_message, entry_key):
    
    plain_text = entry_message.lower().split()
    key = entry_key.lower()
    key_length = len(key)
    
    encrypted_message = []
    
    key_n = 0
    for i in plain_text:
        partial_encrypted_message = ""
        for j in i:
            c = (ord(j)+ord(key[key_n])-97)%26
            partial_encrypted_message+=chr(97+c)
            key_n = (key_n+1)%key_length
        encrypted_message.append(partial_encrypted_message)
        
    encrypted_message = " ".join(encrypted_message)
    
    return encrypted_message

def decryption(entry_message, entry_key):
    
    encrypted_message = entry_message.lower().split()
    key = entry_key.lower()
    key_length = len(key)
    
    decrypted_message = []
    
    key_n = 0
    for i in encrypted_message:
        partial_decrypted_message = ""
        for j in i:
            p = (ord(j)-ord(key[key_n])-97)%26
            partial_decrypted_message+=chr(97+p)
            key_n = (key_n+1)%key_length
        decrypted_message.append(partial_decrypted_message)
        
    decrypted_message = " ".join(decrypted_message)

    return encrypted_message


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/affine',methods=['POST','GET'])
def affine():
    if request.method=="POST":
        a,b=request.form['key'].split()
        a,b=int(a),int(b)
        message=request.form['msg']
        if 'encrypt' in request.form:
            choice=1
        else :
            choice=2
        output = ''
        if choice == 1:
            for i in message:
                output += chr(((a * (ord(i) - 97) + b) % 26) + 97)
            return render_template('about.html',result='Encrypted Message is: '+output)
        elif choice == 2:
            for i in message:
                output += chr(((mod_inverse(a, 26) * (ord(i) - 97 - b)) % 26) + 97)
            return render_template('about.html', result='Decrypted Message is: '+output)
    return render_template('about.html', result="")

@app.route('/playfair',methods=['POST','GET'])
def playfair():
    if request.method=="POST":
            key = request.form['key']
            message = request.form['msg'].replace('j', 'i')
            if 'encrypt' in request.form:
                choice=1
            else :
                choice=2

            message = message + 'z' if len(message) % 2 == 1 else message

            pairs = [message[i:i+2] for i in range(0, len(message), 2)]
            alphabets = [alphabet for alphabet in [chr(x) for x in range(97, 123)] if alphabet != 'j']
            arr = np.array([alphabets.pop(alphabets.index(key[x])) for x in range(len(key))] + alphabets).reshape(5, 5)

            output = ''

            if choice == 1:
                for pair in pairs:
                    a = np.array([np.where(arr == pair[0])[0][0], np.where(arr == pair[0])[1][0]])
                    b = np.array([np.where(arr == pair[1])[0][0], np.where(arr == pair[1])[1][0]])
                    if not ((a - b).all()):
                        if np.count_nonzero(a-b == 0) == 1:
                            if a[0] == b[0]:
                                output += arr[a[0], (a[1] + 1) % 5] + arr[b[0], (b[1] + 1) % 5]
                            else:
                                output += arr[(a[0] + 1) % 5, a[1]] + arr[(b[0] + 1) % 5, b[1]]
                        else:
                            output += pair
                    else:
                        output += arr[a[0], b[1]] + arr[b[0], a[1]]
                return render_template('playfair.html', result='Encrypted Message is: '+ output)
            else:
                for pair in pairs:
                    a = np.array([np.where(arr == pair[0])[0][0], np.where(arr == pair[0])[1][0]])
                    b = np.array([np.where(arr == pair[1])[0][0], np.where(arr == pair[1])[1][0]])
                    if not ((a - b).all()):
                        if np.count_nonzero(a-b == 0) == 1:
                            if a[0] == b[0]:
                                output += arr[a[0], (a[1] - 1) % 5] + arr[b[0], (b[1] - 1) % 5]
                            else:
                                output += arr[(a[0] - 1) % 5, a[1]] + arr[(b[0] - 1) % 5, b[1]]
                        else:
                            output += pair
                    else:
                        output += arr[a[0], b[1]] + arr[b[0], a[1]]
                return render_template('playfair.html', result='Decrypted Message is: '+output)
    return render_template('playfair.html', result="")

@app.route('/vigenere',methods=['POST','GET'])
def vigenere():
    if request.method=="POST":
        if 'encrypt' in request.form:
            output=encryption(request.form['msg'], request.form['key'])
            return render_template('vigenere.html', result='Encrypted Message is: '+ output)
        else :
            output=decryption(request.form['msg'], request.form['key'])
            return render_template('vigenere.html', result='Decrypted Message is: '+ output)
    return render_template('vigenere.html', result="")

def gcd(a,b): 
    if b==0: 
        return a 
    else: 
        return gcd(b,a%b) 

@app.route('/rsa',methods=['POST','GET'])
def rsa():
    if request.method=="POST":
    
        p = int(request.form['p']) 
        q = int(request.form['q']) 
        no = int(request.form['msg']) 
        n = p*q 
        t = (p-1)*(q-1) 
        
        for e in range(2,t): 
            if gcd(e,t)== 1: 
                break
        
        
        for i in range(1,10): 
            x = 1 + i*t 
            if x % e == 0: 
                d = int(x/e) 
                break
        ctt = Decimal(0) 
        ctt =pow(no,e) 
        ct = ctt % n 
        
        dtt = Decimal(0) 
        dtt = pow(ct,d) 
        dt = dtt % n 
        
        print('n = '+str(n)+' e = '+str(e)+' t = '+str(t)+' d = '+str(d)+'cipher text = '+str(ct)+' decrypted text = '+str(dt))
        return render_template('rsa.html', result='n = '+str(n)+' e = '+str(e)+' t = '+str(t)+' d = '+str(d)+'cipher text = '+str(ct)+' decrypted text = '+str(dt))

    return render_template('rsa.html', result="")
    


if __name__ =='__main__':
    app.run(debug=True)