import socket
import threading
import sys
import pickle
import os

class Servidor():
	def __init__(self, host=socket.gethostname(), port = int(input("Que puerto quiere usar: "))):
		self.clientes = []
		self.sock = socket.socket()
		self.sock.bind((str(host), int(port)))
		self.sock.listen(20)
		self.sock.setblocking(False)

		aceptar = threading.Thread(target=self.aceptarC)
		procesar = threading.Thread(target=self.procesarC)
		hostip = socket.gethostbyname(host)
		print("Su ip actual es: ", hostip)

		aceptar.daemon = True
		aceptar.start()
		print("------Hilo que acepta conexiones iniciado en modo DAEMON------")

		procesar.daemon = True
		procesar.start()
		print("------Hilo que procesa mensajes iniciado en modo DAEMON------")

		while True:
			msg = input('SALIR = Q\n')
			if msg == 'Q':
				print("**** TALOGOOO *****")
				self.sock.close()
				sys.exit()
			else:
				pass

	def broadcast(self, msg, cliente):
		for c in self.clientes:
			try:
				if c != cliente:
					c.send(msg)
			except:
				self.clientes.remove(c)
		print("Clientes conectado: ", len(clientes))
		
	def aceptarC(self):
		while True:
			try:
				conn, addr = self.sock.accept()
				print(f"\nConexion aceptada via {addr}\n")
				conn.setblocking(False)
				self.clientes.append(conn)
			except:
				pass

	def procesarC(self):
		#print("Procesamiento de mensajes iniciado")
		while True:
			if len(self.clientes) > 0:
				for c in self.clientes:
					try:
						data = c.recv(32)
						if data:
							self.broadcast(data,c)
					except:
						pass

s = Servidor()