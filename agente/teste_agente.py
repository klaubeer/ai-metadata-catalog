def main():

    agente = criar_agente()

    while True:

        pergunta = input("\nPergunta: ")

        if pergunta.lower() in ["sair", "exit", "quit"]:
            break

        resposta = agente.invoke({"input": pergunta})

        print("\nResposta:")
        print(resposta["output"])
