from datetime import datetime, timedelta
import hashlib

import sqlalchemy
from sqlalchemy.sql import text
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import scoped_session, sessionmaker

from flask_login import login_user, logout_user

from models import Reserva, Aeroporto, Voo, Cadastro, Base
from settings import DATABASE_URL

print(DATABASE_URL)

engine = create_engine(DATABASE_URL, convert_unicode=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    if not database_exists(engine.url):
        create_database(engine.url)
        print('Base de dados criada com sucesso')
    else:
        print('Base de dados já foi criada')
        engine.connect()

def init_tables():
    if (sqlalchemy.inspect(engine).has_table('reserva')):
        print('Tables already exists')
        ret = {'status' : 'Tables already exists'}
    else:
        import models
        Base.metadata.create_all(bind=engine)
        print('Tables has been created')
        ret = {'status' : 'Tables has been created'}
    return ret


####################### AEROPORTO ##########################
def populate_aeroporto(aeroportos):
    return [
        {"id": aeroporto.id, "nome": aeroporto.nome, "cidade": aeroporto.cidade}
        for aeroporto in aeroportos
    ]

def hw_add_aeroporto(request):
    session = SessionLocal()
    aeroporto = Aeroporto(nome=request["nome"], cidade=request["cidade"])
    # aeroporto_json = populate_aeroporto([aeroporto])
    session.add(aeroporto)
    session.commit()
    aeroporto_json = hw_get_aeroporto(aeroporto.id)
    session.close()
    return aeroporto_json

def hw_get_aeroportos():
    session = SessionLocal()
    aeroportos = session.query(Aeroporto).order_by(Aeroporto.nome.asc()).all()
    aeroportos_json = populate_aeroporto(aeroportos)
    session.close()
    return aeroportos_json

def hw_get_aeroporto(id):
    session = SessionLocal()
    aeroporto = session.query(Aeroporto).filter_by(id=id).all()
    aeroporto_json = populate_aeroporto(aeroporto)
    session.close()
    return aeroporto_json

def hw_remove_aeroporto(id):
    session = SessionLocal()
    aeroporto = session.query(Aeroporto).filter_by(id=id).first()
    session.delete(aeroporto)
    session.commit()
    session.close()
    return {"message": f"Aeroporto {aeroporto.id} was deleted"}

def hw_update_aeroporto(request):
    session = SessionLocal()
    aeroporto_old = session.query(Aeroporto).filter_by(id=request["id"]).first()
    session.delete(aeroporto_old)
    aeroporto = Aeroporto(
        id=request["id"], nome=request["nome"], cidade=request["cidade"]
    )
    session.add(aeroporto)
    session.commit()
    aeroporto_json = hw_get_aeroporto(aeroporto.id)
    session.close()
    return aeroporto_json

def hw_get_aeroportos_destino(origem):
    session = SessionLocal()
    voo_origem = (
        session.query(Voo).join(Aeroporto).filter(Aeroporto.cidade == origem).all()
    )
    voo_origem_json = populate_voo_aeroporto(voo_origem)
    destinos = [{"destino": elem["destino"]} for elem in voo_origem_json]
    return destinos


####################### VOO ##########################
def populate_voo(voos):
    return [
        {
            "id": voo.id,
            "data": datetime.strftime(voo.data, "%d/%m/%Y %H:%M:%S"),
            "destino": voo.destino,
            "companhia": voo.companhia,
            "capacidade": voo.capacidade,
            "ocupacao": voo.ocupacao,
            "preco": voo.preco,
            "id_aeroporto": voo.id_aeroporto,
        }
        for voo in voos
    ]

def populate_voo_aeroporto(voos):
    return [
        {
            "id": voo.id,
            "data": datetime.strftime(voo.data, "%d/%m/%Y %H:%M:%S"),
            "destino": voo.destino,
            "companhia": voo.companhia,
            "capacidade": voo.capacidade,
            "ocupacao": voo.ocupacao,
            "preco": voo.preco,
            "id_aeroporto": voo.id_aeroporto,
            "aeroporto": populate_aeroporto([voo.aeroporto]),
        }
        for voo in voos
    ]

def hw_add_voo(request):
    session = SessionLocal()
    voo = Voo(
        data=datetime.strptime(request["data"], "%d/%m/%Y %H:%M:%S"),
        destino=request["destino"],
        companhia=request["companhia"],
        capacidade=request["capacidade"],
        ocupacao=request["ocupacao"],
        preco=request["preco"],
        id_aeroporto=request["id_aeroporto"],
    )
    session.add(voo)
    session.commit()
    voo_json = hw_get_voo(voo.id)
    session.close()
    return voo_json

def hw_get_voos():
    session = SessionLocal()
    voos = session.query(Voo).order_by(Voo.data.asc()).all()
    voos_json = populate_voo(voos)
    session.close()
    return voos_json

def hw_get_voos_aeroportos():
    session = SessionLocal()
    voos = session.query(Voo).order_by(Voo.data.asc()).all()
    voos_json = populate_voo_aeroporto(voos)
    session.close()
    return voos_json

def hw_get_voo(id):
    session = SessionLocal()
    voo = session.query(Voo).filter_by(id=id).all()
    voo_json = populate_voo(voo)
    session.close()
    return voo_json

def hw_remove_voo(id):
    session = SessionLocal()
    voo = session.query(Voo).filter_by(id=id).first()
    session.delete(voo)
    session.commit()
    session.close()
    return {"message": f"Voo {voo.id} was deleted"}

def hw_update_voo(request):
    session = SessionLocal()
    voo_old = session.query(Voo).filter_by(id=request["id"]).first()
    session.delete(voo_old)
    voo = Voo(
        id=request["id"],
        data=datetime.strptime(request["data"], "%d/%m/%Y %H:%M:%S"),
        destino=request["destino"],
        companhia=request["companhia"],
        capacidade=request["capacidade"],
        ocupacao=request["ocupacao"],
        preco=request["preco"],
    )
    session.add(voo)
    session.commit()
    voo_json = hw_get_voo(voo.id)
    session.close()
    return voo_json

def hw_get_aeroporto_by_company(company):
    session = SessionLocal()
    voos_company = session.query(Voo).filter_by(companhia=company).all()

    voos_company_json = populate_voo_aeroporto(voos_company)
    cidades_destino = [elem["aeroporto"][0] for elem in voos_company_json]
    session.close()
    return cidades_destino

def hw_get_voos_companhia(request):
    session = SessionLocal()
    date = datetime.strptime(request["data"] + " 00:00:00", "%d/%m/%Y %H:%M:%S")
    time_after = date + timedelta(hours=23, minutes=59, seconds=59)
    voos = (
        session.query(Voo)
        .filter(Voo.data >= date, Voo.data <= time_after)
        .filter_by(companhia=request["companhia"])
        .all()
    )
    voos_json = populate_voo_aeroporto(voos)
    session.close()
    return voos_json

def hw_get_voos_passageiros(n):
    session = SessionLocal()
    voos_disponibilidade = (
        session.query(Voo, (Voo.capacidade - Voo.ocupacao).label("disponibilidade"))
        .filter(text(f"disponibilidade > {n}"))
        .order_by(Voo.preco.asc())
        .all()
    )
    voo_list = [voo[0] for voo in voos_disponibilidade]
    voos_json = populate_voo_aeroporto(voo_list)
    session.close()
    return voos_json


####################### LOGIN ##########################
def populate_cadastro(cadastros):
    return [
        {
            "id": cadastro.id,
            "nome": cadastro.nome,
            "email": cadastro.email,
            "senha": cadastro.senha,
        }
        for cadastro in cadastros
    ]

def hw_load_user(id):
    session = SessionLocal()
    return session.query(Cadastro).filter_by(id=id).first()

def hw_get_cadastros():
    session = SessionLocal()
    cadastros = session.query(Cadastro).order_by(Cadastro.nome.asc()).all()
    cadastros_json = populate_cadastro(cadastros)
    session.close()
    return cadastros_json

def hw_add_cadastro(request):
    session = SessionLocal()
    senha = request["senha"]
    hash_obj = hashlib.md5(f"{senha}".encode())
    md5_value = hash_obj.hexdigest()
    cadastro = Cadastro(nome=request["nome"], email=request["email"], senha=md5_value)
    cadastro_json = populate_cadastro([cadastro])
    session.add(cadastro)
    session.commit()
    session.close()
    return cadastro_json

def hw_login(request):
    session = SessionLocal()
    senha = request["senha"]
    hash_obj = hashlib.md5(f"{senha}".encode())
    md5_value = hash_obj.hexdigest()
    user = (
        session.query(Cadastro)
        .filter_by(email=request["email"], senha=md5_value)
        .first()
    )
    login_user(user)
    session.close()
    return "Voce entrou"

def hw_logout():
    session = SessionLocal()
    logout_user()
    return "Voce saiu"


####################### RESERVA ##########################
def populate_reserva(reservas):
    return [
        {
            "id": reserva.id,
            "id_voo": reserva.id_voo,
            "id_cadastro": reserva.id_cadastro,
            "e_ticket": None if reserva.e_ticket is None else reserva.e_ticket,
            "voo": populate_voo_aeroporto([reserva.voo]),
            "cadastro": populate_cadastro([reserva.cadastro]),
        }
        for reserva in reservas
    ]

def hw_add_reserva(request):
    session = SessionLocal()
    reserva = Reserva(id_voo=request["id_voo"], id_cadastro=request["id_cadastro"])
    session.add(reserva)
    session.commit()
    hash_obj = hashlib.md5(f"{reserva.id}".encode())
    md5_value = hash_obj.hexdigest()
    reserva.e_ticket = md5_value
    session.add(reserva)
    session.commit()
    reserva_json = hw_get_reserva(reserva.id)
    session.close()
    return reserva_json

def hw_get_reservas():
    session = SessionLocal()
    reservas = session.query(Reserva).all()
    reserva_json = populate_reserva(reservas)
    return reserva_json

def hw_remove_reserva(id):
    session = SessionLocal()
    reserva = session.query(Reserva).filter_by(id=id).first()
    session.delete(reserva)
    session.commit()
    session.close()
    return {"message": f"Reserva {reserva.id} was deleted"}

def hw_update_reserva(request):
    session = SessionLocal()
    reserva_old = session.query(Reserva).filter_by(id=request["id"]).first()
    session.delete(reserva_old)
    reserva = Reserva(
        id_voo=request["id_voo"],
        id_cadastro=request["id_cadastro"],
        e_ticket=request["e_ticket"],
    )
    session.add(reserva)
    session.commit()
    reserva_json = hw_get_reserva(reserva.id)
    session.close()
    return reserva_json

def hw_get_reserva(id):
    session = SessionLocal()
    reserva = session.query(Reserva).filter_by(id=id).first()
    reserva_json = populate_reserva([reserva])
    return reserva_json