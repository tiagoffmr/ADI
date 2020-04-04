#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações distribuídas - Projeto 1 - lock_server.py
Grupo: 13
Números de aluno: 51595, 51628, 51636
"""

#Zona para fazer importação

import argparse,pickle, struct,  sys
import select
from sock_utils import *
from lock_skel import *

#Programa principal

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("TCPPort", type = int, help='TCP Port - Same for every client')
    parser.add_argument("N", type = int, help='Number of resources')
    parser.add_argument("K", type = int, help='Maximum number of locks per resource')
    parser.add_argument("Y", type = int, help='Maximum number of locked resources')
    parser.add_argument("T", type = int, help='Time in seconds')
    args = parser.parse_args()

    if args.Y >= args.N:
        print("Y must be lower than N\n")
        exit()

    listener_socket = create_tcp_server_socket('', args.TCPPort, 1)
    lista_sock = [listener_socket, sys.stdin]
    skel = ListSkeleton(args.N, args.K, args.Y, args.T)

    while True:
        R, W, X = select.select(lista_sock,[],[])
        skel.catalog.clear_expired_locks()
        for socket in R:
            if socket is listener_socket:
                (conn_sock, addr) = socket.accept()
                addr, port = conn_sock.getpeername()
                print("New client connected, IP address: " + str(addr) + ", Port: " + str(port) + ".\n")
                lista_sock.append(conn_sock)

            elif socket is sys.stdin:
                stdin = sys.stdin.readline()
                if stdin == "Exit\n" or stdin == "EXIT\n" or stdin == "exit\n":
                    sys.exit()

            else:
                resposta = skel.processMessage(socket)

                resp_bytes = pickle.dumps(resposta, -1)
                size_bytes = struct.pack('!i', len(resp_bytes))
                socket.sendall(size_bytes)
                socket.sendall(resp_bytes)

                if resposta[0] == "EXIT":
                    print("The client with IP address: " + str(addr) + ", Port: " + str(port) + " has disconnected.\n")
                    socket.close()
                    lista_sock.remove(socket)
                else:
                    print(repr(skel.catalog))
