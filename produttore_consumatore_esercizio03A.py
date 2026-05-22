import threading
import random

DIM_BUFFER = 5
N_PRODUTTORI = 3
N_CONSUMATORI = 2
N_ORDINI = 6

buffer = [None] * DIM_BUFFER
metti = 0
togli = 0

vuoto = threading.Semaphore(DIM_BUFFER)
pieno = threading.Semaphore(0)
mutexP = threading.Semaphore(1)
mutexC = threading.Semaphore(1)


def genera_ordine():
    return f"ORD-{random.randint(10000, 99999)}"


class ProduttoreThread(threading.Thread):
    def __init__(self, idx):
        super().__init__()
        self.idx = idx
        self.dato= genera_ordine()

    def run(self):
        global metti
        i=0
        while i<N_ORDINI:
            vuoto.acquire()
            mutexP.acquire()
            i_metti=metti
            metti= (metti+1)%DIM_BUFFER
            mutexP.release()
            buffer[i_metti]=self.dato
            print(f"{self.idx} creato ordine {self.dato}")

            self.dato=genera_ordine()
            pieno.release()
            i = i+1

class ConsumatoreThread(threading.Thread):
    def __init__(self, idx):
        super().__init__()
        self.idx = idx

    def run(self):
        global togli
        Termina = False

        while not(Termina):
            pieno.acquire()
            mutexC.acquire()
            i_togli=togli
            togli= (togli+1)%DIM_BUFFER
            mutexC.release()
            dato=buffer[i_togli]
            if (dato == None):
                Termina=True
                print(f"terminato!")
            else :
                print(f"{self.idx} prepara {dato}")
            vuoto.release()



def main():
    global metti

    produttori = [ProduttoreThread(i + 1) for i in range(N_PRODUTTORI)]
    consumatori = [ConsumatoreThread(i + 1) for i in range(N_CONSUMATORI)]

    for p in produttori:
        p.start()
    for c in consumatori:
        c.start()
    for p in produttori:
        p.join()
    
    print("Tutti i canali hanno terminato. Chiusura addetti...")
    
    for _ in range(N_CONSUMATORI):
        vuoto.acquire()
        buffer[metti]= None
        metti = (metti+1 )% DIM_BUFFER
        pieno.release()
        pass

    for c in consumatori:
        c.join()
    

    print("Magazzino chiuso.")


if __name__ == "__main__":
    main()
