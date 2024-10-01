from flask import Flask, render_template, request, redirect  # Importa o Flask e outras funções necessárias

app = Flask(__name__)  # Inicializa a aplicação Flask

# Rota para a página inicial
@app.route("/")
def index():
    return render_template("index.html")  # Renderiza o template HTML da página inicial

def status(imc):
    if imc < 18.5:
        return 'Abaixo do peso'
    elif 18.5 <= imc < 24.9:
        return 'Peso Normal'
    elif 25 <= imc < 29.9:
        return 'Acima do Peso'
    else:
        return 'Obeso'

# Rota para validar e salvar os dados no arquivo
@app.route("/validar_imc", methods=['POST'])
def validar_imc():
    nome_da_pessoa = request.form["nome_da_pessoa"]  # Obtém o nome da pessoa do formulário
    peso = float(request.form["peso"])  # Obtém o peso do formulário
    altura = float(request.form["altura"])  # Obtém a altura do formulário

    # Calcula o IMC
    imc = peso / (altura ** 2)

    # Caminho para o arquivo de texto onde os dados serão salvos
    caminho_arquivo = 'models/notas.txt'
    with open(caminho_arquivo, 'a') as arquivo:  # Abre o arquivo no modo de adição
        arquivo.write(f"{nome_da_pessoa};{peso};{altura};{imc:.2f}; {status(imc)}\n")  # Escreve os dados no arquivo

    return redirect("/")  # Redireciona de volta para a página inicial

# Rota para consultar os IMCs
@app.route("/consultar_imc")
def consultar_imc():
    imc = []  # Lista para armazenar os dados das pessoas
    caminho_arquivo = 'models/notas.txt'  # Define o caminho do arquivo de dados
    
    # Abre o arquivo para leitura
    with open(caminho_arquivo, 'r') as arquivo:
        for linha in arquivo:  # Itera sobre cada linha do arquivo
            item = linha.strip().split(';')  # Separa os dados da linha por ponto e vírgula
            
            # Verifica se a linha tem o número correto de elementos
            if len(item) < 5:
                continue  # Ignora linhas com dados insuficientes
            
            # Adiciona os dados à lista de IMC
            imc.append({
                'nome': item[0],  # Nome da pessoa
                'peso': item[1],  # Peso
                'altura': item[2],  # Altura
                'imc': item[3], # IMC calculado
                'status': item[4]  # Status
            })

    
    return render_template("consultar_imc.html", imc=imc)  # Renderiza o template de consulta com os dados

# Inicia a aplicação Flask
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=80, debug=True)  # Executa o servidor na porta 80, modo debug ativado
