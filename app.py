from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect, request
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Cartas
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
carta_tag = Tag(name="Carta", description="Adição, visualização e remoção de cartas à base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/adicionacarta', tags=[carta_tag],
          responses={"200": CartaViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_carta(form: CartasSchema):
    """Adiciona uma nova Carta à base de dados

    Retorna uma representação da carta.
    """
    # criando conexão com a base
    session = Session()
    carta = Cartas(
        nome_carta = form.nome_carta ,
        nome_edicao = form.nome_edicao ,
        quantidade_copia = form.quantidade_copia ,
        qualidade = form.qualidade ,
        idioma = form.idioma ,
        extra = form.extra ,
        rotacao = form.rotacao ,
        )  
    logger.debug(f"Adicionando carta de nome: '{carta.nome_carta}'")
    try:
        
        # adicionando carta
        session.add(carta)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionada carta de nome: '{carta.nome_carta}'")
        return apresenta_carta(carta), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Carta com mesmas características já salva na base :/"
        logger.warning(f"Erro ao adicionar carta '{carta.nome_carta}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar carta '{carta.nome_carta}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.get('/buscacartas', tags=[carta_tag],
         responses={"200": ListagemCartasSchema, "404": ErrorSchema})
def get_cartas():
    """Faz a busca por todos as Cartas cadastradas

    Retorna uma representação da listagem de cartas.
    """
    logger.debug(f"Coletando cartas ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    cartas = session.query(Cartas).all()

    if not cartas:
        # se não há cartas cadastradas
        return {"cartas": []}, 200
    else:
        logger.debug(f"%d cartas encontradas" % len(cartas))
        # retorna a representação de carta
        print(cartas)
        return apresenta_cartas(cartas), 200





@app.delete('/deletacarta', tags=[carta_tag],
            responses={"200": CartaDelSchema, "404": ErrorSchema})
def del_carta(query: CartasBuscaSchema):
    """Deleta uma carta a partir das informações da carta

    Retorna uma mensagem de confirmação da remoção.
    """
    carta_nome = unquote(unquote(query.nome_carta))
    carta_edicao = unquote(unquote(query.nome_edicao))
    carta_qualidade = unquote(unquote(query.qualidade))
    carta_idioma = unquote(unquote(query.idioma))
    carta_extra = unquote(unquote(query.extra))
    print(carta_nome)
    logger.debug(f"Deletando dados sobre a carta {carta_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Cartas).filter(Cartas.nome_carta == carta_nome, Cartas.nome_edicao == carta_edicao,
                                         Cartas.qualidade == carta_qualidade, Cartas.idioma == carta_idioma,
                                         Cartas.extra == carta_extra).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Carta deletada: #{carta_nome}")
        return {"mesage": "Carta removida", "id": carta_nome}
    else:
        # se a carta não foi encontrada
        error_msg = "Carta não encontrada na base :/"
        logger.warning(f"Erro ao deletar carta '{carta_nome}', {error_msg}")
        return {"mesage": error_msg}, 404

@app.get('/buscacarta', tags=[carta_tag],
         responses={"200": CartaViewSchema, "404": ErrorSchema})
def get_carta(query: CartasBuscaSchema):
    """Faz a busca por todos as Cartas cadastradas com o mesmo nome

    Retorna uma representação da listagem de cartas.
    """
    nome_carta = request.args.get('nome_carta')

    nome_carta = query.nome_carta
    nome_edicao = query.nome_edicao
    qualidade = query.qualidade
    idioma = query.idioma
    extra = query.extra
    logger.debug(f"Coletando todas as cartas com o nome #{nome_carta}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    carta = session.query(Cartas).filter(Cartas.nome_carta == nome_carta, Cartas.nome_edicao == nome_edicao,
                                         Cartas.qualidade == qualidade, Cartas.idioma == idioma,
                                         Cartas.extra == extra).first()

    if not carta:
        # se nenhuma carta for encontrada
        error_msg = "Nenhuma carta com esse nome encontrada na base :/"
        logger.warning(f"Erro ao buscar carta com o nome '{nome_carta}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Cartas encontradas!")
        # retorna a representação da carta
        return apresenta_carta(carta), 200
    


@app.put('/alteracarta', tags=[carta_tag],
         responses={"200": CartaViewSchema, "404": ErrorSchema})
def altera_carta(query: CartaAlteraSchema):
    """Busca uma carta e alterar a partir de suas colunas principais

    Retorna uma representação da carta modificada
    """
    nome_carta = query.nome_carta
    nome_edicao = query.nome_edicao
    qualidade = query.qualidade
    idioma = query.idioma
    extra = query.extra
    quantidade_copia = query.quantidade_copia

    logger.debug(f"Coletando informações da carta com o nome #{nome_carta}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    carta = session.query(Cartas).filter(Cartas.nome_carta == nome_carta, Cartas.nome_edicao == nome_edicao,
                                         Cartas.qualidade == qualidade, Cartas.idioma == idioma,
                                         Cartas.extra == extra).first()

    if not carta:
        # se nenhuma carta for encontrada
        error_msg = "Nenhuma carta com esse nome encontrada na base :/"
        logger.warning(f"Erro ao buscar carta com o nome '{nome_carta}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Carta encontrada!")

        if quantidade_copia == "" :
            error_msg = "Favor preencher o campo 'Quantidade' com um número."
            logger.warning(f"{error_msg} Livro: '{carta.nome_carta}'")
            return {"message": error_msg}, 400
        else :
            carta.quantidade_copia = quantidade_copia

    try:
        session.commit()
        logger.debug(f"Carta '{carta.nome_carta}' atualizado com sucesso")
        return apresenta_carta(carta), 200
    
    except Exception as e:
        error_msg = "Não foi possível atualizar a carta na base :/"
        logger.warning(f"Erro ao atualizar livro '{carta.nome_carta}', {error_msg}")
        return {"message": error_msg}, 400
