import json
from orientacao import Orientacao


ACENTOS = {
    "á": "a", "à": "a", "ã": "a", "â": "a",
    "é": "e", "ê": "e", "í": "i",
    "ó": "o", "õ": "o", "ô": "o",
    "ú": "u", "ç": "c"
}


def normalizar(texto):
    texto = texto.lower().strip()

    for letra, troca in ACENTOS.items():
        texto = texto.replace(letra, troca)

    for sinal in "?!.,;:()[]{}-/\\_":
        texto = texto.replace(sinal, " ")

    return " " + " ".join(texto.split()) + " "


class BaseConhecimento:
    def __init__(self, caminho):
        self.caminho = caminho
        self.orientacoes = []

    def carregar(self):
        try:
            with open(self.caminho, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)

            self.orientacoes = [
                Orientacao(**item)
                for item in dados
            ]

            return True

        except FileNotFoundError:
            print("Erro: arquivo da base de conhecimento não encontrado.")
            self.orientacoes = []
            return False

        except (json.JSONDecodeError, TypeError, KeyError):
            print("Erro: a base de conhecimento está inválida ou corrompida.")
            self.orientacoes = []
            return False

    def categorias(self):
        return sorted(set(
            orientacao.categoria
            for orientacao in self.orientacoes
        ))

    def por_categoria(self, categoria):
        return [
            orientacao
            for orientacao in self.orientacoes
            if orientacao.categoria == categoria
        ]

    def pontuar(self, pergunta, orientacao):
        pergunta_normalizada = normalizar(pergunta)
        titulo_normalizado = normalizar(orientacao.titulo)

        pontos = 0

        for palavra_chave in orientacao.palavras_chave:
            chave = normalizar(palavra_chave).strip()

            if chave and chave in pergunta_normalizada:
                pontos += 3

        palavras_pergunta = set(pergunta_normalizada.split())

        for palavra in palavras_pergunta:
            if len(palavra) >= 4 and f" {palavra} " in titulo_normalizado:
                pontos += 1

        return pontos

    def buscar(self, pergunta):
        resultados = []

        for orientacao in self.orientacoes:
            pontos = self.pontuar(pergunta, orientacao)

            if pontos >= 3:
                resultados.append((pontos, orientacao))

        resultados.sort(
            key=lambda item: item[0],
            reverse=True
        )

        return resultados
