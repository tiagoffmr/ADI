#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações distribuídas - Projeto 1 - lock_pool.py
Grupo: 13
Números de aluno: 51595, 51628, 51636
"""

#Zona para fazer importação

import time

#Programa principal

class resource_lock:
    def __init__(self):
        """
        Define e inicializa as características de um LOCK num recurso.
        """
        self.nTimes = 0
        self.blocked = 1      #0-bloqueado   1-desbloqueado   2-inativo
        self.byWho = None
        self.timeLock = None

    def lock(self, client_id, time_limit):
        """
        Bloqueia o recurso se este não estiver bloqueado ou inativo, ou mantém o bloqueio
        se o recurso estiver bloqueado pelo cliente client_id. Neste caso renova
        o bloqueio do recurso até time_limit.
        Retorna True se bloqueou o recurso ou False caso contrário.
        """
        if self.blocked == 1 :                             #estava desbloqueado e bloqueamos
            self.byWho = client_id
            self.nTimes += 1
            self.blocked = 0
            self.timeLock = time.time() + time_limit
            return True
        elif self.blocked == 0 and self.byWho == client_id:
                self.timeLock = time.time() + time_limit
                self.nTimes += 1
                return False
        else:
            return False

    def urelease(self):
        """
        Liberta o recurso incondicionalmente, alterando os valores associados
        ao bloqueio.
        """
        self.byWho = None
        self.blocked = 1
        self.temp = None

    def release(self, client_id):
        """
        Liberta o recurso se este foi bloqueado pelo cliente client_id,
        retornando True nesse ecaso. Caso contrário retorna False.
        """
        if self.byWho == client_id:
            self.blocked = 1
            return True
        else:
            return False

    def test(self):
        """
        Retorna o estado de bloqueio do recurso ou inativo, caso o recurso se
        encontre inativo.
        """
        return self.blocked

    def stat(self):
        """
        Retorna o número de vezes que este recurso já foi bloqueado.
        """
        return self.nTimes

    def stat_byWho(self):
        """
        Retorna o ClientID do recurso bloqueado.
        """
        return self.byWho

    def stat_timeLock(self):
        """
        Retorna o tempo que o recurso estará bloqueado.
        """
        return self.timeLock

    def disable(self):
        """
        Coloca o recurso inativo/indisponível incondicionalmente, alterando os
        valores associados à sua disponibilidade.
        """
        self.blocked = 2

class lock_pool:
    def __init__(self, N, K, Y, T):
        """
        Define um array com um conjunto de locks para N recursos. Os locks podem
        ser manipulados pelos métodos desta classe.
        Define K, o número máximo de bloqueios permitidos para cada recurso. Ao
        atingir K, o recurso fica indisponível/inativo.
        Define Y, o número máximo permitido de recursos bloqueados num dado
        momento. Ao atingir Y, não é possível realizar mais bloqueios até que um
        recurso seja libertado.
		Define T, o tempo máximo de concessão de bloqueio.
        """
        self.locksList = []

        for i in range(N):
            rec = resource_lock()
            self.locksList.append(rec)

        self.k = K
        self.y = Y
        self.t = T

    def clear_expired_locks(self):
        """
        Verifica se os recursos que estão bloqueados ainda estão dentro do tempo
        de concessão do bloqueio. Liberta os recursos caso o seu tempo de
        concessão tenha expirado.
        """
        for rec in range(len(self.locksList)):
            if self.locksList[rec].test() == 0 and self.locksList[rec].stat_timeLock() <= time.time():
                    self.locksList[rec].urelease()
                    if self.locksList[rec].stat() == self.k:
                        self.locksList[rec].disable()

    def clear_disconnected_client_locks(self, clientID):
        """
	Liberta o(s) recurso(s) bloqueado(s) pelo clientID, quando este se 
	desconecta do servidor.
        """
        for rec in range(len(self.locksList)):
            if self.locksList[rec].stat_byWho() == str(clientID):
                self.locksList[rec].urelease()


    def lock(self, resource_id, client_id, time_limit):
        """
        Tenta bloquear o recurso resource_id pelo cliente client_id, até ao
        instante time_limit.
        O bloqueio do recurso só é possível se o recurso estiver ativo, não
        bloqueado ou bloqueado para o próprio requerente, e Y ainda não foi
        excedido. É aconselhável implementar um método __try_lock__ para
        verificar estas condições.
        Retorna True em caso de sucesso e False caso contrário.
        """
        if self._try_lock(resource_id, client_id):
            self.locksList[resource_id].lock(client_id, time_limit)
            return True
        else:
            return False

    def release(self, resource_id, client_id):
        """
        Liberta o bloqueio sobre o recurso resource_id pelo cliente client_id.
        True em caso de sucesso e False caso contrário.
        """
        return self.locksList[resource_id].release(client_id)

    def test(self,resource_id):
        """
        Retorna 0 se o recurso resource_id estiver bloqueado,
        1 caso esteja desbloqueado e 2 caso esteja inativo.
        """
        if self.locksList[resource_id].test() == 0:
            return 0                                                    #recurso bloqueado
        elif self.locksList[resource_id].test() == 1:
            return 1                             			#recurso desbloqueado
        else:
            return 2                         				#recurso inativo

    def _try_lock(self, resource_id, client_id):
        """
        Verifica se o recurso pode ser bloqueado, True,
        ou não, False.
        """
        if self.stat(resource_id) < self.k:
            if self.locksList[resource_id].test() == 1 and self.stat_y() < self.y:
                return True
            elif self.locksList[resource_id].test() == 0 and self.locksList[resource_id].stat_byWho() == client_id and self.stat_y() <= self.y:
                return True
        else:
            return False

    def stat(self,resource_id):
        """
        Retorna o número de vezes que o recurso resource_id já foi bloqueado, dos
        K bloqueios permitidos.
        """
        return self.locksList[resource_id].stat()

    def stat_y(self):
        """
        Retorna o número de recursos bloqueados num dado momento do Y permitidos.
        """
        cont = 0
        for i in self.locksList:
            if i.test() == 0:
                cont += 1
        return cont

    def stat_n(self):
        """
        Retorna o número de recursos disponíneis em N.
        """
        cont = 0
        for i in self.locksList:
            if i.test() == 1:
                cont += 1
        return cont

    def __repr__(self):
        """
        Representação da classe para a saída standard. A string devolvida por
        esta função é usada, por exemplo, se uma instância da classe for
        passada à função print.
        """
        output = ""
        for resourceID in range(len(self.locksList)):
            if self.locksList[resourceID].test() == 0:
                output += "recurso " + str(resourceID) + " bloqueado pelo cliente " + \
                str(self.locksList[resourceID].stat_byWho()) + " até " + \
                time.ctime(self.locksList[resourceID].stat_timeLock()) + "\n"
            elif self.locksList[resourceID].test() == 2:
                output += "recurso " + str(resourceID) + " inativo\n"
            else:
                output+= "recurso " + str(resourceID) + " desbloqueado\n"
        return output
