import socket
from datetime import datetime

def logger(info):
	"""
	Функция, работающая с лог-файлом
	"""
	log = open('photo_receiver.log', 'a')
	dt = datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S")
	log.write(dt + ' : ' + info + '\n')
	log.close()


def main():
	sock = socket.socket()
	sock.bind(('', 9090))
	
	try:	
		while True:	
			sock.listen(1)
			conn, addr = sock.accept()
			
			logger('built connection : ' + str(addr))
			dt = datetime.strftime(datetime.now(), "%Y_%m_%d_%H_%M_%S")
			
			file = open(dt + '.jpg', "wb")
			while True:
				data = conn.recv(1024)
				if not data:
					break
				file.write(data)
			
			file.close()
			conn.close()
			logger('destroyed connection : ' + str(addr))
	except KeyboardInterrupt:
		print('Server is going to sleep!')
	except Exception as e:
		print(str(e))
	
if __name__ == '__main__':
	main()