Aplicações Distribuídas 2018/19 - 2ªEntrega 

Trabalho realizado por:
	- Diogo Frazão Nº51595
	- Tiago Robalo Nº51628
	- Vasco Bento Nº51636


Melhoramentos de implementação do Projeto 1 para o Projeto 2:
 - Não foi feito nenhum melhoramento de implementação do Projeto 1 para o Projeto 2

Limitações na implementação:
 - Não foi encontrada nenhuma limitação na implementação

Implementação de outras funcionalidades:
 - Foi criada uma função(clear_disconnected_client_locks) que é chamada quando um cliente se disconecta 
   que remove o(s) lock(s) do cliente

-------------------------------------------------------------------------------------------------------
	                                lock_pool.py
-------------------------------------------------------------------------------------------------------
Descrição:
	Este ficheiro cria os recursos e estes são geridos pelo lock_server.py.


-------------------------------------------------------------------------------------------------------
	                                lock_skel.py
-------------------------------------------------------------------------------------------------------
Descrição:
	Este ficheiro recebe, processa e envia a mensagem de volta ao cliente. Consoante a mensagem, 
	responde [11, True/False/None], [21, True/False/None], [31, True/False/Disable/None], 
	[[41, <nº de bloqueios do recurso em K>/None], [51, <nº de recursos bloqueados em Y], 
	[61, <nº de recursos disponíveis].


-------------------------------------------------------------------------------------------------------
	                                lock_server.py
-------------------------------------------------------------------------------------------------------
Descrição:
	O servidor irá esperar que sejam efetuadas várias conexões, este suporta multiplos clientes.

Sinopse:
	lock_server.py porta N K Y T 

Opções:
	porta - Porta TCP onde escutará por pedidos de ligação;
	N - Número de recursos que serão geridos pelo servidor;
	K - Número de bloqueios permitidos de cada recurso;
	Y - Número permitido de recursos bloqueados num dado momento;
	T - Tempo de concessão (em segundos) dos bloqueios.

Exemplo:
	lock_server.py 9999 5 2 3 120 

	Irá ser criado um servidor com a porta TCP 9999, onde terá disponivel 5 recursos, cada recurso 
        pode ser bloqueado 2 vezes, após o final do segundo bloqueio passa a estar inativo.
	Dos 5 recursos geridos pelo servidor apenas podem estar bloqueados em simultâneo 3. Quando um 
        recurso é bloqueado ao fim de 120 segundos passará a estar desbloqueado a não ser que seja o seu 
        último bloqueio possível(passa a estar inativo).


---------------------------------------------------------------------------------------------------------
	                                lock_client.py
---------------------------------------------------------------------------------------------------------
Descrição:
	Este ficheiro serve para que cada cliente consiga aceder aos recursos que se encontram disponíveis 
	no servidor.


Sinopse:
	lock_client.py ip porta id_cliente

Opções:
	ip - O ip do servidor que fornece os recursos;
	porta - A porta TCP onde o servidor recebe pedidos de ligação;
	id_cliente - O id único do cliente.

Exemplo:
	lock_client.py 127.0.0.1 9999 007


---------------------------------------------------------------------------------------------------------
	                                lock_stub.py
---------------------------------------------------------------------------------------------------------
Descrição:
	Este ficheiro inicializa a ligação do cliente ao servidor.


---------------------------------------------------------------------------------------------------------
	                                net_client.py
---------------------------------------------------------------------------------------------------------
Descrição:
	Este ficheiro contém as definições respeitantes à comunicação do cliente com o servidor.

