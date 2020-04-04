#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações distribuídas - Projeto 1 - lock_skel.py
Grupo: 13
Números de aluno: 51595, 51628, 51636
"""

#Zona para fazer importação

from lock_pool import *
from sock_utils import *

#Programa principal

class ListSkeleton:

    def __init__(self, numResources, numLocks, numLockedResource, tempLimit):
        self.catalog = lock_pool(numResources, numLocks, numLockedResource, tempLimit)
        self.time = tempLimit
        self.numResources = numResources
        self.numLocks = numLocks

    def processMessage(self, socket):
        """
	Recebe a mensagem e retorna a resposta consoanto o pedido do cliente.
        """
        msg = receive_all(socket, 4)

        if msg[0] == 10 and len(msg) == 3:
            clientID = str(msg[1])
            num_recurso = int(msg[2])
            if num_recurso < self.numResources:
                if self.catalog.lock(num_recurso, clientID, self.time) == True:
                    return [11, True]
                else:
                    return [11, False]
            else:
                return [11, None]

        elif msg[0] == 20 and len(msg) == 3:
            clientID = str(msg[1])
            num_recurso = int(msg[2])
            if num_recurso < self.numResources:
                if self.catalog.release(num_recurso, clientID) == True:
                    return [21, True]
                else:
                    return [21, False]
            else:
                return [21, None]

        elif msg[0] == 30 and len(msg) == 2:
            num_recurso = int(msg[1])
            if num_recurso < self.numResources:
                if self.catalog.test(num_recurso) == 0:
                    return [31, True]
                elif self.catalog.test(num_recurso) == 1:
                    return [31, False]
                else:
                    return [31, "disable"]
            else:
                return [31, None]

        elif msg[0] == 40 and len(msg) == 2:
            num_recurso = int(msg[1])
            if num_recurso < self.numResources:
                return [41, self.catalog.stat(num_recurso)]
            else:
                return [41, None]

        elif msg[0] == 50 and len(msg) == 1:
            return [51, self.catalog.stat_y()]

        elif msg[0] == 60 and len(msg) == 1:
            return [61, self.catalog.stat_n()]

        elif msg[0] == "EXIT":
            self.catalog.clear_disconnected_client_locks(msg[1])
            return ["EXIT"]
