from socket import *
import ssl
import base64

msg = "\r\n I love computer networks! Apes together STRONG!!!!!!!!"
username = "**"
password = '**'
recipient = "<**>\r\n"
sender = "<**>"

mailserver = 'smtp.gmail.com'

# Create socket called clientSocket and establish a TCP connection with mailserver
# Fill in start
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((mailserver, 587))
# Fill in end

recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '220':
    print('220 reply not received from server.')

# Send HELO command and print server response.
print("sending HELO command")
heloCommand = 'HELO Alice\r\n'
clientSocket.send(heloCommand.encode())
recv1 = clientSocket.recv(1024).decode()
print(recv1)
if recv1[:3] != '250':
    print('250 reply not received from server.')

# Start a TLS connection
TLSCommand = 'STARTTLS\r\n'
clientSocket.send(TLSCommand.encode())
recvtls = clientSocket.recv(1024).decode()
print(recvtls)
if recvtls[:3] != '220':
    print('220 reply not received from server')

clientSocket = ssl.wrap_socket(clientSocket)

# Send AUTH LOGIN command
print("Sending AUTH LOGIN command")
authCommand = 'AUTH LOGIN\r\n'
clientSocket.write(authCommand.encode())
recvAUTH = clientSocket.read(1024).decode()
print(recvAUTH)
if recvAUTH[:3] != '334':
    print('334 reply not received from server')


# Send the username specified above
USRname = base64.b64encode(username.encode()) + "\r\n".encode()
print("Sending Username")
clientSocket.write(USRname)
recvUSRname = clientSocket.read(1024).decode()
print(recvUSRname)
if recvUSRname[:3] != '334':
    print('334 reply not received from server')

# Send the password for the username specified above
PSword = base64.b64encode(password.encode()) + '\r\n'.encode()
print("Sending password")
clientSocket.write(PSword)
recvPSword = clientSocket.read(1024).decode()
print(recvPSword)
if recvPSword[:3] != '235':
    print('235 reply not received from server')

# Send MAIL FROM command and print server response.
print("sending MAIL FROM command")
clientSocket.send("MAIL FROM:".encode() + sender.encode() + "\r\n".encode())
recv1 = clientSocket.recv(1024).decode()
print(recv1)
if recv1[:3] != '250':
    print('250 reply not received from server.')

# Send RCPT TO command and print server response.
print("sending RCPT TO command")
clientSocket.send("RCPT TO:".encode() + recipient.encode())
recv1 = clientSocket.recv(1024).decode()
print(recv1)
if recv1[:3] != '250':
    print('250 reply not received from server.')

# Send DATA command and print server response.
clientSocket.send("DATA\r\n".encode())
recv1 = clientSocket.recv(1024).decode()
print(recv1)
if recv1[:3] != '354':
    print('354 reply not received from server.')


# Send message data.
clientSocket.send(msg.encode() +"\r\n.\r\n".encode())

recv1 = clientSocket.recv(1024).decode()
print(recv1)
if recv1[:3] != '250':
    print('250 reply not received from server.')

# Send QUIT command and get server response.
QUIT = 'QUIT\r\n'.encode()
clientSocket.send(QUIT)
recv1 = clientSocket.recv(1024).decode()
print(recv1)
if recv1[:3] != '221':
    print('221 reply not received from server.')
