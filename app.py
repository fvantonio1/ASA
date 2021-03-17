from flask import Flask, url_for, request, json, jsonify
from json import dumps
from aluno import Aluno
from materias import Materia
from notas import Notas

app = Flask(__name__)
alunos = []
materias = []
notas = []


@app.route('/')
def api_root():
    return 'oi'

@app.route('/relatorio')
def api_relatorio():
    return 'oii'

@app.route('/createalunos')
def api_createalunos():
    global alunos
    alunos.append(Aluno(1, "Antonio", 11711))
    alunos.append(Aluno(2, "Joao", 22411))
    res = {'status' : 'ok'}
    return jsonify(res)


@app.route('/addaluno', methods =['POST'])
def api_newaluno():
    global alunos
    req_data = request.get_json()

    id = req_data['id']
    nome = req_data['nome']
    matricula = req_data['matricula']
    new_aluno = Aluno(id, nome, matricula)
    alunos.append(new_aluno)
    res = {'status' : 'ok'}
    return jsonify(res)


@app.route('/removealuno', methods = ['DELETE'])
def api_removealuno():
    global alunos

    for elem in alunos:
        if(request.args['id'] == elem.getAlunoId()):
            alunos.remove(elem)
            res = {'status' : 'ok'}
            return jsonify(res)

    res = 'Not find ID'
    return res


@app.route('/alteraaluno', methods = ['PATCH'])
def api_alteraaluno():
    global alunos
    req_data = reques.get_json()

    id = req_data['id']
    nome = req_data['nome']
    matricula = req_data['matricula']
    updated_aluno = Aluno(id, nome, matricula)

    for elem in alunos:
        if(request.args['id'] == elem.getAlunoId()):
            alunos.remove(elem)
            alunos.append(updated_aluno)
            res = {'status' : 'ok'}
            return jsonify(res)

    res = "Not find ID"
    return res


@app.route('/listalunos', methods = ['GET'])
def api_listusers():
    global alunos
    payload = []
    content = {}

    for elem in alunos:
        content = {'id' : elem.getAlunoId(), 'nome' : str(elem.getAlunoNome()), 'matricula' : elem.getAlunoMatricula()}
        payload.append(content)
        content = {}

    res = json.dumps(payload)
    res = payload

    return jsonify(res)


@app.route('/creatematerias')
def api_creatematerias():
    global materias
    materias.append(Materia(1, "ASA", 117))
    materias.append(Materia(2, "TWM", 118))
    res = {'status' : 'ok'}
    return jsonify(res)


@app.route('/addmateria', methods = ['POST'])
def api_addmateria():
    global alunos
    req_data = request.get_json()

    id = req_data['id']
    nome = req_data['nome']
    codigo = req_data['codigo']
    new_materia = Materia(id, nome, codigo)
    materias.append(new_materia)
    res = {'status' : 'ok'}
    return res


@app.route('/listmaterias', methods = ['GET'])
def api_listmaterias():
    global materias
    payload = []
    content = {}

    for elem in materias:
        content = {'id' : elem.getMateriaId(), 'nome' : elem.getMateriaNome(), 'codigo' : elem.getMateriaCodigo()}
        payload.append(content)
        content = {}

    res = json.dumps(payload)
    res = payload

    return jsonify(res)


## @app.route('addnotas')

if __name__ == '__main__':
    app.run()
