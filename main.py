from openai import OpenAI
from dotenv import load_dotenv
import os
import tiktoken

load_dotenv()
cliente = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
is_conected = (os.system('nc -z 8.8.8.8 53') == 0)

def matematica(problema, problemas_valido, modelo):
    if modelo == "gpt-3.5-turbo":
        token = 1024
    elif modelo == "gpt-3.5-turbo-0125":
        token = 4096
    prompt_system = f"""
    Você é um resolvedor de problemas de matematica
    você deve resolver todo o problema especificado pelo usuário
    Você deve responder apenas a resposta e, só explicar a resposta se o usuário perguntar
    #problemas validos:
    {problemas_valido}

    #formato de saída:
    exemplo 1
    entrada: Resolva essa equação: 1x² - 3x + 2 = 0
    saida: x1 = 2, x2 = 1
    
    exemplo 2
    entrada: Resolva essa equação e explique o resultado: 2x + 5 = 11 
    saída: x=3 pois 2.3 + 5 = 11

    """
    lista_mensagens = [
    {
        "role": "system",
        "content": prompt_system
    },
    {
        "role": "user",
        "content": problema
    }
    ]

    resposta = cliente.chat.completions.create(
        messages=lista_mensagens,
        model=modelo,
        temperature=0.5,
        max_tokens=token

    )
    return resposta.choices[0].message.content


def ler_problemas_validos():
    try:
        arquivo = open("mathsolver/problemas.txt", "r", encoding="utf-8")
        leitura = arquivo.read()
        arquivo.close()
        return leitura
    except IOError as f:
        print(f"Não foi possível abrir o arquivo: {f}")

def definir_modelo(token):
    codificador =  tiktoken.encoding_for_model("gpt-3.5-turbo")
    lista_tokens = codificador.encode(token)
    num_tokens = len(lista_tokens)
    print(f"Números de tokens utilizados: {num_tokens}")
    if num_tokens <= 4096:
        return "gpt-3.5-turbo"
    elif num_tokens > 4096 and num_tokens <= 16385:
        return "gpt-3.5-turbo-0125"

    
def chat(conec):
    if conec == True:
        problemas_validos = ler_problemas_validos()
        print("Escreva 'exit' para sair ou 'help' para ajuda")
        print("A IA pode cometer erros.")
        while True:
            problem = input("Transcreva o seu problema, se quiser explicação, peça explicação: ")
            modelo = definir_modelo(problem)
            print(f"modelo usado: {modelo}")
            if problem == "" or problem == "exit":
                print("Saindo do programa")
                break
            elif problem == "help":
                print(f'{problemas_validos} exit para sair')
            else:
               resposta = matematica(problem, problemas_validos, modelo)
               print(resposta)
               
    else:
        print("Não foi possível estabelecer uma conexão com a internet")

chat(is_conected)
