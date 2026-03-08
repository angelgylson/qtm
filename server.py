import socket
import json
from rsa_utils import generate_keypair, decrypt, ints_to_string
from rich.console import Console
from rich.panel import Panel

console = Console()

def run_server(host='127.0.0.1', port=65432):
    console.rule("[bold blue]Secure Server Started")
    
    # 1. Generate RSA Keys (using small bit size for simulation purposes)
    bit_size = 16
    console.print(f"[yellow]Generating {bit_size}-bit RSA keypair...[/yellow]")
    public_key, private_key = generate_keypair(bit_size)
    
    console.print(Panel(f"Public Key (e, n): {public_key}\nPrivate Key (d, n): {private_key}", 
                        title="Server Keys", border_style="green"))

    # 2. Setup socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Allow port reuse
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen()
        console.print(f"[green]Listening for connections on {host}:{port}...[/green]")
        
        conn, addr = s.accept()
        with conn:
            console.print(f"[bold green]Connected by {addr}[/bold green]")
            
            # 3. Send public key to client
            conn.sendall(json.dumps({'e': public_key[0], 'n': public_key[1]}).encode('utf-8'))
            console.print("[cyan]Public key sent to client.[/cyan]")
            
            # 4. Receive encrypted message
            data = conn.recv(4096)
            if not data:
                return
                
            payload = json.loads(data.decode('utf-8'))
            ciphertext = payload.get('ciphertext', [])
            
            console.print(Panel(f"{ciphertext}", title="Received Ciphertext", border_style="red"))
            
            # 5. Decrypt message
            console.print("[yellow]Decrypting message with private key...[/yellow]")
            decrypted_ints = [decrypt(private_key, char) for char in ciphertext]
            plaintext = ints_to_string(decrypted_ints)
            
            console.print(Panel(f"[bold white]{plaintext}[/bold white]", title="Decrypted Message", border_style="green"))

if __name__ == "__main__":
    run_server()
