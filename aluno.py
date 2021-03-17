class Aluno:
    __id = None
    __nome = None
    __matricula = None 

    def __init__(self, id, nome, matricula):
        self.__id = id
        self.__nome = nome
        self.__matricula = matricula
        
    def getAlunoNome(self):
        return self.__nome

    def getAlunoMatricula(self):
        return self.__matricula

    def getAlunoId(self):
        return self.__id