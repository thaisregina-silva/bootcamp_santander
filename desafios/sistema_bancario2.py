"""
Sistema Bancário Simples

Funcionalidades:
- Depósito, saque, extrato e consulta de saldo
- Cadastro de usuários com CPF único
- Criação de contas associadas aos usuários
- Menu interativo com entrada de dados via input

Regras de negócio:
- Um usuário pode ter múltiplas contas
- Limite de 3 saques/dia de até R$ 500,00 cada
- Cada conta está vinculada a um único CPF
- Sistema permanece em execução até usuário optar por sair
"""

def menu():
    menu = """\n
    **** MENU ****

    Digite a opção desejada:
    
    [d] Depositar
    [s] Sacar
    [c] Consultar Saldo
    [e] Extrato
    [n] Nova Conta
    [l] Listar Contas
    [u] Novo Usuário
    [q] Sair

    -> """
    return input(menu)

def consultar_saldo(saldo):
    print(f"Seu saldo é R${saldo:.2f}")

def depositar(saldo, valor, extrato, /):
    if valor < 0:
        print("Não foi possível realizar a operação. Valor inválido")
    else:    
        saldo += valor
        extrato += f"Depósito: {valor:.2f}\n"
        print(f"Depósito de {valor:.2f} realizado com sucesso. Seu saldo atual é de R$ {saldo:.2f}")
    
    return saldo, extrato   

def sacar(*, saldo, valor, extrato, limite_valorsaque, n_saque, limite_nsaque):
    excedeu_saldo = valor > saldo
    excedeu_n_saque = n_saque >= limite_nsaque
    excedeu_valor_saque = valor > limite_valorsaque
    if excedeu_saldo:
        print(f"Não foi possível realizar a operação. Seu saldo é de R$ {saldo:.2f}")
    elif excedeu_n_saque:
        print(f"Operação falhou. Você atingiu o número máximo diário de {limite_nsaque} saques.")
    elif excedeu_valor_saque:
        print(f"Operação falhou. O valor ultrapassa o limite de R$ {limite_valorsaque:.2f}")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R${valor:.2f}\n"
        print(f"Saque de R${valor:.2f} realizado com sucesso.")
        n_saque += 1

    return saldo, extrato, n_saque
    
def exibir_extrato(saldo, /, *, extrato):
    print("\n---------- EXTRATO ----------")
    print("Não foram realizadas movimentações" if not extrato else extrato)
    print(f"Saldo: R$ {saldo:.2f}") 
    print("---------------------------")
    
def criar_usuario(usuarios):
    cpf = input("Digite seu CPF (apenas números): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("Já existe um usuário cadastrado com esse CPF!")
        return
    
    nome = input("Digite seu nome completo: ")
    data_nascimento = input("Informe sua data de nascimento (dd-mm-aaa): ")
    endereco = input("Informe seu endereço (logradouro, nº - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print("Usuário cadastrado com sucesso!")

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("Conta criada com sucesso!")
        return({"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario})
    print("\nUsuário não encontrado, fluxo de criação de conta encerrado.")

def listar_contas(contas):
    for conta in contas:
        linha = f"""
            Ag: {conta['agencia']}
            C/C: {conta['numero_conta']}
            Titular: {conta['usuario']['nome']}
         """
        print(linha)

def main():
    saldo = 0
    limite_valorsaque = 500
    extrato = ""
    n_saque = 0
    LIMITE_NSAQUE = 3
    AGENCIA = "0001"
    usuarios = []
    contas = []
    numero_conta = 0

    while True:

        opcao = menu()

        if opcao == "d":
            valor = float(input("Qual valor deseja depositar?\n"))
            saldo, extrato = depositar(saldo, valor, extrato)
            
        elif opcao == "s":
            valor = float(input("Informe o valor do saque:\n"))

            saldo, extrato, n_saque = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite_valorsaque=limite_valorsaque,
                n_saque=n_saque,
                limite_nsaque=LIMITE_NSAQUE,
            )

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)   

        elif opcao == "q":
            break

        elif opcao == "c":
            consultar_saldo(saldo)

        elif opcao == "u":
            criar_usuario(usuarios)

        elif opcao == "n":
            conta = criar_conta(AGENCIA, numero_conta, usuarios)  

            if conta:
                contas.append(conta)
                numero_conta +=1  

        elif opcao == "l":
            listar_contas(contas)

        else:
            print("Operação inválida, digite a operação desejada.")    


if __name__ == "__main__":
    main()