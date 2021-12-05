import cyberBoot as mainB
from playsound import playsound
import os
from threading import Thread

def playBoot():
 playsound(os.path.join(dir, "audio/beep.wav"))


def playWelcome():
	 playsound(os.path.join(dir, "audio/boot.mp3"))

dir = os.path.realpath(os.path.join(
    os.getcwd(), os.path.dirname(__file__)))  # pega o diretorio do arquivo
thread = Thread(target=playBoot)
thread2 = Thread(target=playWelcome)
thread.start()
thread2.start()

### iniciar
if mainB.iniciar():
    senha = mainB.login()
    if senha != None:
        print(mainB.menu())
    else:
        mainB.bloquearTela()
