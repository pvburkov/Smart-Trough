def send_photo(photo_name):
	import socket
	
	try:
		sock = socket.socket()
		sock.connect(('52.169.114.1', 9090))

		file = open(photo_name, "rb")
		while True:
			data = file.read(1024)
			if not data:
				break
			sock.send(data)
		file.close()
		sock.close()
		return 'OK'
		
	except Exception as e:
		return str(e)

if __name__ == '__main__':
	print(send_photo('123.jpg'))
