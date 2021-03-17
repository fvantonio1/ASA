class Notas:
    __codigomateria = None
    __idaluno = None
    __notas = None
    __situacao = None

    def __init__(self, codigomateria, idaluno, nota1, nota2, nota3, nota4):
        self.__codigomateria = codigomateria
        self.__idaluno = idaluno
        self.__notas = [nota1,nota2,nota3,nota4]
        if ((nota1+nota2+nota3+nota4) >= 60):
            self.__situacao = "APROVADO"
        else:
            self.__situacao = "REPROVADO"

    def getNotasCodigomateria(self):
        return self.__codigomateria

    def getNotasIdaluno(self):
        return self.__idaluno

    def getNotasSituacao(self):
        return self.__situacao

    def getNotasFinal(selfl):
        return self.__notas