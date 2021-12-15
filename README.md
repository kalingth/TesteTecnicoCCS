# Desafio Técnico (Dev Jr)

---
## Conceitos Aplicados

### Padrão de Projeto

Ao desenvolver esta aplicação, o padrão de projeto M.V.C. (Model View Controller) foi aplicado onde:
* A camada Model ficou responsável por coletar e organizar os dados;
* A camada View ficou responsável por implementar uma API onde serão disponibilizados os dados;
* A camada Controller ficou responsável por comunicar as camadas View e Model controlando, desta forma, as requisições que chegam ao model.

### Algoritmo de Ordenação

Neste projeto, o algoritmo escolhido foi o *[QuickSort](http://www.dsc.ufcg.edu.br/~pet/jornal/abril2013/materias/historia_da_computacao.html)* idealizado por **Charles Antony Richard Hoare**. O algoritmo implementa a ideia de dividir um problema grande e problemas menores onde, de forma recursiva, eles serão resolvidos da forma mais eficiente possível. É considero um dos algoritmos de ordenação mais utilizados no mundo.

### Bibliotecas Utilizadas

Para o desenvolvimento deste projeto foram utilizadas as seguintes bibliotecas:
#### Bibliotecas Padrões:
* concurrent
* time
* sys
#### Bibliotecas Externas:
* requests
* flask
* flask_httpauth

As bibliotecas externas podem ser instaladas a partir do arquivo requeriments.txt através do seguinte comando:
```console
>>> pip install -r requeriments.txt
```
---

### Execução

A aplicação pode ser iniciada através do seguinte comando:
```console
>>> python viewer.py
```
> **_Obs:_** Este código foi escrito em Python 3. Não é possível rodar em Python 2!

Outra forma de se incializar é importando a biblioteca e iniciando a classe View como pode ser observado abaixo:
~~~python
import viewer
viewer.View()
~~~

---

### API

A API criada utilizando o flask possui os seguintes caminhos:
* **_/_** - Lista todos os números coletados pelo model de uma vez só.
* **_/length_** - Retorna o número de itens na lista de números coletados da plataforma.
* **_/int1/int2_** - Retorna uma fatia da lista contendo os números da posição int1 até a posição int2. Este intervalo retornado é intervalo fechado.
* **_/restart_** - Método protegido por login e senha que realiza a coleta dos dados da plataforma novamente.

#### Exemplo de uma requisição bem sucedida no caminho /length
~~~json
{
  "success": true,
  "data": {
    "length": 980700
  }
}
~~~

#### Exemplo de uma requisição má sucedida
~~~json
{
  "success": false,
  "data": []
}
~~~