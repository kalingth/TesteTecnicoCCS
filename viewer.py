from flask import Flask, jsonify
from flask_httpauth import HTTPBasicAuth
from controller import Controler
from sys import stdout


class View:
    __users__: dict = {
        "admin": {"password": "P@ssw0rd", "scope": "admin"},
        "root": {"password": "S3nH4", "scope": "admin"},
        "juquinha": {"password": "1234", "scope": "user"}
    }

    def run(self):
        """Método de Inicialização do Servidor

        Método responsável por realizar a inicialização do servidor Flask que responderá com os dados.
        Caminhos disponíveis:
            / -> Retorna todos os dados coletados já organizados.
            /length -> Retorna a quantidade de dados coletados.
            /n1/n2 -> Retorna os dados coletados e já organizados entre as posições n1 e n2 (intervalos fechados)
            /restart -> Método disponível aos administradores para que haja uma nova coleta e reordenação.
        Entradas:

        Saída:

        """
        app = Flask(__name__)
        auth = HTTPBasicAuth()

        @auth.verify_password
        def auth_admin(login, password):
            if not (login or password):
                return False
            user_data = self.__users__.get(login)
            if user_data and user_data["scope"] == "admin":
                return user_data["password"] == password
            return False

        @app.route("/restart")
        @auth.login_required
        def restart():
            print("-" * 75, "***\t\t\t\t\tDados Carregados com Sucesso!!\t\t\t\t\t***", sep="\n")
            print("***\t\t\t\t\t\tReiniciando o Aplicativo\t\t\t\t\t\t***\n"
                  "***\t\tPor favor, aguarde enquanto os módulos são recarregados...\t\t***")
            self.control = Controler(300)
            self.__n = self.control.numbers
            print("-" * 75, "***\t\t\t\t\tDados Carregados com Sucesso!!\t\t\t\t\t***", sep="\n")
            stdout.flush()
            return jsonify(**{"success": True, "data": []})

        @app.route("/length", methods=["GET"])
        def length():
            data = {"length": len(self.control.numbers)}
            return jsonify(success=True,
                           data=data), 200

        @app.route("/", methods=["GET"])
        def index():
            resp = {
                "success": True,
                "data": self.control.numbers
            }
            return jsonify(**resp), 200

        @app.route("/<int:init>/<int:end>", methods=["GET"])
        def sliced(init, end):
            resp = {
                "success": False,
                "data": []
            }
            if end > init >= 0 and init < len(self.control.numbers):
                resp["success"] = True
                resp["data"] = self.control.numbers[init:end + 1]
                return jsonify(**resp), 200
            return jsonify(**resp), 404

        app.run()

    def __init__(self):
        """Método de Inicialização do View

        Método responsável inicializar o controlador e realizar interação gráfica com o administrador.
        Entradas:

        Saída:

        """
        print("-" * 71)
        print("***\t\t\t\t\t\tIniciando o Aplicativo\t\t\t\t\t\t***\n"
              "***\t\tPor favor, aguarde enquanto os módulos são carregados...\t\t***")
        self.control = Controler(300)
        print("-" * 71, "***\t\t\t\t\tDados Carregados com Sucesso!!\t\t\t\t\t***", sep="\n")
        print("***\t\t\t\t\t\tInciando o Servidor\t\t\t\t\t\t\t***", "-" * 71, sep="\n")
        stdout.flush()
        self.run()
        self.__n = self.control.numbers


if __name__ == "__main__":
    v = View()
