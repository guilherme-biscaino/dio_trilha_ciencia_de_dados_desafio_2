LIMITE_SAQUES = 3
contas = {}
usuarios = {"teste": {"nome": "admin", "nascimento": "00000000", "endereco": "teste", "senha": "admin"}}
agencia = "001"
contas_no_banco = 1
menu_option = str
current_user = str


def menu():
    menu = """
    ***Menu***
        [d] Depositar
        [s] Sacar
        [e] Extrato
        [q] Sair
        [n] Criar nova conta
        [l] Listar suas contas
    ********
    """
    return input(menu)


def init_menu():
    log_menu = """
                Bem vindo ao NewBanking
                selecione a opção (1) caso queira fazer login na sua conta.
                selecione a opção (2) caso deseje criar uma nova conta.
    """
    return input(log_menu)


def login(usuarios):
    print(usuarios)

    try:
        attemp_user = input('digite seu cpf: \n')
        temp_dict = usuarios.__getitem__(attemp_user)
        if (temp_dict.__getitem__("senha") == input("digite a senha: \n")):
            return attemp_user
        else:
            print("usuario ou senha incorretos")
            login(usuarios)
    except KeyError:
        print("Usuário não existe")
        login(usuarios)


def deposito(contas, current_user):
    print("""A opção escolhida foi: Depósito""")
    conta_deposito = input("digite o numero da conta que deseja fazer o deposito: \n")

    valor_deposito = float(input(f"""Digite o valor que deseja depositar: \n"""))

    try:
        if valor_deposito > 0:
            contas[f"{conta_deposito}"][
                "extrato"] += f"""**Fora feito o deposito no valor de: R$ {valor_deposito:.2f}** \n"""
            contas[f"{conta_deposito}"]["saldo"] += valor_deposito
            print("Deposito feito com sucesso!")
            return contas
        else:
            print("""O valor do deposito não pode ser negativo!\n""")
    except ValueError:
        print("""O valor inserido não é um número compatível.""")

    return contas


def saque(contas):
    print("""A opção escolhida foi: Saque""")
    conta_saque = input("digite o numero da conta que deseja efetuar o saque: \n")
    valor_saque = float(
        input(f"""Saldo atual: R${contas[f"{conta_saque}"]["saldo"]:.2f} \nDigite o valor que deseja sacar:\n"""))

    try:
        if LIMITE_SAQUES <= contas[f"{conta_saque}"]["numero_de_saques"]:
            print("""Você já atingiu o limite de saques diários""")

        elif valor_saque > contas[f"{conta_saque}"]["limite"]:
            print("O valor de saque não pode ser maior que o limite de saque!")

        elif valor_saque > contas[f"{conta_saque}"]["saldo"]:
            print("O valor a ser sacado não pode ser maior que o saldo da conta.")

        else:
            contas[f"{conta_saque}"]["extrato"] += f"""**Fora feito um saque no valor de: {valor_saque:.2f}** \n"""
            contas[f"{conta_saque}"]["saldo"] -= valor_saque
            contas[f"{conta_saque}"]["numero_de_saques"] += 1
            print(
                f"""Quantidades de saques disponiveis: {LIMITE_SAQUES - contas[f"{conta_saque}"]["numero_de_saques"]}""")

    except ValueError:
        print("O valor inserido não é um número compatível.")
    return contas


def Extrato(contas):
    conta_extrato = input("digite o numero da conta que deseja obter extrato: \n")
    print("""A opção escolhida foi: Extrato""")
    contas[f"{conta_extrato}"][
        "extrato"] += f"""***extrato gerado, saldo em conta durante o extrato: R$ {contas[f"{conta_extrato}"]["saldo"]:.2f} \n"""
    print(contas[f"{conta_extrato}"]["extrato"])

    return contas


def criar_usuario(usuarios):
    nome = input("digite seu nome: \n")
    cpf = input("digite seu cpf: \n")
    endereco = input("digite seu endereço: \n")
    nascimento = input("data de nascimento: \n")
    senha = input("digite uma senha: \n")
    if (cpf not in usuarios):
        usuarios.update({f"{cpf}": {"nome": nome, "nascimento": nascimento, "endereco": endereco, "senha": senha}})
        print("sua conta foi criada com sucesso!")
        return usuarios, cpf
    else:
        print("já existe uma conta com seu cpf \n tente fazer login com seu cpf!")
        init_menu()
        return usuarios, cpf


def criar_conta(current_user, contas, agencia, contas_no_banco, usuarios):
    if (current_user in contas):
        contas = {f"{contas_no_banco}": {"titular": f"{current_user}", "nome": usuarios[f"{current_user}"]["nome"],
                                         "numero_da_conta": contas_no_banco, "agencia": agencia, "saldo": 0.0,
                                         "limite": 500, "extrato": f"""""", "numero_de_saques": 0}}
    else:
        contas.update({f"{contas_no_banco}": {"titular": f"{current_user}", "nome": usuarios[f"{current_user}"]["nome"],
                                              "numero_da_conta": contas_no_banco, "agencia": agencia, "saldo": 0.0,
                                              "limite": 500, "extrato": f"""""", "numero_de_saques": 0}})

    contas_no_banco += 1
    print("conta criada com sucesso!")
    return contas, contas_no_banco


def get_current_user_in_contas(current_user, contas):
    for i in enumerate(contas):
        account_check = []
        account_check.append(contas[i[1]]["titular"] == current_user)
        return account_check


def listar_contas_do_usuario(contas, current_user):
    print("suas contas: ")
    for i in enumerate(contas):
        if (contas[i[1]]["titular"] == current_user):
            print(f"numero da conta: {contas[i[1]]['numero_da_conta']}, nome do titular: {contas[i[1]]['nome']}, agencia da conta: {contas[i[1]]['agencia']}, saldo: {contas[i[1]]['saldo']}")

def sair(current_user):
    print("Obrigado por usar nosso sistema!")
    current_user = 0
    return current_user

def routine(usuarios, contas, current_user, contas_no_banco):
    while True:
        if (get_current_user_in_contas(current_user, contas) == None or get_current_user_in_contas(current_user,contas) == False):
            print("Notamos que você ainda não tem uma conta em nosso banco, então criaremos uma para você")
            contas, contas_no_banco = criar_conta(current_user, contas, agencia, contas_no_banco, usuarios)

        opcao = menu()

        if opcao == "d":
            contas = deposito(contas, current_user)


        elif opcao == "s":
            contas = saque(contas)


        elif opcao == "e":
            contas = Extrato(contas)


        elif opcao == "q":
            current_user = sair(current_user)
            return usuarios, contas, current_user, contas_no_banco

        elif opcao == "n":
            contas, contas_no_banco = criar_conta(current_user, contas, agencia, contas_no_banco, usuarios)

        elif opcao == "l":
            listar_contas_do_usuario(contas, current_user)

        else:
            print("A opção escolhida não é compatível, por favor selecione uma opção disponivel no menu.")

def init(usuarios, contas, current_user, contas_no_banco):
    init_option = init_menu()

    if (init_option == "1" and current_user != "0"):
        current_user = login(usuarios)
        print(contas)
        usuarios, contas, current_user, contas_no_banco = routine(usuarios, contas, current_user,contas_no_banco)


    elif (init_option == "2"):
        usuarios, current_user = criar_usuario(usuarios)
        current_user = login(usuarios)
        usuarios, contas, current_user, contas_no_banco = routine(usuarios, contas, current_user,contas_no_banco)

    elif (init_option == "10"):
        print("delisgando sistema")
        return usuarios, contas, current_user, contas_no_banco

    elif (init_option == "12"):
        for i in enumerate(contas):
            print(f"numero da conta: {contas[i[1]]['numero_da_conta']}, nome do titular: {contas[i[1]]['nome']}, agencia da conta: {contas[i[1]]['agencia']}, saldo: {contas[i[1]]['saldo']}")
            init(usuarios, contas, current_user, contas_no_banco)

    else:
        print("desculpe, a opção que escolheu não é valida")
    init(usuarios, contas, current_user, contas_no_banco)

init(usuarios, contas, current_user, contas_no_banco)
print("registros do sistema: ")
print("contas criadas: ")
print(contas)
print("usuarios criados: ")
print(usuarios)
input()



