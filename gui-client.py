import socket
import threading
import tkinter as tk
from tkinter import messagebox

class RPSClient:
    def __init__(self, master):
        self.master = master
        self.master.title("Rock Paper Scissors Client")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(("localhost", 9999))

        self.label = tk.Label(master, text="Waiting for server...", font=("Arial", 14))
        self.label.pack(pady=10)

        self.buttons = {}
        for choice in ["Rock", "Paper", "Scissors"]:
            btn = tk.Button(master, text=choice, width=10, command=lambda c=choice: self.send_choice(c.lower()), state='disabled')
            btn.pack(pady=5)
            self.buttons[choice.lower()] = btn

        threading.Thread(target=self.receive).start()

    def send_choice(self, choice):
        self.sock.send(choice.encode())
        self.label.config(text="Waiting for opponent...")

    def receive(self):
        while True:
            try:
                msg = self.sock.recv(1024).decode()
                print("[SERVER]:", msg)
                self.label.config(text=msg)
                if "Enter" in msg:
                    for btn in self.buttons.values():
                        btn.config(state='normal')
                if "Win" in msg or "Lose" in msg or "Draw" in msg:
                    messagebox.showinfo("Result", msg)
                    self.master.quit()
                    break
            except:
                break

root = tk.Tk()
client_app = RPSClient(root)
root.mainloop()
