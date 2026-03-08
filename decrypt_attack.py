import json
import time
from rich.console import Console
from rich.panel import Panel

from rsa_utils import mod_inverse, decrypt, ints_to_string
from shor_simulation import shors_algorithm_simulation
from attacker_mitm import AttackerMITM

console = Console()

def run_attack():
    console.rule("[bold red]QUANTUM ATTACK SIMULATOR (DARK-WEB INTERFACE)")
    
    # 1. Start MITM Interception
    console.print("\n[red]>>> Stage 1: Network Sniffing[/red]")
    mitm = AttackerMITM(local_port=65431, server_host='127.0.0.1', server_port=65432)
    # This blocks until it intercepts the full exchange
    intercepted = mitm.run()
    
    # 2. Extract Data
    e, N = intercepted['public_key']
    ciphertext = intercepted['ciphertext']
    
    console.print("\n[red]>>> Stage 2: Quantum Factorization[/red]")
    console.print(f"[yellow][*] Target Modulus N = {N}[/yellow]")
    console.print(f"[yellow][*] Intercepted {len(ciphertext)} encrypted bytes.[/yellow]")
    
    # Simulate Shor's Algorithm
    time.sleep(1) # Dramatic effect
    p, q = shors_algorithm_simulation(N)
    
    # 3. Reconstruct Private Key
    console.print("\n[red]>>> Stage 3: Key Reconstruction[/red]")
    phi = (p - 1) * (q - 1)
    d = mod_inverse(e, phi)
    
    console.print(Panel(f"Target Public Key (e, N) = ({e}, {N})\nPrime Factors (p, q) = ({p}, {q})\nEuler's Totient phi(N) = {phi}\n\n[bold white]Calculated Private Key d = {d}[/bold white]",
                        title="[bold green]Recovered Private Key[/bold green]", border_style="green"))
                        
    # 4. Decrypt the payload!
    console.print("\n[red]>>> Stage 4: Payload Decryption[/red]")
    
    decrypted_ints = [decrypt((d, N), char) for char in ciphertext]
    plaintext = ints_to_string(decrypted_ints)
    
    console.print(Panel(f"[bold red]DECRYPTED SECRET MESSAGE:[/bold red]\n\n[bold white]{plaintext}[/bold white]",
                        title="[blink red]ATTACK SUCCESSFUL[/blink red]", border_style="red"))

if __name__ == "__main__":
    run_attack()
