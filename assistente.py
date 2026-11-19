import csv
import json
import os
import time
from datetime import datetime


class Assistente:
    def __init__(self, nome, base, caminho_historico="data/historico.json"):
        self.nome = nome
        self.base = base
        self.caminho_historico = caminho_historico
        self.historico = []
        self.carregar_historico()

    def carregar_historico(self):
        try:
            with open(self.caminho_historico, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)

            if isinstance(dados, list):
                self.historico = dados
            else:
                self.historico = []

        except (FileNotFoundError, json.JSONDecodeError):
            self.historico = []

    def salvar_historico(self):
        os.makedirs(os.path.dirname(self.caminho_historico), exist_ok=True)

        with open(self.caminho_historico, "w", encoding="utf-8") as arquivo:
            json.dump(
                self.historico,
                arquivo,
                ensure_ascii=False,
                indent=2
            )

    def tem_dado_pessoal(self, texto):
        quantidade_digitos = sum(
            caractere.isdigit()
            for caractere in texto
        )

        return quantidade_digitos >= 8 or "@" in texto

    def registrar(self, origem, pergunta, orientacao_id,
                  encontrou, ajudou, tentativas, tempo_segundos):
        registro = {
            "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "origem": origem,
            "pergunta": pergunta,
            "id_orientacao": orientacao_id,
            "encontrou": encontrou,
            "ajudou": ajudou,
            "tentativas": tentativas,
            "tempo_segundos": tempo_segundos
        }

        self.historico.append(registro)
        self.salvar_historico()

    def perguntar_sim_nao(self, mensagem):
        while True:
            resposta = input(mensagem).strip().lower()

            if resposta in ["s", "n"]:
                return resposta == "s"

            print("Digite somente s ou n.")

    def perguntar(self):
        inicio = time.time()
        tentativas = 0

        while True:
            pergunta = input("\nDigite sua dúvida (0 para voltar): ").strip()

            if pergunta == "0":
                return

            if not pergunta:
                print("A pergunta não pode ficar vazia.")
                continue

            if self.tem_dado_pessoal(pergunta):
                print(
                    "Atenção: não digite CPF, telefone ou e-mail. "
                    "Reescreva sua dúvida sem dados pessoais."
                )
                continue

            tentativas += 1
            resultados = self.base.buscar(pergunta)

            if not resultados:
                print("\nNão encontrei uma orientação para essa dúvida.")
                print("Tente usar outras palavras ou consulte as categorias.")

                categorias = ", ".join(self.base.categorias())
                print(f"Categorias disponíveis: {categorias}")

                tentar_novamente = self.perguntar_sim_nao(
                    "Quer tentar escrever a dúvida de outro jeito? (s/n): "
                )

                if tentar_novamente:
                    continue

                tempo = round(time.time() - inicio, 1)

                self.registrar(
                    "pergunta",
                    pergunta,
                    None,
                    False,
                    False,
                    tentativas,
                    tempo
                )
                return

            pontos, melhor = resultados[0]

            if pontos >= 6:
                confianca = "ALTA"
            else:
                confianca = "MÉDIA"

            print(f"\nConfiança da resposta: {confianca} ({pontos} pontos)")
            melhor.exibir()

            if len(resultados) > 1:
                print("\nOutras orientações relacionadas:")
                for pontos_alt, orientacao_alt in resultados[1:3]:
                    print(
                        f"- {orientacao_alt.titulo} "
                        f"({pontos_alt} pontos)"
                    )

            ajudou = self.perguntar_sim_nao(
                "\nEssa orientação respondeu sua dúvida? (s/n): "
            )

            tempo = round(time.time() - inicio, 1)

            self.registrar(
                "pergunta",
                pergunta,
                melhor.id,
                True,
                ajudou,
                tentativas,
                tempo
            )
            return

    def navegar(self):
        inicio = time.time()

        while True:
            categorias = self.base.categorias()

            if not categorias:
                print("Nenhuma categoria disponível.")
                return

            print("\nCATEGORIAS")
            for indice, categoria in enumerate(categorias, start=1):
                print(f"{indice} - {categoria}")
            print("0 - Voltar")

            escolha = input("Escolha uma categoria: ").strip()

            if escolha == "0":
                return

            if not escolha.isdigit():
                print("Digite o número de uma categoria.")
                continue

            numero = int(escolha)

            if numero < 1 or numero > len(categorias):
                print("Opção fora da faixa.")
                continue

            categoria = categorias[numero - 1]
            orientacoes = self.base.por_categoria(categoria)

            while True:
                print(f"\n{categoria.upper()}")

                for indice, orientacao in enumerate(orientacoes, start=1):
                    print(f"{indice} - {orientacao.titulo}")

                print("0 - Voltar")

                escolha_orientacao = input(
                    "Escolha uma orientação: "
                ).strip()

                if escolha_orientacao == "0":
                    break

                if not escolha_orientacao.isdigit():
                    print("Digite o número de uma orientação.")
                    continue

                numero_orientacao = int(escolha_orientacao)

                if (
                    numero_orientacao < 1
                    or numero_orientacao > len(orientacoes)
                ):
                    print("Opção fora da faixa.")
                    continue

                orientacao = orientacoes[numero_orientacao - 1]
                orientacao.exibir()

                ajudou = self.perguntar_sim_nao(
                    "\nEssa orientação respondeu sua dúvida? (s/n): "
                )

                tempo = round(time.time() - inicio, 1)

                self.registrar(
                    "categoria",
                    orientacao.titulo,
                    orientacao.id,
                    True,
                    ajudou,
                    1,
                    tempo
                )
                return

    def indicadores(self):
        if not self.historico:
            print("\nAinda não existem atendimentos registrados.")
            return

        total = len(self.historico)
        encontrados = sum(
            1 for item in self.historico
            if item.get("encontrou")
        )
        ajudaram = sum(
            1 for item in self.historico
            if item.get("ajudou")
        )

        tempo_medio = sum(
            item.get("tempo_segundos", 0)
            for item in self.historico
        ) / total

        tentativas_media = sum(
            item.get("tentativas", 0)
            for item in self.historico
        ) / total

        notas = [
            item["facilidade"]
            for item in self.historico
            if "facilidade" in item
        ]

        sem_solucao = [
            item.get("pergunta", "")
            for item in self.historico
            if not item.get("encontrou")
        ]

        print("\nINDICADORES")
        print(
            f"Resposta encontrada: "
            f"{(encontrados / total) * 100:.1f}%"
        )
        print(
            f"Taxa de acerto (ajudou): "
            f"{(ajudaram / total) * 100:.1f}%"
        )
        print(
            f"Tempo médio para encontrar: "
            f"{tempo_medio:.1f} segundos"
        )
        print(
            f"Tentativas por atendimento: "
            f"{tentativas_media:.1f}"
        )

        if notas:
            print(
                f"Facilidade de uso: "
                f"{sum(notas) / len(notas):.1f} de 5"
            )
        else:
            print("Facilidade de uso: ainda sem avaliações")

        if sem_solucao:
            print("\nDúvidas sem solução:")
            for pergunta in sem_solucao:
                print(f"- {pergunta}")
        else:
            print("\nDúvidas sem solução: nenhuma")

    def avaliar_facilidade(self):
        if not self.historico:
            return

        while True:
            nota = input(
                "\nDe 1 a 5, qual a facilidade de uso? "
            ).strip()

            if nota.isdigit() and 1 <= int(nota) <= 5:
                self.historico[-1]["facilidade"] = int(nota)
                self.salvar_historico()
                print("Obrigado pela avaliação!")
                return

            print("Digite uma nota de 1 a 5.")

    def exportar_csv(self, caminho="data/atendimentos.csv"):
        campos = [
            "data",
            "origem",
            "pergunta",
            "id_orientacao",
            "encontrou",
            "ajudou",
            "tentativas",
            "tempo_segundos",
            "facilidade"
        ]

        os.makedirs(os.path.dirname(caminho), exist_ok=True)

        with open(caminho, "w", newline="", encoding="utf-8-sig") as arquivo:
            escritor = csv.DictWriter(
                arquivo,
                fieldnames=campos,
                extrasaction="ignore"
            )
            escritor.writeheader()

            for item in self.historico:
                linha = item.copy()
                linha.setdefault("facilidade", "")
                escritor.writerow(linha)

        print(f"CSV exportado para {caminho}")
