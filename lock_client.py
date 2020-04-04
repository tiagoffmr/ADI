#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações distribuídas - Projeto 1 - lock_client.py
Grupo: 13
Números de aluno: 51595, 51628, 51636
"""

#Zona para fazer importação

import argparse
from lock_stub import list_stub

#Programa principal

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument("IPAddress", type = str, help='IP Address - Different for each client')
	parser.add_argument("TCPPort", type = int, help='TCP Port - Same as the server')
	parser.add_argument("ClientID", type = int, help='Client ID - Different for each client')
	args = parser.parse_args()

	ls = list_stub(args.IPAddress, args.TCPPort)
	ClientID = args.ClientID

	cmd = ""
	while cmd != "EXIT":

		cmd = input("comando > ")
		cmdS = cmd.split(" ")

		if cmdS[0] == "EXIT":
			resposta = ls.sendreceive(["EXIT", ClientID])

		elif cmdS[0] == "LOCK" and len(cmdS) == 2:
			resposta = ls.sendreceive([10, ClientID, int(cmdS[1])])

		elif cmdS[0] == "RELEASE" and len(cmdS) == 2:
			resposta = ls.sendreceive([20, ClientID, int(cmdS[1])])

		elif cmdS[0] == "TEST" and len(cmdS) == 2:
			resposta = ls.sendreceive([30, int(cmdS[1])])

		elif cmdS[0] == "STATS" and len(cmdS) == 2:
			resposta = ls.sendreceive([40, int(cmdS[1])])

		elif cmdS[0] == "STATS-Y" and len(cmdS) == 1:
			resposta = ls.sendreceive([50])

		elif cmdS[0] == "STATS-N" and len(cmdS) == 1:
			resposta = ls.sendreceive([60])

		else:
			resposta = "UNKNOWN COMMAND"

		print(str(resposta))

	ls.close()
	exit()
