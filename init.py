import boot as mainB
import subprocess
import tempfile
import os
from threading import Thread

def audio(filepath, repeats=1):
    subprocess.Popen(f"ffplay -nodisp -autoexit -loop {repeats} {filepath}", shell=True)


  
def playBoot():
     audio(os.path.join(dir, "audio/beep.wav"))


dir = os.path.realpath(os.path.join(
    os.getcwd(), os.path.dirname(__file__)))  # pega o diretorio do arquivo
thread = Thread(target=playBoot)

thread.start()


### iniciar
if mainB.iniciar():
    senha = mainB.login()
    if senha != None:
        print(mainB.menu())
    else:
        mainB.bloquearTela()
