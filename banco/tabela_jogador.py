from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError
from flask import flash
from database import Jogador, db_session, Time



def select_todos_jogadores():
    #Montar o Select
    #join(Tabela que quero juntar, condição=chave estrangeira igual chave primária)
    jogadores_sql = select(Jogador, Time).join(Time, Jogador.time_id == Time.id)
    #Executar o select
    #usar scalars quando tiver somente uma tabela
    jogadores = db_session.execute(jogadores_sql).all()
    return jogadores

def select_quantidade_total():
    jogadores_sql = select(func.count(Jogador.id))
    quantidade_total = db_session.execute(jogadores_sql).scalar()
    return quantidade_total
print(select_quantidade_total())

def salvar(nome, time_id, numero_camisa, posicao):
    try:
        novo_jogador = Jogador(nome=nome,time_id=time_id , numero_camisa=numero_camisa, posicao=posicao)
        db_session.add(novo_jogador)
        db_session.commit()
        flash("Jogador salvo com sucesso!", "success")
    except SQLAlchemyError as e:
        db_session.rollback()
        flash("Houve um erro. Tente novamente", "error")
        print(f"{e}")
    except Exception as e:
        db_session.rollback()
        flash("Houve um erro. Tente novamente", "error")
        print(f"{e}")