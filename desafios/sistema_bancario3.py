"""
Sistema Bancário Simples

Funcionalidades:
- Depósito, saque, histórico e consulta de saldo
- Cadastro de usuários com CPF único
- Criação de contas associadas aos usuários

Regras de negócio:
- Um usuário pode ter múltiplas contas
- Limite de 3 saques/dia de até R$ 500,00 cada
- Cada conta está vinculada a um único CPF
"""

from abc import ABC, abstractmethod
from datetime import datetime   

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = [] # um cliente pode ter várias contas

    def adicionar_conta(self, conta):
        self.contas.append(conta)

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta) 

class PessoaFisica(Cliente):
   
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf    

class Conta:
    def __init__(self, numero, cliente):
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._saldo = 0
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, numero, cliente):
        return cls(numero, cliente)

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def saldo(self):
        return self._saldo

    @property
    def historico(self):
        return self._historico
        
    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo
        if excedeu_saldo:
            print("Saldo insuficiente.")
        elif valor > 0:
            self._saldo -= valor
            print(f"Saque de {valor:.2f} realizado com sucesso.")
            return True
        else:
            print("Operação falhou! Valor inválido.")
        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print(f"Depósito de {valor:.2f} realizado com sucesso.")
        else:
            print("Operação falhou! Valor inválido.")
            return False
        return True

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite_valor_saque=500, limite_saque=3):
        super().__init__(numero, cliente)
        self.limite_valor_saque = limite_valor_saque
        self.limite_saque = limite_saque

    @classmethod
    def nova_conta(cls, numero, cliente):
        return cls(numero, cliente)

    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == "Saque"])
        excedeu_limite = valor > self.limite_valor_saque
        execedeu_saques = numero_saques >= self.limite_saque

        if excedeu_limite:
            print("Limite de saque excedido.")
        elif execedeu_saques:
            print("Limite de saques excedido.")
        else:
            return super().sacar(valor)
        return False

    def __str__(self):
        return f"""
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """
    
class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
        })

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

# criar um cliente
Cliente1 = PessoaFisica("Thaís", "27-02-1990", "123.456.789-00", "Rua Manoel Salgado, 381 - São Paulo/SP")

# criar uma conta para o cliente1
Conta1 = ContaCorrente.nova_conta("0001-123456", Cliente1)

# adicionar conta1 ao cliente1
Cliente1.adicionar_conta(Conta1)

# depositar valor
deposito = Deposito(1000)
Cliente1.realizar_transacao(Conta1, deposito)

saque = Saque(200)
Cliente1.realizar_transacao(Conta1, saque)

print(f"Saldo atual: R$ {Conta1.saldo:.2f}")

for transacao in Conta1.historico.transacoes:
    print(f"{transacao['tipo']}: R$ {transacao['valor']:.2f}")
