#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações distribuídas - Projeto 1 - sock_utilis.py
Grupo: 13
Números de aluno: 51595, 51628, 51636
"""

#Zona para fazer importação

import socket as s
import pickle
import struct

#Programa principal

def create_tcp_server_socket(address, port, queue_size):
	"""
	Cria a ligacao da socket do servidor.
	"""
	try:
		sock = s.socket(s.AF_INET, s.SOCK_STREAM)
		sock.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
		sock.bind((address, port))
		sock.listen(queue_size)
		return sock
	except:
		print("There was an error creating the server socket.")
		exit()
    
def create_tcp_client_socket(address, port):
	"""
	Cria a ligacao da socket do cliente.
	"""
	try:
		sock = s.socket(s.AF_INET, s.SOCK_STREAM)
		sock.connect((address, port))
		return sock
	except:
		print("There was an error creating the client socket.")
		exit()

def receive_all(socket, nbytes):
	"""
	Recebe os dados da mensage e converte.
	"""
	msg_size_bytes = socket.recv(4)
	msg_size = struct.unpack('!i', msg_size_bytes)[0]

	msg_contador = 1024
	msg_bytes = socket.recv(msg_contador)
	while msg_contador < msg_size:
		msg_bytes = msg_bytes + socket.recv(1024)
		msg_contador += 1024

	return pickle.loads(msg_bytes)
