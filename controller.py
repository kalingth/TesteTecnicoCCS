from sys import stdout
from time import sleep
from concurrent.futures import ThreadPoolExecutor
from model import Desafio


class Controler:
    initiator: bool = True

    @property
    def numbers(self):
        return self.desafio.numbers

    def __spin_load(self):
        """Método de Interação durante Carregamento

        Método escrito para tornar o processo da coleta de dados um pouco mais amigável. Pensado na experiência do
        administrador.
        Entradas:

        Saída:

        """

        def spinning_cursor():
            while True:
                for c in "/\u2015\\|":
                    yield c

        spin = spinning_cursor()
        while self.initiator:
            print(next(spin), end="")
            stdout.flush()
            sleep(.5)
            print("\b", end="")

    def eval(self):
        """Método de Acesso às Métricas Internas do Modelo

        Sua função é integrar a camada de visão (Viewer) às métricas registradas na camada modelo (Model) durante
        a execução do método run.
        Realizará a impressão de alguns dados de grande importância para o administrador do servidor. Como número
        de erros durante a coleta e o número de requisições realizadas.
        Entradas:

        Saída:

        """
        print("\t Foram realizadas %d requisições. Destas, foram encontrados %d erros simulados e %d erros"
              " reais de conexão." % self.desafio.evaluete)

    def sortData(self):
        """Método de Acesso ao Algoritmo de Ordenação

        Sua função é integrar a camada de visão (Viewer) ao método de ordenação da camada modelo (Model).
        Realizará a impressão de alguns dados importantes para o administrador do servidor. Como tempo de
        execução e quantos números foram ordenados.
        Entradas:

        Saída:

        """
        print("Organizando os Dados", end="\t\t.....\t\t\tAguarde...")
        stdout.flush()
        log = self.desafio.sort(True)
        print("\b" * 10, "Ok\n", sep="")
        print("Log: ", log)

    def getData(self):
        """Método de Acesso ao Algoritmo de Ordenação

        Sua função é integrar a camada de visão (Viewer) ao método de coleta de dados da camada modelo (Model).
        Realizará a impressão de alguns dados importantes para o administrador do servidor como tempo de execução
        e os dados de avaliação do programa através do método eval.
        Entradas:

        Saída:

        """
        with ThreadPoolExecutor(max_workers=2) as executor:
            print("Coletando Dados", end="\t\t\t\t.....\t\t\t")
            p1 = executor.submit(self.desafio.run, True)
            executor.submit(self.__spin_load)
            while not p1.done():
                pass
            self.initiator = False
            print("\bOk\n")
            print("Log: ", p1.result())

    def start(self):
        """Método de Transações

        Método responsável por fazer as chamadas que realizarão as transações corretamente com o modelo e darão
        feedback ao administrador.
        Entradas:

        Saída:

        """
        print("-" * 71)
        self.getData()
        self.eval()
        print("-" * 71)
        self.sortData()
        print()

    def __init__(self, workers=200):
        """Método de Inicialização do Controlador

        Inicia o controlador e inicializa o modelo.
        Entradas:

        Saída:

        """
        self.desafio = Desafio(n_workers=workers)
        self.start()
