import socket
import json
from rsa_utils import encrypt, string_to_ints
from rich.console import Console
from rich.panel import Panel

console = Console()

def run_client(host='127.0.0.1', port=65431, message="TOP SECRET: QUANTUM ALGORITHM FOUND"):
    console.rule("[bold blue]Secure Client Started")
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        console.print(f"[yellow]Connecting to {host}:{port}...[/yellow]")
        try:
            s.connect((host, port))
        except ConnectionRefusedError:
            console.print("[bold red]Connection refused. Is the server running?[/bold red]")
            return
            
        console.print("[green]Connected successfully.[/green]")
        
        # 1. Receive public key
        data = s.recv(4096)
        pub_key_data = json.loads(data.decode('utf-8'))
        public_key = (pub_key_data['e'], pub_key_data['n'])
        
        console.print(Panel(f"Received Public Key (e, n): {public_key}", title="Server Public Key", border_style="cyan"))
        
        # 2. Encrypt message
        console.print(f"[yellow]Original Message:[/yellow] {message}")
        encoded_ints = string_to_ints(message)
        
        console.print("[yellow]Encrypting message...[/yellow]")
        ciphertext = [encrypt(public_key, char) for char in encoded_ints]
        
        console.print(Panel(f"{ciphertext}", title="Ciphertext to Send", border_style="red"))
        
        # 3. Send encrypted message
        payload = json.dumps({'ciphertext': ciphertext})
        s.sendall(payload.encode('utf-8'))
        console.print("[bold green]Message sent reliably to server![/bold green]")

if __name__ == "__main__":
    run_client()
