from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import relationship
from typing import Union

from  model import Base


class Cartas(Base):
    __tablename__ = 'Cartas'

    id = Column("pk_cartas", Integer, primary_key=True)
    nome_carta = Column(String)
    nome_edicao = Column(String)
    quantidade_copia = Column(Integer, nullable=False)
    qualidade = Column(String, nullable=False)
    idioma = Column(String, nullable=False)
    extra = Column(String, nullable=False)
    rotacao = Column(String, nullable=False)
    UniqueConstraint(nome_carta, nome_edicao, qualidade, idioma, extra)

    def __init__(self, nome_carta:str, nome_edicao:str, quantidade_copia:int,
                 qualidade:str, idioma:str, extra:str, rotacao:str):
        """
        Cria um Produto

        Arguments:
            nome_carta: nome da carta.
            nome_edicao: nome da edição que a carta foi lançada
            quantidade_copia: quantidade de copias dessa carta
            qualidade : Estado da carta 
            idioma = Linguaguem da carta
            extra = Efeitos especiais da carta(Ex:Foil)
            rotacao = Se ela é permitida na rotação atual do jogo
        """
        self.nome_carta = nome_carta
        self.nome_edicao = nome_edicao
        self.quantidade_copia = quantidade_copia
        self.qualidade = qualidade
        self.idioma = idioma
        self.extra = extra
        self.rotacao = rotacao


       
