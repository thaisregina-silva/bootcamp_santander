'''
Projeto de um sistema bancário simples onde o usuário pode escolher opções apresentadas no menu (depositar, sacar, obter extrato ou sair).
A operação extrato apresenta o histórico completo de saques e depósitos realizados.
A operação de saque tem limite diário (3) com valor máximo de R$ 500,00 cada.
O sistema faz verificação de saldo e limite de saques antes de realizar as operações e apresenta uma mensagem ao usuário caso resulte em falha.
Além disso, o sistema roda em um loop infinito criado com 'while True' para que as movimentações (depósito, saque e extrato) ocorram até que o usuário decida encerrar.
'''

menu = '''
***Escolha uma opção***

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

'''

saldo = 0
limite_valorsaque = 500
extrato = ""
numero_saque = 0
LIMITE_NSAQUE = 3

while True:

    opcao = input(menu)

    if opcao == "d":
        valor_deposito = float(input("Qual valor deseja depositar?\n"))
        if valor_deposito < 0:
            print("Não foi possível realizar a operação. Valor informado é inválido.")
        else:
            saldo = saldo + valor_deposito
            print(f"Depósito de R${valor_deposito:.2f} realizado com sucesso.\n")
            print(f"Seu saldo atual é R$ {saldo}.")
            extrato += f"Depósito: R$ {valor_deposito:.2f}\n"
           
    elif opcao == "s":
        
        excedeu_saque = numero_saque >= LIMITE_NSAQUE
        if excedeu_saque:
            print("Operação falhou! Número máximo de saques excedido.")
        else:
                    
            valor_saque = float(input("Informe o valor do saque:\n"))

            excedeu_saldo = valor_saque > saldo

            excedeu_limite = valor_saque > limite_valorsaque


            if excedeu_saldo:
                print("Operação falhou! Você não tem saldo suficiente.")

            elif excedeu_limite:
                print("Operação falhou! O valor do saque excede o limite.")

    
            elif valor_saque > 0:
                saldo -= valor_saque
                extrato += f"Saque: R$ {valor_saque:.2f}\n"
                print(f"Saque de R$ {valor_saque:.2f} realizado com sucesso!")
                numero_saque += 1

            else:
                print("Operação falhou! Valor informado é inválido.")    

    elif opcao == "e":
        print("\n---------- EXTRATO ----------")
        if not extrato:
            print("Não foram realizadas movimentações.")
        else:
            print(extrato)
        print(f"Saldo: R$ {saldo:.2f}") 
        print("---------------------------")       

    elif opcao == "q":
        break

    else:
       print("Operação inválida, digite a operação desejada.")          

