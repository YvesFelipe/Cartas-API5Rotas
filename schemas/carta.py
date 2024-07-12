from pydantic import BaseModel
from typing import Optional, List
from model.Cartas import Cartas

#from schemas import ComentarioSchema


class CartasSchema(BaseModel):
    """ Define como uma nova carta a ser inserida deve ser representada
    """
    nome_carta: str = ""
    nome_edicao: str = ""
    quantidade_copia: int = ""
    qualidade : str = ""
    idioma : str = ""
    extra : str = ""
    rotacao : str = ""


class CartasBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base nas cinco colunas principais.
    """
    nome_carta: str = ""
    nome_edicao: str = ""
    qualidade : str = ""
    idioma : str = ""
    extra : str = ""

class CartaAlteraSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita com base nas colunas que definem uma entrada única.
    """
    nome_carta: str = ""
    nome_edicao: str = ""
    qualidade : str = ""
    idioma : str = ""
    extra : str = ""
    quantidade_copia: int = ""


class ListagemCartasSchema(BaseModel):
    """ Define como uma listagem de cartas será retornada.
    """
    produtos:List[CartasSchema]


def apresenta_cartas(cartas: List[Cartas]):
    """ Retorna uma representação da carta seguindo o schema definido em
        CartaViewSchema.
    """
    result = []
    for carta in cartas:
        result.append({
            "nome_carta": carta.nome_carta ,
            "nome_edicao": carta.nome_edicao ,
            "quantidade_copia": carta.quantidade_copia ,
            "qualidade" : carta.qualidade ,
            "idioma" : carta.idioma ,
            "extra" : carta.extra ,
            "rotacao" : carta.rotacao ,
        })

    return {"Cartas": result}


class CartaViewSchema(BaseModel):
    """ Define como a carta será retornada
    """
    id: int = 1
    nome_carta: str = ""
    nome_edicao: str = ""
    quantidade_copia: int = ""
    qualidade : str = ""
    idioma : str = ""
    extra : str = ""
    rotacao : str = ""
   

class CartaDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    nome_carta: str

def apresenta_carta(carta: Cartas):
    """ Retorna uma representação da carta seguindo o schema definido em
        CartaViewSchema.
    """
    return {
        "id": carta.id,
        "nome_carta": carta.nome_carta ,
        "nome_edicao": carta.nome_edicao ,
        "quantidade_copia": carta.quantidade_copia ,
        "qualidade" : carta.qualidade ,
        "idioma" : carta.idioma ,
        "extra" : carta.extra ,
        "rotacao" : carta.rotacao ,
    }
