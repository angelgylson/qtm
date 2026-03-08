import math
import random
from typing import Optional, Tuple
from rich.console import Console
from rich.progress import track
from rsa_utils import gcd

console = Console()

def find_period_classical(a: int, N: int) -> int:
    """
    Classically simulates the quantum period-finding part of Shor's Algorithm.
    Finds the smallest r > 0 such that a^r = 1 (mod N).
    
    Warning: This is exponentially slow on a classical computer for large N!
    That's why our simulator uses small bit-size RSA keys.
    """
    for r in range(1, N):
        if pow(a, r, N) == 1:
            return r
    return -1

def shors_algorithm_simulation(N: int) -> Optional[Tuple[int, int]]:
    """
    Simulates Shor's quantum factoring algorithm.
    Returns a tuple of prime factors (p, q).
    """
    console.print(f"[bold cyan]Starting Shor's Algorithm simulation to factor N = {N}[/bold cyan]")
    
    # 1. Handle easy cases
    if N % 2 == 0:
        return (2, N // 2)

    attempts = 0
    while True:
        attempts += 1
        console.print(f"\n[grey53]--- Attempt {attempts} ---[/grey53]")
        
        # 2. Pick a random number 'a' between 1 and N-1
        a = random.randint(2, N - 1)
        console.print(f"1. Choose random a < N: [yellow]a = {a}[/yellow]")
        
        # 3. Check if 'a' shares a factor with N (lucky classical guess)
        g = gcd(a, N)
        if g > 1:
            console.print(f"[bold green]Lucky guess! GCD(a, N) > 1.[/bold green] Found factor: {g}")
            return (g, N // g)
            
        console.print(f"2. GCD({a}, {N}) = 1. Proceeding to quantum period finding.")
        console.print(f"3. \[Quantum Routine] Finding period 'r' of f(x) = {a}^x mod {N}...")
        
        # 4. Find the period r (Quantum simulated classically)
        r = find_period_classical(a, N)
        console.print(f"   => Found period [bold yellow]r = {r}[/bold yellow]")
        
        if r == -1:
            console.print("[red]Period finding failed (r=-1), retrying...[/red]")
            continue
            
        # 5. We need an even period to proceed
        if r % 2 != 0:
            console.print("[red]Period 'r' is odd. Shor's requires an even period. Retrying...[/red]")
            continue
            
        # 6. Check for trivial factors condition: a^(r/2) = -1 mod N
        half_power = pow(a, r // 2, N)
        if half_power == N - 1: # which is -1 mod N
            console.print("[red]Trivial factor condition met (a^(r/2) = -1 mod N). Retrying...[/red]")
            continue
            
        # 7. Calculate the factors!
        console.print("4. Calculating factors from period: p = GCD(a^(r/2) - 1, N), q = GCD(a^(r/2) + 1, N)")
        
        p = gcd(pow(a, r // 2) - 1, N)
        q = gcd(pow(a, r // 2) + 1, N)
        
        # Filter trivial factors just in case
        if p == 1 or q == 1:
            console.print("[red]Found trivial factors (1, N). Retrying...[/red]")
            continue
            
        console.print(f"[bold green]Success! Found factors: p = {p}, q = {q}[/bold green]")
        return (p, q)

if __name__ == "__main__":
    # Test simulation
    test_n = 3233  # 61 * 53
    p, q = shors_algorithm_simulation(test_n)
    print(f"\nResult: {test_n} = {p} * {q}")
