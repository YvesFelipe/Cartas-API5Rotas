# Minha API

Este pequeno projeto faz parte da entrega do MVP da Pós de Engenharia de Software, da Sprint de Desenvolvimento Full Stack Básico. Nas próximas linhas irei dar uma breve visão do que foi projetado no meu back-end e no banco de dados.

O objetivo deste projeto foi a criação de uma SPA que funcione como uma ajuda a uma pessoa que colecione MTG(Magig The Gathering), um jogo de cartas, possibilitando assim um melhor controle de quais cartas a pessoa tem em sua coleção.

Para começar foi criado um banco de dados em SQLite contendo sete colunas, sendo elas o nome da carta, a edição em que ela foi lançada, a quantidade de cópias, a qualidade em que se encontra a carta, o idioma, se ela possui algo extra em sua ilustração e se é possível usar na rotação atual. Como é possível que todas essas colunas se repitam foi utilizado também uma UniqueConstraint com as colunas de nome, edição, qualidade, idioma e extra para que todos essas informações juntas indentificassem uma entrada única.

Após isso foi criado a API e três rotas que seriam necessárias para o projeto sendo elas a /adicionacarta, /buscacartas e /deletacarta.

A rota /adicionacarta, como o próprio nome sugere, serve para quando o usuário colocar os dados na SPA e clicar no botão adicionar seja possível colocar os dados da carta na base de dados criada. Já a de /buscacartas serve para pegar todas as cartas que estão no banco de dados e assim ser possível mostrá-las na página criada.

A rota /deletacarta que serve para deletar uma carta especifica do banco de dados e por conta disso precisa de todos os valores das colunas que compõem  a UniqueConstraint criada anteriormente para que assim seja excluída somente a entrada desejada.

A rota /alteracarta serve para alterar a quantidade de cópias de uma carta definida pelas colunas que compõem a UniqueConstraint. E por último temos a rota /buscacarta que serve para buscar uma carta especifica no banco de dados a partir das colunas que compões o UniqueConstraint.

---
## Como executar 


Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.
Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

```
(env)$ pip install -r requirements.txt
```

Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.

Para executar a API  basta executar:

```
(env)$ flask run --host 0.0.0.0 --port 5000
```

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte. 

```
(env)$ flask run --host 0.0.0.0 --port 5000 --reload
```

Abra o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução.


## Como executar através do Docker

Certifique-se de ter o Docker instalado e em execução em sua máquina.

Navegue até o diretório que contém o Dockerfile e o requirements.txt no terminal. Execute como administrador o seguinte comando para construir a imagem Docker:

```
$ docker build -t rest-api .
```
Uma vez criada a imagem, para executar o container basta executar, como administrador, seguinte o comando:

```
$ docker run -p 5000:5000 rest-api
```
Uma vez executando, para acessar a API, basta abrir o http://localhost:5000/#/ no navegador.

