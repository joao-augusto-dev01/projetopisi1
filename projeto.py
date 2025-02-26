import os
import re
from pydantic import BaseModel, HttpUrl, ValidationError
from urllib.parse import urlparse

class URLModel(BaseModel):
    url: HttpUrl

dados_usuarios = {}

url_historico = []
numero_telefone_historico = []

urls = {
    "ecommerce": {
        "https://www.mercadolivre.com.br",
        "https://www.amazon.com.br",
        "https://www.americanas.com.br",
        "https://www.magazineluiza.com.br",
        "https://www.casasbahia.com.br",
        "https://shopee.com.br"
    },
    "bancos": {
        "https://www.caixa.gov.br",
        "https://www.santander.com.br",
        "https://www.bb.com.br",
        "https://nubank.com.br"
    },
    "operadoras": {
        "https://www.oi.com.br/",
        "https://www.claro.com.br/",
        "https://www.tim.com.br"
        "https://vivo.com.br"
    },
    "jogos": {
        "https://store.steampowered.com",
        "https://store.epicgames.com",
        "https://www.nintendo.com",
        "https://www.crunchyroll.com",
        "https://www.ea.com"
    },
    "governo": {
        "https://www.gov.br",
        "https://www.detran.pe.gov.br",
        "https://servicos.compesa.com.br",
        "https://www.neoenergia.com",
        "https://www.ufrpe.br",
        "https://www.ufpe.br"
    }
}

def limpar_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def validar_email():
    while True:
        email = input("Digite seu email: (Ex: usuario@gmail.com) ").strip().lower()
        erros = []
        if "@" not in email:
            erros.append("faltando '@'")
        if not re.search(r"\.(com|org|br)$", email):
            erros.append("faltando ou domínio inválido (.com, .org, .br)")
        if not re.search(r"@(gmail|hotmail|outlook)\.com", email):
            erros.append("provedor de domínio inválido (gmail, hotmail, outlook)")
        
        if not erros:
            return email
        print(f"Email inválido: {', '.join(erros)}")

def validar_senha():
    while True:
        senha = input("Digite sua senha (Ex: Senha123): ").strip()
        erros = []
        if len(senha) < 8:
            erros.append("precisa ter pelo menos 8 caracteres")
        if not re.search(r"[A-Z]", senha):
            erros.append("precisa conter pelo menos uma letra maiúscula")
        if not re.search(r"[0-9]", senha):
            erros.append("precisa conter pelo menos um número")
        
        if erros:
            print(f"Senha inválida: {', '.join(erros)}")
            continue
        confirmar_senha = input("Confirme sua senha: ").strip()
        if confirmar_senha == senha:
            return senha
        else:
            print("As senhas não coincidem.")

dominios_permitidos = {}

def atualizar_dominios_permitidos():
    global dominios_permitidos
    dominios_permitidos.clear()
    for categoria, lista_urls in urls.items():
        for url in lista_urls:
            parsed_url = urlparse(url)
            netloc_parts = parsed_url.netloc.split(".")
            if netloc_parts[-1] == "br":
                dominio_base = ".".join(netloc_parts[-2:])
            else:
                dominio_base = ".".join(netloc_parts[-2:])
            dominios_permitidos[dominio_base] = categoria
    
    dominios_permitidos["mercadolivre.com.br"] = "e-commerce"

atualizar_dominios_permitidos()

def validar_url():
    while True:
        url = input("Digite uma URL: ("https://www.mercadolivre.com.br").strip().lower()
        try:
            # Validar a URL usando Pydantic
            url_validada = URLModel(url=url)
            url_str = str(url_validada.url).rstrip("/")
            
            # Cortar a URL na primeira barra
            url_cortada = url_str.split('/')[0] + '//' + url_str.split('/')[2]
            
            # Verificar se a URL cortada está no dicionário de URLs válidas
            encontrada = False
            for categoria, lista_urls in urls.items():
                if url_cortada in lista_urls:
                    print(f"✅ URL válida e segura: {url_cortada} (Tipo: {categoria})")
                    url_historico.append(url_cortada)
                    encontrada = True
                    break
            
            if not encontrada:
                print(f"❌ URL inválida: Não está na lista segura.")
            
            return url_cortada
        
        except ValidationError as e:
            print(f"❌ URL inválida: {e.errors()[0]['msg']}")
        print("Tente novamente.")

def validar_telefone():
    while True:
        telefone = input("Digite um número de telefone (Ex: (DDD) 9 1234-5678 ou similar): ").strip()
        telefone_limpo = re.sub(r"\D", "", telefone)
        if len(telefone_limpo) > 15:
            print("Número inválido. Deve conter no máximo 15 dígitos.")
            continue
        spam_palavras = [("0303", "canal de vendas"), ("0555", "possível spam")]
        for prefixo, descricao in spam_palavras:
            if telefone_limpo.startswith(prefixo):
                print(f"Número marcado como {descricao}.")
                numero_telefone_historico.append(telefone)
                return
        ddds = {
            "AC": ["68"], "AL": ["82"], "AM": ["92", "97"], "AP": ["96"],
            "BA": ["71", "73", "74", "75", "77"], "CE": ["85", "88"], "DF": ["61"],
            "ES": ["27", "28"], "GO": ["62", "64"], "MA": ["98", "99"], "MG": ["31", "32", "33", "34", "35", "37", "38"],
            "MS": ["67"], "MT": ["65", "66"], "PA": ["91", "93", "94"], "PB": ["83"],
            "PE": ["81", "87"], "PI": ["86", "89"], "PR": ["41", "42", "43", "44", "45", "46"],
            "RJ": ["21", "22", "24"], "RN": ["84"], "RO": ["69"], "RR": ["95"],
            "RS": ["51", "53", "54", "55"], "SC": ["47", "48", "49"], "SE": ["79"],
            "SP": ["11", "12", "13", "14", "15", "16", "17", "18", "19"], "TO": ["63"]
        }
        
        ddd = telefone_limpo[4:6] if telefone_limpo.startswith("9090") else telefone_limpo[:2]
        estado_encontrado = None
        for estado, lista_ddds in ddds.items():
            if ddd in lista_ddds:
                estado_encontrado = estado
                break
        if telefone_limpo.startswith("9090"):
            if estado_encontrado:
                print(f"Número a cobrar do DDD {ddd}, localizado em {estado_encontrado}.")
                numero_telefone_historico.append(telefone)
                return
            print("Número a cobrar, mas DDD inválido.")
            return
        elif estado_encontrado:
            print(f"Número pertence a {estado_encontrado}.")
            numero_telefone_historico.append(telefone)
            return
        print("Formato de número inválido.")

def adicionar_url():
    while True:
        url = input("Digite a URL que deseja adicionar: ").strip().lower()
        
        if re.search(r"\d", url):
            print("❌ URLs não podem conter números. Tente novamente.")
            continue
        
        if " " in url:
            print("❌ URLs não podem conter espaços em branco. Tente novamente.")
            continue
        
        parsed_url = urlparse(url)
        if not parsed_url.scheme:
            url = "https://" + url
            parsed_url = urlparse(url)
        
        url_cortada = f"{parsed_url.scheme}://{parsed_url.netloc}"
        
        with open("urls.txt", "r") as arquivo:
            urls_existentes = arquivo.readlines()
            if url_cortada + "\n" in urls_existentes:
                print("❌ Esta URL já foi adicionada anteriormente.")
                continue
        
        with open("urls.txt", "a") as arquivo:
            arquivo.write(url_cortada + "\n")
        print(f"✅ URL '{url_cortada}' adicionada com sucesso no arquivo 'urls.txt'.")
        break

def adicionar_telefone():
    while True:
        telefone = input("Digite o número de telefone que deseja adicionar: ").strip()
        
        if re.search(r"[a-zA-Z]", telefone):
            print("❌ Números de telefone não podem conter letras. Tente novamente.")
            continue
        
        if " " in telefone:
            print("❌ Números de telefone não podem conter espaços em branco. Tente novamente.")
            continue
        
        if not re.match(r"^[0-9\-()]+$", telefone):
            print("❌ Números de telefone só podem conter números, hífen (-) e parênteses (). Tente novamente.")
            continue
        
        with open("numeros.txt", "r") as arquivo:
            numeros_existentes = arquivo.readlines()
            if telefone + "\n" in numeros_existentes:
                print("❌ Este número de telefone já foi adicionado anteriormente.")
                continue
        
        with open("numeros.txt", "a") as arquivo:
            arquivo.write(telefone + "\n")
        print(f"✅ Número de telefone '{telefone}' adicionado com sucesso no arquivo 'numeros.txt'.")
        break

def excluir_url():
    url = input("Digite a URL que deseja excluir: ").strip().lower()
    with open("urls.txt", "r") as arquivo:
        linhas = arquivo.readlines()
    with open("urls.txt", "w") as arquivo:
        for linha in linhas:
            if linha.strip() != url:
                arquivo.write(linha)
    print(f"URL '{url}' excluída com sucesso do arquivo 'urls.txt'.")

def excluir_telefone():
    telefone = input("Digite o número de telefone que deseja excluir: ").strip()
    with open("numeros.txt", "r") as arquivo:
        linhas = arquivo.readlines()
    with open("numeros.txt", "w") as arquivo:
        for linha in linhas:
            if linha.strip() != telefone:
                arquivo.write(linha)
    print(f"Número de telefone '{telefone}' excluído com sucesso do arquivo 'numeros.txt'.")

def excluir_historico_urls():
    global url_historico
    if not url_historico:
        print("Nenhuma URL no histórico para excluir.")
    else:
        url_historico.clear()
        print("Histórico de URLs excluído com sucesso.")
    input("Pressione Enter para continuar...")

def excluir_historico_telefones():
    global numero_telefone_historico
    if not numero_telefone_historico:
        print("Nenhum número de telefone no histórico para excluir.")
    else:
        numero_telefone_historico.clear()
        print("Histórico de números de telefone excluído com sucesso.")
    input("Pressione Enter para continuar...")

def menu_principal():
    while True:
        limpar_terminal()
        print("\n---Menu Principal---")
        print("[1] ---Cadastrar Email e Senha---")
        print("[2] ---Mostrar Cadastro---")
        print("[3] ---Atualizar Cadastro---")
        print("[4] ---Excluir Cadastro---")
        print("[5] ---Validar Url---")
        print("[6] ---Validar Número de Telefone---")
        print("[7] ---Gerenciar Números de Telefone e Urls---")
        print("[8] ---Visualizar Histórico---")
        escolha = input("Escolha uma opção: ").strip()
        
        if escolha == "1":
            limpar_terminal()
            email = validar_email()
            senha = validar_senha()
            dados_usuarios[email] = senha
            print("Cadastro realizado com sucesso.")
            input("Pressione Enter para continuar...")
        elif escolha == "5":
            limpar_terminal()
            validar_url()
            input("Pressione Enter para continuar...")
        elif escolha == "6":
            limpar_terminal()
            validar_telefone()
            input("Pressione Enter para continuar...")
        elif escolha == "2":
            limpar_terminal()
            if not dados_usuarios:
                print("Não há nenhum registro ainda.")
            else:
                for email, senha in dados_usuarios.items():
                    print(f"Email: {email}, Senha: {'*' * len(senha)}")
                    mostrar = input("Deseja ver a senha cadastrada? (s/n): ").strip().lower()
                    if mostrar == "s":
                        print(f"Senha cadastrada: {senha}")
                        input("Pressione Enter para continuar...")
        elif escolha == "3":
            limpar_terminal()
            dados_usuarios.clear()
            print("Cadastro excluído. Vamos criar um novo cadastro.")
            email = validar_email()
            senha = validar_senha()
            dados_usuarios[email] = senha
            print("Cadastro atualizado com sucesso.")
            input("Pressione Enter para continuar...")
        elif escolha == "4":
            limpar_terminal()
            dados_usuarios.clear()
            print("Todos os cadastros foram excluídos.")
            input("Pressione Enter para continuar...")
        elif escolha == "7":
            while True:
                limpar_terminal()
                print("\nGerenciar URLs e Números de Telefone:")
                print("[1] ---Adicionar URL---")
                print("[2] ---Adicionar Número de Telefone---")
                print("[3] ---Excluir URL---")
                print("[4] ---Excluir Número de Telefone---")
                print("[5] ---Voltar ao Menu Principal---")
                opcao = input("Escolha uma opção: ").strip()
                if opcao == "1":
                    adicionar_url()
                    input("Pressione Enter para continuar...")
                elif opcao == "2":
                    adicionar_telefone()
                    input("Pressione Enter para continuar...")
                elif opcao == "3":
                    excluir_url()
                    input("Pressione Enter para continuar...")
                elif opcao == "4":
                    excluir_telefone()
                    input("Pressione Enter para continuar...")
                elif opcao == "5":
                    break
                else:
                    print("Opção inválida. Tente novamente.")
        elif escolha == "8":
            while True:
                limpar_terminal()
                print("\n---Visualizar Histórico---")
                print("[1] ---Visualizar Histórico de URLs---")
                print("[2] ---Visualizar Histórico de Números de Telefone---")
                print("[3] ---Excluir Histórico de URLs---")
                print("[4] ---Excluir Histórico de Números de Telefone---")
                print("[5] ---Voltar ao Menu Principal---")
                opcao = input("Escolha uma opção: ").strip()
                if opcao == "1":
                    limpar_terminal()
                    if not url_historico:
                        print("Nenhuma URL foi validada ainda.")
                    else:
                        print("Histórico de URLs:")
                        for url in url_historico:
                            print(f"- {url}")
                    input("Pressione Enter para continuar...")
                elif opcao == "2":
                    limpar_terminal()
                    if not numero_telefone_historico:
                        print("Nenhum número de telefone foi validado ainda.")
                    else:
                        print("Histórico de Números de Telefone:")
                        for telefone in numero_telefone_historico:
                            print(f"- {telefone}")
                    input("Pressione Enter para continuar...")
                elif opcao == "3":
                    excluir_historico_urls()
                elif opcao == "4":
                    excluir_historico_telefones()
                elif opcao == "5":
                    break
                else:
                    print("Opção inválida. Tente novamente.")
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu_principal()
