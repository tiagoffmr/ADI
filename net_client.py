#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações distribuídas - Projeto 1 - net_client.py
Grupo: 13
Números de aluno: 51595, 51628, 51636
"""

#Zona para fazer importação

from sock_utils import *

#Programa principal

class server:
    """
    Classe para abstrair uma ligação a um servidor TCP. Implementa métodos
    para estabelecer a ligação, para envio de um comando e receção da resposta,
    e para terminar a ligação
    """

    def __init__(self, address, port):
        """
        Inicializa a classe com parâmetros para funcionamento futuro.
        """
        self.address = address
        self.port = port
        self.conn_socket = create_tcp_client_socket(self.address, self.port)
	
    def connect(self):
        """
        Estabelece a ligação ao servidor especificado na inicialização do
        objeto.
        """
        self.conn_sock.connect(self.address, self.port)
	
    def send_receive(self, data):
        """
        Envia os dados contidos em data para a socket da ligação, e retorna a
        resposta recebida pela mesma socket.
        """
        msg_bytes = pickle.dumps(data, -1)
        size_bytes = struct.pack('!i', len(msg_bytes))

        self.conn_socket.sendall(size_bytes)
        self.conn_socket.sendall(msg_bytes)

        resposta = receive_all(self.conn_socket, 4)
        return resposta
	
    def close(self):
        """
        Termina a ligação ao servidor.
        """
        self.conn_socket.close()
