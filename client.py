import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 9999))

while True:
    msg = client.recv(1024).decode()
    print(msg)
    if "Enter" in msg:
        choice = input("Your choice: ")
        client.send(choice.encode())
    if "Win" in msg or "Lose" in msg or "Draw" in msg:
        break

client.close()
