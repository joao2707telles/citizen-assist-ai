# Citizen Assist AI - Primeiro Emprego

## Integrantes
- João Augusto Poloniato Telles - RM 571443
- Lais da Silva Dias - RM 569943

## Público e problema escolhido
O público escolhido foi **jovens entrando no mercado de trabalho**.

A ideia do projeto é reunir orientações simples sobre documentos, primeiro emprego,
serviços digitais e alguns direitos do trabalhador. O assistente não consulta cadastros
e não pede dados pessoais.

## ODS relacionados
- **ODS 4 - Educação de Qualidade:** ajuda o usuário a entender informações importantes.
- **ODS 8 - Trabalho Decente e Crescimento Econômico:** o projeto trata de primeiro emprego e direitos trabalhistas.
- **ODS 10 - Redução das Desigualdades:** facilita o acesso a informações públicas.

## Como executar

É necessário ter Python 3 instalado.

No terminal, entre na pasta do projeto e execute:

```bash
python main.py
```

Não foram usadas bibliotecas externas.

## Estrutura do projeto

```text
citizen-assist-ai/
├── README.md
├── main.py
├── orientacao.py
├── base_conhecimento.py
├── assistente.py
└── data/
    ├── base_conhecimento.json
    ├── historico.json
    └── atendimentos.csv
```

## Como a busca funciona

A pergunta é normalizada antes da comparação: fica em minúsculas, sem acentos e
sem alguns sinais de pontuação.

A pontuação usada foi:

- palavra-chave encontrada na pergunta: **+3 pontos**;
- palavra da pergunta com 4 letras ou mais encontrada no título: **+1 ponto**;
- 6 pontos ou mais: **confiança ALTA**;
- entre 3 e 5 pontos: **confiança MÉDIA**;
- abaixo de 3 pontos: o sistema informa que não encontrou uma orientação.

O método `buscar()` devolve uma lista de tuplas no formato
`(pontos, orientacao)`, ordenada da maior para a menor pontuação.

## Classes

### Orientacao
Representa uma orientação carregada do JSON e possui o método `exibir()`.

### BaseConhecimento
Carrega o JSON, lista categorias, filtra orientações por categoria, calcula a
pontuação e realiza a busca.

### Assistente
Conversa com o usuário, registra o histórico, calcula indicadores e exporta o CSV.

As classes usam composição: o `Assistente` possui uma `BaseConhecimento`, que por
sua vez possui uma lista de objetos `Orientacao`.

## Proteção de dados pessoais

O programa não pede nome, CPF, telefone ou e-mail.

Se uma pergunta tiver 8 ou mais dígitos ou contiver `@`, ela é recusada e não é
registrada no histórico.

## Base de conhecimento

A base possui **10 orientações**, distribuídas em 4 categorias:

- Documentos
- Primeiro emprego
- Direitos do trabalhador
- Serviços digitais

Todas as orientações possuem fonte oficial e data de verificação.

## Fontes consultadas

- Ministério do Trabalho e Emprego / gov.br
- Receita Federal / gov.br
- Tribunal Superior Eleitoral
- Ministério da Defesa / gov.br
- Ministério do Desenvolvimento e Assistência Social / gov.br

As URLs completas estão em `data/base_conhecimento.json`.

## Histórico, indicadores e CSV

Cada atendimento registra:
- data;
- origem;
- pergunta;
- id da orientação;
- se encontrou resposta;
- se ajudou;
- quantidade de tentativas;
- tempo em segundos.

Ao sair, o usuário dá uma nota de facilidade de 1 a 5.

O sistema calcula:
- percentual de respostas encontradas;
- taxa de acerto;
- tempo médio;
- média de tentativas;
- facilidade de uso;
- dúvidas sem solução.

Os atendimentos podem ser exportados para `data/atendimentos.csv`.

## Teste com usuários

**Esta parte deve ser preenchida após o teste real com pelo menos 3 pessoas de fora
da equipe, totalizando 10 atendimentos ou mais. Não registrar nomes.**

Indicadores do teste:
- Resposta encontrada: [PREENCHER]
- Taxa de acerto: [PREENCHER]
- Tempo médio: [PREENCHER]
- Tentativas por atendimento: [PREENCHER]
- Facilidade de uso: [PREENCHER]
- Dúvidas sem solução: [PREENCHER]

Melhoria feita depois do teste:
- [PREENCHER COM UMA MELHORIA REAL, por exemplo uma nova palavra-chave]

## Limitações

O assistente usa busca por regras e não entende a pergunta como uma IA generativa.
Por isso, uma pergunta escrita de um jeito muito diferente das palavras-chave pode
não ser encontrada.

A base também é pequena e contém apenas os assuntos cadastrados no JSON.

O assistente não consulta situação de documentos, cadastros pessoais ou sistemas
externos.

## Vídeo

Link do vídeo técnico no YouTube:
[PREENCHER]
