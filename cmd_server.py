import socket
import os

server = socket.socket()
server.bind(('localhost', 4399))
server.listen(5)

while True:
	print('waiting...')
	conn, addr = server.accept()
	print('connectting! ...')
	print(addr)
	while True:
		data = conn.recv(1024)
		data = data.decode()
import socket
import os

server = socket.socket()
server.bind(('localhost', 4399))
server.listen(5)

while True:
	print('waiting...')
	conn, addr = server.accept()
	print('connectting! ...')
	print(addr)
	while True:
		data = conn.recv(1024)
		data = data.decode()
		if data == '':
			break
		if data == 'exit':
			print('this session is closed!')
			break
		print('receive data: ', data)
		res = os.popen(data).read()
		if res == '' :
			conn.send(b'error')
			break
		if conn.send( str(len(res)).encode('utf-8') ):
			for _ in range( int((len(res)/1024)) +1):
				conn.send(res.encode('utf-8'))

#print('send to client: ', conn.send(data.upper()))

server.close()
		if data == '':
			break
		if data == 'exit':
			print('this session is closed!')
			break
		print('receive data: ', data)
		res = os.popen(data).read()
		if res == '' :
			conn.send(b'error')
			break
		if conn.send( str(len(res)).encode('utf-8') ):
			for _ in range( int((len(res)/1024)) +1):
				conn.send(res.encode('utf-8'))

#print('send to client: ', conn.send(data.upper()))

server.close()
