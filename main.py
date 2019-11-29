import sqlite3
from hashlib import sha256



# master_password = "12345"
#
# connect = input("Password: \n")
#
# while connect != master_password:
# 	connect = input("Password: \n")


conn = sqlite3.connect('database.db')
c = conn.cursor()

# # Create table
# c.execute('''CREATE TABLE stocks
# (date text, trans text, symbol text, qty real, price real)''')
#
# # Insert a row of data
# c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")
#
# # Commit the changes
# conn.commit()
#
# # Close the connection
# c.close()
# conn.close()


password = input("Type a password: ")
bpassword = password.encode('utf-8') # Encode transforms our string into bytes, equivalent to bpassword = (b"string")
enc_pass = sha256(bpassword) # enc_pass = sha256(b"password")
print(bpassword)
print(enc_pass.digest())
print(enc_pass.hexdigest())


