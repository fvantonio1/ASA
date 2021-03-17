class Materia:
    __id = None
    __nome = None
    __codigo = None

    def __init__(self, id, nome, codigo):
        self.__id = id
        self.__nome = nome
        self.__codigo = codigo

    def getMateriaId(self):
        return self.__id
    
    def getMateriaNome(self):
        return self.__nome

    def getMateriaCodigo(self):
        return self.__codigo