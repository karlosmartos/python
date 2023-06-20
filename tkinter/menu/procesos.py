import sys
import paramiko
import os
import os.path
import time
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from base64 import b64encode, b64decode
import os
from Crypto.Cipher import Salsa20

ip =   "10.84.44.8" # ip de la maquina asignada

user = "bscs01" # Usuario de la maquina asignada

llave='uVonTKesjZ2hOC5MzgFV/L3IO3wZzxTjpsVnzU8Szsc=' # llave encriptada de la maquina a la que se conectara

# cambiar ruta en duro por la ruta en donde se encuentra el archivo opciones.py 
def val_archivo(opcion, passmaquina):

    client = paramiko.SSHClient()

    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    client.connect(ip, username=user, password=passmaquina, timeout= 10)

    stdin, stdout, stderr = client.exec_command("cd /BSCS_RATING/bscs01/prod/WORK/BILLING_TOOLS/MENUFACT/ ; python opcion.py "+str(opcion))

    tarea = stdout.readlines()

    tarea = tarea[1].rstrip("\n")

    stdin2, stdout2, stderr2 = client.exec_command(" ps -fea | grep " + str(tarea) +" | wc -l")

    lines = stdout2.readlines()

    conteo=lines[0].rstrip("\n")
    
    client.close()

    return (int(conteo))


# cambiar ruta en duro por la ruta en donde se encuentra el archivo  opciones.py 
def ejecucion(opcion, data, keymachine):

    print("Entre en la ejecucion")

    client = paramiko.SSHClient()

    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    client.connect(ip, username=user, password=keymachine, timeout=10)

    stdin, stdout, stferr = client.exec_command("cd /BSCS_RATING/bscs01/prod/WORK/BILLING_TOOLS/MENUFACT/ ; python opcion.py "+str(opcion))

    lines = stdout.readlines()
    print(lines)
    instruccion = ''

    contador = 0

    for comando in lines:

        if (contador == 0):

            instruccion = comando
        
        contador= contador+1
    
    instruccion = instruccion.rstrip("\n")

    for parametro in data:
    
        instruccion = instruccion+' '+parametro
    
    stdin2, stdout2, stferr2 = client.exec_command(instruccion)

    respuesta = stdout2.readlines() 

    respuestafinal = ''

    for resp in respuesta:

        respuestafinal = respuestafinal + resp

    client.close()

    return str(respuestafinal) 


#Desencriptacion de credencial ingresada al sistema

def revelar(path):

    file_in = open(path, "rb")

    nonce, tag, ciphertext = [ file_in.read(x) for x in (16, 16 , -1) ]

    key = str.encode(llave)

    key = b64decode(key)

    cipher = AES.new(key, AES.MODE_EAX, nonce)

    data = cipher.decrypt_and_verify(ciphertext, tag)

    return data.decode('utf-8')

#recuperar opcines de proceso para la ejecucion
# cambiar ruta en duro por la ruta en donde se encuentra el archivo menu.py
def recuperar_menu(listoption, key):
    machinepassword =key

    client = paramiko.SSHClient()

    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    client.connect(ip, username=user, password=machinepassword,timeout=10)

    stdin, stdout, stderr = client.exec_command("cd /BSCS_RATING/bscs01/prod/WORK/BILLING_TOOLS/MENUFACT/; python menu.py")

    lines = stdout.readlines()

    for line in lines:

        listoption.append(line)

    client.close()

    return listoption
    


    # Recuperacion de datos formulario por tarea
    # cambiar ruta en duro por la ruta en donde se encuentra el archivo  opciones.py 
def recuperar_campos_Formulario(listaFormulario , opcion, key): #path,
    
    machinepassword = key

    client = paramiko.SSHClient()

    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    client.connect(ip, username=user, password=machinepassword, timeout=10)

    stdin, stdout, stderr = client.exec_command("cd /BSCS_RATING/bscs01/prod/WORK/BILLING_TOOLS/MENUFACT/ ; python opcion.py "+str(opcion)) 
    
    lines = stdout.readlines()

    contador = 0
    
    for line in lines:
        if(contador > 1):

            listaFormulario.append(line)

        contador = contador+1
    
    client.close()
    
    return listaFormulario
