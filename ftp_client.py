import os
import socket
import json

'''
this program will download and upload a file from server
'''

ftp_client = socket.socket()
ftp_client.connect(('localhost', 4399))
ftp_file_dict = {
				'file_cmd': None,
				'file_name': None,
				'file_size': 0,
				'file_ensur': False
}

while True:
	print('you have two options: download _filename,  upload _filename')
	cmd = input('>>:').strip()

	if len(cmd) == 0:
		print('Error! you should put something')
		break
	
	if cmd == 'exit':
		break

	cmd, filename = cmd.split()

	if cmd == 'download':
		''' download, send message to server, server checks file, send '''
		if len(filename) == 0:
			print('error! filename can not be none... ')	
			break
		ftp_file_dict['file_cmd'] = cmd
		ftp_file_dict['file_name'] = filename

		if os.path.isfile(ftp_file_dict['file_name']):
			print('warning! this file is exited, this operation will overriden your file. Are you sure to do that? ')
			ensur = input('y/n? :').strip()
			if ensur == 'y':
				ftp_file_dict['file_ensur'] = True
			elif ensur == 'n':
				break
			else:
				print('you should input again...')
				break
		
		file_dict_json = json.dumps(ftp_file_dict)
		ftp_client.send(file_dict_json.encode('utf-8'))
		
		#processing ftp_file_dict from server(ensure file message)
		down_recv = ftp_client.recv(1024)
		ftp_file_dict = json.loads(down_recv.decode('utf-8'))
		print('file message: ', ftp_file_dict)
		
		#empty operation, preventing sticky bag
		ftp_client.send(b'0')

		#receiving file
		size = ftp_file_dict['file_size']
		download_size = 0
		f = open(ftp_file_dict['file_name'], 'wb') #! F.CLOSE()
		while download_size < size:
			download_recv = ftp_client.recv(1048576) #1024*1024
			if size - download_size < 1048576:
				f.write(download_recv)
				#print('received {} bytes...'.format(download_recv))
			download_size += len(download_recv)
			f.write(download_recv)
		f.close()
	elif cmd == 'upload':
		''' upload, client should check file, send to server '''
	else:		
		print('error! no such command...')
		break
	#ftp_client.send(cmd.encode('utf-8'))
	
	


ftp_client.close()
