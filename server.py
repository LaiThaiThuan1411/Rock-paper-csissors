import socket
import threading

clients = []
choices = {}

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    conn.send("Welcome! Waiting for opponent...\n".encode())

    clients.append(conn)
    if len(clients) < 2:
        conn.send("Waiting for second player...\n".encode())
    while len(clients) < 2:
        continue

    conn.send("Game Start! Enter Rock, Paper or Scissors: ".encode())
    choice = conn.recv(1024).decode().strip().lower()
    choices[conn] = choice
    print(f"[{addr}] chose {choice}")

    while len(choices) < 2:
        continue

    c1, c2 = clients[0], clients[1]
    result = get_winner(choices[c1], choices[c2])

    c1.send(f"You chose: {choices[c1]}. Opponent chose: {choices[c2]}. {result[0]}\n".encode())
    c2.send(f"You chose: {choices[c2]}. Opponent chose: {choices[c1]}. {result[1]}\n".encode())

    conn.close()

def get_winner(p1, p2):
    if p1 == p2:
        return ("Draw!", "Draw!")
    elif (p1 == "rock" and p2 == "scissors") or (p1 == "scissors" and p2 == "paper") or (p1 == "paper" and p2 == "rock"):
        return ("You Win!", "You Lose!")
    else:
        return ("You Lose!", "You Win!")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 9999))
server.listen(2)
print("[STARTING] Server is listening...")

while True:
    conn, addr = server.accept()
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()
