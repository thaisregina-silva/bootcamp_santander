'''
Desafio: sistema bancário simples
Apenas um usuário;
Deve permitir depositar valores positivos na conta;
Operação Extrato deve mostrar o histórico de saques e depósitos realizados;
Operação saque deve ter limites: 3 saques diários de até R$ 500,00 cada;
Sempre que o saldo for insuficiente ou opção inválida, apresentar mensagem.
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

