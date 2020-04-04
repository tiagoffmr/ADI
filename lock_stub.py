#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações distribuídas - Projeto 1 - lock_stub.py
Grupo: 13
Números de aluno: 51595, 51628, 51636
"""

#Zona para fazer importação

from net_client import server

#Programa principal

class list_stub:
    def __init__(self, server_addr, server_port):
        """
        Inicializa a classe com os argumentos server_addr e server_port que servem para estabelecer a ligacao ao servidor.
        """
        self.address = server_addr
        self.port = server_port
        self.connection = server(server_addr, server_port)
	
    def sendreceive(self, data):
        """
	Recebe os dados e retorna a resposta.
	"""
        response = self.connection.send_receive(data)
        return response
	
    def close(self):
        """
	Fecha a conexão do cliente com o servidor.
	"""
        self.connection.close()
