import sqlite3
from hashlib import sha256



# O que esse programa faz na verdade é criar uma senha para cada serviço que vc utiliza e quer uma nova senha.
# O programa faz isso criando uma chave secreta baseado em sua ADMIN_PASSWORD e o nome do serviço que vc bota. Com
# base nessa chave secreta, ele decodifica a combinação chave secreta + ADMIN_PASSWORD + serviço e pega os 15 primeiros
# dígitos dessa hash.
# Toda vez que vc pede a senha pra cada serviço, ele repete todo esse processo. Não todo o processo exatamente, porque
# o programa salva a chave secreta na database e só faz a última hash de novo.


ADMIN_PASSWORD = "Phukyou95369"

connect = input("What is your password?\n")

while connect != ADMIN_PASSWORD:
	connect = input("What is your password?\n")
	if connect == "q":
		break

conn = sqlite3.connect('pass_manager.db')


def create_password(pass_key, service, admin_pass):
	return sha256(admin_pass.encode('utf-8') + service.lower().encode('utf-8') + pass_key.encode('utf-8')).hexdigest()[
	       :15]


def get_hex_key(admin_pass, service):
	return sha256(admin_pass.encode('utf-8') + service.lower().encode('utf-8')).hexdigest()


def get_password(admin_pass, service):
	secret_key = get_hex_key(admin_pass, service)
	cursor = conn.execute("SELECT * from KEYS WHERE PASS_KEY=" + '"' + secret_key + '"')

	file_string = ""
	for row in cursor:
		file_string = row[0]
	return create_password(file_string, service, admin_pass)


def add_password(service, admin_pass):
	secret_key = get_hex_key(admin_pass, service)

	command = 'INSERT INTO KEYS (PASS_KEY) VALUES (%s);' % ('"' + secret_key + '"')
	conn.execute(command)
	conn.commit()
	return create_password(secret_key, service, admin_pass)


if connect == ADMIN_PASSWORD:
	try:
		conn.execute('''CREATE TABLE KEYS
            (PASS_KEY TEXT PRIMARY KEY NOT NULL);''')
		print("Your safe has been created!\nWhat would you like to store in it today?")
	except:
		print("You have a safe, what would you like to do today?")

	while True:
		print("\n" + "*" * 15)
		print("Commands:")
		print("q = quit program")
		print("gp = get password")
		print("sp = store password")
		print("*" * 15)
		input_ = input(":")

		if input_ == "q":
			break
		if input_ == "sp":
			service = input("What is the name of the service?\n")
			print("\n" + service.capitalize() + " password created:\n" + add_password(service, ADMIN_PASSWORD))
		if input_ == "gp":
			service = input("What is the name of the service?\n")
			print("\n" + service.capitalize() + " password:\n" + get_password(ADMIN_PASSWORD, service))


# Se vc vai em 'gp' e digita o nome do serviço errado, vc ainda vai receber uma senha aleatória