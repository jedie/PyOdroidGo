import time
import machine

def main(screen):
    for i in range(5, 0, -1):
        screen.echo("Hard reset in %i Sek!" % i)
        time.sleep(1)
        
    screen.echo("reset...")
    machine.reset()
