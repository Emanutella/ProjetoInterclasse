import os
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, scoped_session


engine = create_engine("mysql+pymysql://root:senaisp@localhost:3306/INTERCLASSE_DB")
db_session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()

class Time(Base):
    __tablename__ = "times"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    turma = Column(String(20))
    responsavel = Column(String(100))


class Jogador(Base):
    __tablename__ = "jogadores"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    numero_camisa = Column(Integer)
    posicao = Column(String(50))
    time_id = Column(Integer, ForeignKey("times.id", ondelete="SET NULL"))

class Partida(Base):
    __tablename__ = "partidas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    time_casa_id = Column(Integer, ForeignKey("times.id", ondelete="CASCADE"), nullable=False)
    time_visitante_id = Column(Integer, ForeignKey("times.id", ondelete="CASCADE"), nullable=False)
    gols_casa = Column(Integer, default=0)
    gols_visitante = Column(Integer, default=0)
    data_partida = Column(Date)


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)

