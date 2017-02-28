#!/usr/bin/python

"""
Simple HTTP Server version 2: reuses the port, so it can be
restarted right after it has been killed. Accepts connects from
the outside world, by binding to the primary interface of the host.
Jesus M. Gonzalez-Barahona and Gregorio Robles
{jgb, grex} @ gsyc.es
TSAI, SAT and SARO subjects (Universidad Rey Juan Carlos)
"""

import socket

# Create a TCP objet socket and bind it to a port
# Port should be 80, but since it needs root privileges,
# let's use one above 1024

mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Let the port be reused if no process is actually using it
mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Bind to the address corresponding to the main name of the host
mySocket.bind(('localhost', 1234))

# Queue a maximum of 5 TCP connection requests

mySocket.listen(5)

# Accept connections, read incoming data, and an	swer back an HTML page
#  (in an almost-infinite loop; the loop can be stopped with Ctrl+C)

try:
	while True:
		print('Waiting for connections')
		(recvSocket, address) = mySocket.accept()
		print('Request received:')
		peticion = recvSocket.recv(2048).decode("utf-8","strict") # bytes pasados a utf-8
		print(peticion)
		recurso = peticion.split()[1][1:]
		sumando1 = peticion.split()[1][1:]
		dicc = {}
		if recurso in dicc:
			suma = int(dicc[sumando1]) + int(recurso)
			resp = recvSocket.send(bytes("HTTP/1.1 200 OK\r\n\r\n" +
							"</p>" +
							"Me habías enviado un " + sumando1 +
			              	".Ahora un " + recurso +
			                ".La suma es " + str(suma) +
                            "</body></html>" +
                            "\r\n", 'utf-8'))
			recvSocket.close()
		else:
			dicc[sumando1] = recurso
			resp = recvSocket.send(bytes("HTTP/1.1 200 OK\r\n\r\n" +
                       		"</p>" +
                        	"Me has enviado un " + sumando1 +
							".Dame otro sumando" +
                        	"</body></html>" +
                        	"\r\n", 'utf-8'))
			recvSocket.close()
		print(resp)
except KeyboardInterrupt:
    print("Closing binded socket")
    mySocket.close()
