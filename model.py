from concurrent.futures import ThreadPoolExecutor
from requests import get as getreq
from requests.exceptions import ConnectionError
from time import time as timer


class Desafio:
    __error_count: int = 0
    __conn_errors: int = 0
    __n_requests: int = 0

    class DesafioValueError(Exception):
        pass

    class DesafioRequestError(Exception):
        pass

    @property
    def numbers(self):
        return self.__numbers

    @property
    def evaluete(self):
        return self.__n_requests, self.__error_count, self.__conn_errors

    def __init__(self, start: int = 1, n_workers: int = 250) -> None:
        """Método de Inicialização:

        Método responsável por inicializar as variáveis importantes para o funcionamento do programa.
        Entradas:
            start <- inteiro
                Parâmetro reponsável por indicar em que ponto a varredura deverá começar.
            n_workers <- inteiro
                Parâmetro reponsável por informar o número de tarefas que deverão ser executadas simultaneamente.
        Saída:
            self -> objeto
                Retorna um objeto que representa a própria classe inicializada.
        """
        if type(start) != int or start < 1:
            raise self.DesafioValueError("O valor de início deve pertencer ao conjunto dos números naturais."
                                         " ]0, \u221e[")
        if type(start) != int or start < 1:
            raise self.DesafioValueError("O número de tarefas deve pertencer ao conjunto dos números naturais."
                                         " ]0, \u221e[")
        self.workers = n_workers
        self.i = start
        self.__numbers = []

    def __quick_part__(self, i: int, f: int) -> int:
        """Implementação do Algoritmo de Ordenação QuickSort

        Segunda parte da implementação do Algoritmo QuickSort de C.A.R. Hoare.
        Nesta etapa um pivô será selecionado e, do outro lado da lista, serão colocados dois marcadores. Um se
        movimentará à cada iteração do for e o outro se movimentará, nesse caso, a cada vez que um valor menor
        que o pivô for encontrado.
        Entradas:
            i <- inteiro
                Ponto inicial do ordenamento.
            f <- inteiro
                Ponto final do ordenamento.
        Saída:
            mark1 -> inteiro
                posição à qual o pivô se encontra ao término da segunda parte (posição final que ele deverá estar).
        """
        pivot = self.__numbers[f]
        mark1 = i
        for mark2 in range(i, f):
            if self.__numbers[mark2] <= pivot:
                self.__numbers[mark1], self.__numbers[mark2] = self.__numbers[mark2], self.__numbers[mark1]
                mark1 += 1
        self.__numbers[mark1], self.__numbers[f] = self.__numbers[f], self.__numbers[mark1]
        return mark1

    def __quicksort__(self, i: int, f) -> None:
        """Implementação do Algoritmo de Ordenação QuickSort

        Primeira parte da implementação do Algoritmo QuickSort de C.A.R. Hoare.
        Artigo de referência na escolha do algoritmo:
                                      * https://www.devmedia.com.br/algoritmos-de-ordenacao-analise-e-comparacao/28261
        Entradas:
            i <- inteiro
                Ponto inicial do ordenamento. Por se tratar de uma função recursiva, a função deverá ir settando a cada
                chamada que ela mesma realizará.
            f <- inteiro
                Ponto final do ordenamento. Por se tratar de uma função recursiva, a função deverá ir settando a cada
                chamada que ela mesma realizará.
        Saída:

        """
        if i < f:
            part = self.__quick_part__(i, f)
            self.__quicksort__(i, part - 1)
            self.__quicksort__(part + 1, f)

    def sort(self, evaluete: bool = False) -> str:
        """Método de Encapsulamento do Algoritmo de Ordenação

        Função que realizará a chamada da função quicksort e impedirá que o usuário manipule a variáveis de entrada.
        Ação de prevenção a problemas que podem ser causadas pelo mau uso da função recursiva.
        Entradas:
            evaluete <- boleano
                Indica se o método deverá ou não realizar a métrica do tempo de execução.
        Saída:
            log -> texto
                Retornará uma string informando quantos digitos foram ordenados. Caso o usuário deseje, o método
                realizará a metrificação do tempo de execução em segundos.
        """
        start = timer() if evaluete else 0
        initial = 0
        final = len(self.__numbers) - 1
        self.__quicksort__(initial, final)
        if evaluete:
            complete = timer() - start
            log = "%d digitos foram ordenados em %.2f segundos" % (final+1, complete)
            return log

    def __parser__(self, futures: list) -> list:
        """Método de Validação:

        Método responsável por verificar os dados recebidos e retornar uma lista contendo os números recebidos.
        Entradas:
            futures <- lista
                Parâmetro contendo uma lista de objetos assíncronos já resolvidos (cuja execução já foi concluída).
        Saída:
            temp -> lista
                Uma lista contendo os números capturados da plataforma
        """
        temp = []
        for present in futures:
            result = present.result()
            if "numbers" in result.keys():
                temp.extend(result["numbers"])
            else:
                self.__error_count += 1
        return temp

    def __async_get__(self) -> list:
        """Método de Coleta Assíncrona

        Método que controlará o número
        Saída:
            numbers -> lista
                Retorna um objeto que representa a própria classe inicializada.
        """
        futures = []
        with ThreadPoolExecutor(max_workers=self.workers) as executor:
            for i in range(self.workers):
                page = f"http://challenge.dienekes.com.br/api/numbers?page={self.i + i}"
                futures.append(
                    executor.submit(self.get_json, page)
                )
        numbers = self.__parser__(futures)
        return numbers

    def get_json(self, uri: str) -> dict:
        """Método de Raspagem:

        Método responsável por realizar as requisições ao servidor e retornar a resposta como um dicionário.
        O método tentará até 3 conexões com o servidor. Caso a conexão falhe nas 3, um erro será lançado.
        Entradas:
            uri <- texto
                Parâmetro para designar a fonte dos dados a serem raspados;
        Saída:
            dictionary <- dicionário(objeto)
                Dicionário contendo o corpo da resposta do servidor / requisição.
        """
        response = None
        for i in range(3):
            try:
                self.__n_requests += 1
                response = getreq(uri)
            except ConnectionError:
                self.__conn_errors += 1
                continue
            else:
                break
        if response is None:
            raise self.DesafioRequestError("Não foi possível se conectar ao servidor do desafio. Por favor, "
                                           "tente novamente")
        dictionary = response.json()
        return dictionary

    def run(self, evaluete: bool = False) -> [None, str]:
        """Método de Execução:

        Método responsável pelo loop de execução do programa. Este método será executado até que as requisições
        retornem uma lista nula.
        Entradas:
            evaluete <- boleano
                Caso este parâmetro seja settado como True, ele realizará um print do tempo de execução ao coletar
                os dados do servidor.
        Saída:

        """
        start = timer() if evaluete else 0
        self.__numbers = []
        self.__error_count = 0
        self.__conn_errors = 0
        self.__n_requests = 0
        while True:
            received = self.__async_get__()
            if not received:
                break
            self.__numbers.extend(received)
            self.i += self.workers

        if evaluete:
            complete = timer() - start
            minutes = complete // 60
            seconds = complete % 60
            log = "A coleta foi realizada em %d minutos e %.2f segundos." % (minutes, seconds)
            return log


if __name__ == "__main__":
    desafio = Desafio(n_workers=200)
    desafio.run(evaluete=True)
    sort_log = desafio.sort(evaluete=True)
    print(sort_log)
    print("Foram realizadas %d requisições. Destas, foram encontrados %d erros simulados e %d erros reais de conexão"
          % desafio.evaluete)
