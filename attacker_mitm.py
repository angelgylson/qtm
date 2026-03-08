import socket
import json
import time
import threading
from rich.console import Console
from rich.panel import Panel

console = Console()

class AttackerMITM:
    def __init__(self, local_port=65431, server_host='127.0.0.1', server_port=65432):
        self.local_port = local_port
        self.server_host = server_host
        self.server_port = server_port
        self.intercepted_data = {}
        
    def run(self):
        console.rule("[bold red]Attacker MITM Proxy Started (Hacker Interface)")
        console.print("[red]Waiting to intercept traffic...[/red]")
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy:
            # Allow port reuse
            proxy.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            proxy.bind(('127.0.0.1', self.local_port))
            proxy.listen()
            
            client_conn, addr = proxy.accept()
            with client_conn:
                console.print(f"[bold red][!] Intercepted connection from client {addr}[/bold red]")
                
                # Connect to real server
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_conn:
                    server_conn.connect((self.server_host, self.server_port))
                    
                    # 1. Intercept Server -> Client (Public Key)
                    server_data = server_conn.recv(4096)
                    pub_key_pkt = json.loads(server_data.decode('utf-8'))
                    self.intercepted_data['public_key'] = (pub_key_pkt['e'], pub_key_pkt['n'])
                    
                    console.print(Panel(f"Intercepted Public Key!\nN = {pub_key_pkt['n']}\nE = {pub_key_pkt['e']}", 
                                        title="[bold red]Capture #1[/bold red]", border_style="red"))
                    
                    # Forward to client
                    client_conn.sendall(server_data)
                    
                    # 2. Intercept Client -> Server (Ciphertext)
                    client_data = client_conn.recv(4096)
                    cipher_pkt = json.loads(client_data.decode('utf-8'))
                    self.intercepted_data['ciphertext'] = cipher_pkt['ciphertext']
                    
                    console.print(Panel(f"Intercepted Encrypted Payload!\nLength: {len(cipher_pkt['ciphertext'])} integers\nFirst 5 ints: {cipher_pkt['ciphertext'][:5]}...", 
                                        title="[bold red]Capture #2[/bold red]", border_style="red"))
                    
                    # Forward to server
                    server_conn.sendall(client_data)
                    
                    console.print("\n[bold red][!] All required data intercepted successfully. Proceeding to Quantum Attack Phase...[/bold red]")
                    
                    # Save intercepted data to file for the attack module to read
                    with open('intercepted.json', 'w') as f:
                        json.dump(self.intercepted_data, f)
                        
                    return self.intercepted_data

if __name__ == "__main__":
    # Test proxy
    mitm = AttackerMITM()
    mitm.run()
