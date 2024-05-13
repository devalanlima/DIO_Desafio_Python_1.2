menu = """
[u] Novo Usuário
[c] Nova Conta
[l] Listar Usuários
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

numero_contas = 0

def validar_cpf(lista, cpf):
  for usuario in lista:
    if usuario['cpf'] == cpf:
      return True
  return False

def criar_usuario(cpf, usuarios):
  if validar_cpf(usuarios, cpf):
    print(f"\nUsuário {cpf} já está cadastrado")
  else:
    nome= input('Nome do usuário: ')
    data_de_nascimento = input('Data de nascimento no formato dd/mm/yyyy: ')
    endereco = input("Endereço no formato: 'logradouro | Nº | bairro | cidade / sigla estado': ")
    novo_usuario = {
      'nome': nome,
      'data_de_nascimento': data_de_nascimento,
      'cpf': cpf,
      'endereço': endereco,
    }
    usuarios.append(novo_usuario)
    print("\nUsuário cadastrado com sucesso")

def criar_conta(cpf, usuarios, agencia, contas):
  if validar_cpf(usuarios, cpf):  
    global numero_contas

    numero_contas += 1
    conta = {
      'num_conta': f'{agencia}-{numero_contas}', 
      'cpf': cpf,
    }
    contas.append(conta)
    for usuario in usuarios:
      if usuario['cpf'] == cpf:
        usuario["conta"] = conta
    print(f"\nConta de número {conta['num_conta']} criada com sucesso")
  else:
    print(f"\nUsuário de CPF '{cpf}' ainda não foi cadastrado, faça o cadastro e depois crie uma conta.")

def saque(*, valor, saldo, numero_saques, extrato, limite, LIMITE_SAQUES ):

  excedeu_saldo = valor > saldo

  excedeu_limite = valor > limite

  excedeu_saques = numero_saques >= LIMITE_SAQUES

  if excedeu_saldo:
    print("\nOperação falhou! Você não tem saldo suficiente.")

  elif excedeu_limite:
    print("\nOperação falhou! O valor do saque excede o limite.")

  elif excedeu_saques:
    print("\nOperação falhou! Número máximo de saques excedido.")

  elif valor > 0:
    saldo -= valor
    extrato += f"Saque: R$ {valor:.2f}\n"
    numero_saques += 1
    print(f"\nSaque no valor de R${valor:.2f} realizado com sucesso, seu novo saldo é de R${saldo:.2f}")
    return saldo, extrato, numero_saques
  else:
    print("\nOperação falhou! O valor informado é inválido.")

def deposito(valor, saldo, extrato, /):
  if valor > 0:
    saldo += valor
    extrato += f"Depósito: R$ {valor:.2f}\n"
    print(f"\nDepósito de R${valor:.2f} efetuado com sucesso, seu novo saldo é de R${saldo:.2f}")
    return saldo, extrato
  else:
    print("\nOperação falhou! O valor informado é inválido.")

def print_extrato(saldo, /, *, extrato):
  print("\n================ EXTRATO ================")
  print("Não foram realizadas movimentações." if not extrato else extrato)
  print(f"\nSaldo: R$ {saldo:.2f}")
  print("==========================================")

def main():
  saldo = 0
  limite = 500
  extrato = ""
  numero_saques = 0
  LIMITE_SAQUES = 3
  agencia = '0001'
  usuarios = []
  contas = []

  while True:
    opcao = input(menu)
    
    if opcao == "d":
      valor = float(input("\nInforme o valor do depósito: "))
      depositar = deposito(valor, saldo, extrato)
      if depositar:
        saldo, extrato = depositar

    elif opcao == "s":
      valor = float(input("\nInforme o valor do saque: "))
      sacar = saque(valor=valor, saldo=saldo, numero_saques=numero_saques, extrato=extrato, limite=limite, LIMITE_SAQUES=LIMITE_SAQUES)

      if sacar:
        saldo, extrato, numero_saques = sacar

    elif opcao == "e":
      print_extrato(saldo, extrato=extrato)

    elif opcao == "u":
      cpf = input("\nCPF do usuário, apenas números: ")
      criar_usuario(cpf, usuarios)

    elif opcao == "c":
      cpf = input("\nCPF do usuário, apenas números: ")
      criar_conta(cpf, usuarios, agencia, contas)

    elif opcao == "l":
      if len(usuarios) > 0:
        for usuario in usuarios:
          if 'conta' in usuario:
            print(f"\n{usuario['nome']} - CPF: {usuario['cpf']} - Conta: {usuario['conta']['num_conta']}")
          else:
            print(f"\n{usuario['nome']} - CPF: {usuario['cpf']}")
      else:
        print("\nNão existem usuários cadastrados até o momento")

    elif opcao == "q":
      break

    else:
      print("\nOperação inválida, por favor selecione novamente a operação desejada.")

main()
