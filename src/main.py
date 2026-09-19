import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from models.cliente import Cliente
from models.contrato_mensal import ContratoMensal
from models.contrato_anual import ContratoAnual
from services.gerenciador import GerenciadorContratos


gerenciador = GerenciadorContratos()
clientes = []
exemplos_carregados = False

LARGURA = 52


def titulo(texto):
    print()
    print(f"  {texto}")
    print(f"  {'─' * (LARGURA - 4)}")


def buscar_cliente(documento):
    apenas_numeros = "".join(c for c in str(documento) if c.isdigit())
    for cliente in clientes:
        if cliente.get_documento() == apenas_numeros:
            return cliente
    return None


def cadastrar_contrato():
    titulo("Novo contrato")

    numero = input("  Número do contrato: ")
    if gerenciador.buscar_por_numero(numero) is not None:
        print(f"  O contrato {numero.strip()} já existe.")
        return

    documento = input("  CPF ou CNPJ do cliente: ")
    cliente = buscar_cliente(documento)
    cliente_novo = cliente is None

    if cliente_novo:
        nome = input("  Nome: ")
        email = input("  E-mail (Enter para pular): ")
        telefone = input("  Telefone (Enter para pular): ")
        cliente = Cliente(nome, documento, email, telefone)
    else:
        print(f"  Cliente encontrado: {cliente.get_nome()}")

    print("  Tipo: [1] mensal  [2] anual")
    tipo = input("  Escolha: ").strip()

    valor = input("  Valor base: ").replace(",", ".")
    data_inicio = input("  Início (dd/mm/aaaa): ")
    data_fim = input("  Fim (dd/mm/aaaa): ")

    indice = input("  Índice de reajuste (Enter para o padrão): ").replace(",", ".")
    indice = float(indice) if indice.strip() != "" else None

    if tipo == "2":
        antecipado = input("  Pagamento antecipado? (s/n): ").strip().lower() == "s"
        contrato = ContratoAnual(numero, cliente, valor, data_inicio, data_fim, indice, antecipado)
    else:
        contrato = ContratoMensal(numero, cliente, valor, data_inicio, data_fim, indice)

    gerenciador.adicionar(contrato)

    if cliente_novo:
        clientes.append(cliente)

    print(f"\n  Cadastrado: {contrato}")


def listar_contratos():
    if len(gerenciador) == 0:
        print("\n  Nenhum contrato cadastrado.")
        return

    titulo(f"{len(gerenciador)} contrato(s)")
    for contrato in gerenciador:
        print(f"  {contrato}")
        print(f"        {contrato.status()}, {contrato.dias_para_vencer()} dia(s)")


def detalhar_contrato():
    numero = input("  Número do contrato: ")
    contrato = gerenciador.buscar_por_numero(numero)
    if contrato is None:
        print("  Contrato não encontrado.")
        return

    cliente = contrato.get_cliente()

    titulo(f"Contrato {contrato.get_numero()}")
    print(f"  Tipo               {contrato.tipo()}")
    print(f"  Cliente            {cliente}")
    print(f"  Contato            {cliente.telefone_formatado()}")
    print(f"  E-mail             {cliente.get_email() or 'não informado'}")
    print()
    print(f"  Vigência           {contrato.get_data_inicio().strftime('%d/%m/%Y')} a {contrato.get_data_fim().strftime('%d/%m/%Y')}")
    print(f"  Duração            {contrato.duracao_em_meses()} meses")
    print(f"  Situação           {contrato.status()}")
    print(f"  Dias para vencer   {contrato.dias_para_vencer()}")
    print()
    print(f"  Valor base         R$ {contrato.get_valor_base():.2f}")
    print(f"  Reajuste           R$ {contrato.calcular_reajuste():.2f}")
    print(f"  Valor atual        R$ {contrato.valor_atual():.2f}")
    print(f"  Equiv. mensal      R$ {contrato.valor_mensal_equivalente():.2f}")


def buscar_por_cliente():
    termo = input("  Nome ou documento: ")
    encontrados = gerenciador.buscar_por_cliente(termo)
    if not encontrados:
        print("  Nenhum contrato encontrado.")
        return

    titulo(f"{len(encontrados)} resultado(s)")
    for contrato in encontrados:
        print(f"  {contrato}")


def listar_vencendo():
    entrada = input("  Vencendo em quantos dias? (Enter para 45): ").strip()
    dias = int(entrada) if entrada != "" else 45

    encontrados = gerenciador.listar_vencendo(dias)
    if not encontrados:
        print(f"  Nenhum contrato vence nos próximos {dias} dias.")
        return

    titulo(f"Vencendo em até {dias} dias")
    for contrato in encontrados:
        print(f"  {contrato.dias_para_vencer():>4} dia(s)   {contrato}")


def ver_alertas():
    alertas = gerenciador.gerar_alertas()
    if not alertas:
        print("\n  Nenhum contrato cadastrado.")
        return

    titulo(f"{len(alertas)} alerta(s)")
    for alerta in alertas:
        print(f"  {alerta}")


def renovar_contrato():
    numero = input("  Número do contrato: ")
    contrato = gerenciador.buscar_por_numero(numero)
    if contrato is None:
        print("  Contrato não encontrado.")
        return

    print(f"  Vencimento atual: {contrato.get_data_fim().strftime('%d/%m/%Y')}")
    nova_data = input("  Nova data de fim (dd/mm/aaaa): ")
    contrato.renovar(nova_data)
    print(f"\n  Renovado: {contrato}")


def remover_contrato():
    numero = input("  Número do contrato: ")
    removido = gerenciador.remover(numero)
    print(f"\n  Removido: {removido}")


def carregar_exemplos():
    global exemplos_carregados

    if exemplos_carregados:
        print("\n  Os dados de exemplo já foram carregados.")
        return

    hoje = date.today()

    escola = Cliente("Castelinho da Crianca LTDA", "12345678000190", "contato@castelinho.com", "6133334444")
    joao = Cliente("Joao da Silva", "12345678901", "joao@email.com", "61999998888")
    mercado = Cliente("Mercado Central ME", "98765432000110", "financeiro@central.com", "61988887777")
    ana = Cliente("Ana Beatriz Moreira", "32165498702", "ana.moreira@email.com", "61977776666")
    aurora = Cliente("Transportes Aurora LTDA", "45678912000133", "contratos@aurora.com", "6132225555")
    clinica = Cliente("Clinica Vida Plena ME", "78945612000144", "adm@vidaplena.com", "61966665555")

    clientes.extend([escola, joao, mercado, ana, aurora, clinica])

    novos = [
        ContratoMensal("001", escola, 3500.00, hoje - timedelta(days=400), hoje + timedelta(days=10)),
        ContratoMensal("002", joao, 890.50, hoje - timedelta(days=60), hoje + timedelta(days=300)),
        ContratoAnual("003", mercado, 24000.00, hoje - timedelta(days=800), hoje + timedelta(days=30), None, True),
        ContratoAnual("004", escola, 15000.00, hoje - timedelta(days=500), hoje - timedelta(days=20)),
        ContratoMensal("005", ana, 1200.00, hoje - timedelta(days=200), hoje + timedelta(days=5)),
        ContratoAnual("006", aurora, 48000.00, hoje - timedelta(days=1100), hoje + timedelta(days=40)),
        ContratoMensal("007", clinica, 2750.00, hoje + timedelta(days=15), hoje + timedelta(days=560)),
        ContratoMensal("008", mercado, 640.00, hoje - timedelta(days=450), hoje - timedelta(days=90)),
    ]

    for contrato in novos:
        gerenciador.adicionar(contrato)

    exemplos_carregados = True
    print(f"\n  {len(novos)} contratos e {len(clientes)} clientes carregados.")


def menu():
    print()
    print(f"  Gerenciador de contratos{'':>8}{len(gerenciador)} cadastrado(s)")
    print(f"  {'─' * (LARGURA - 4)}")
    print("   1   Cadastrar contrato")
    print("   2   Listar contratos")
    print("   3   Detalhar contrato")
    print("   4   Buscar por cliente")
    print("   5   Contratos vencendo")
    print("   6   Ver alertas")
    print("   7   Relatório")
    print("   8   Renovar contrato")
    print("   9   Remover contrato")
    print("  10   Carregar dados de exemplo")
    print("   0   Sair")
    print()
    return input("  opção: ").strip()


def main():
    acoes = {
        "1": cadastrar_contrato,
        "2": listar_contratos,
        "3": detalhar_contrato,
        "4": buscar_por_cliente,
        "5": listar_vencendo,
        "6": ver_alertas,
        "7": lambda: print(gerenciador.relatorio()),
        "8": renovar_contrato,
        "9": remover_contrato,
        "10": carregar_exemplos,
    }

    while True:
        opcao = menu()

        if opcao == "0":
            print("  Encerrando.\n")
            break

        acao = acoes.get(opcao)
        if acao is None:
            print("  Opção inválida.")
            continue

        try:
            acao()
        except ValueError as erro:
            print(f"  Erro: {erro}")
        except Exception as erro:
            print(f"  Erro inesperado: {erro}")


if __name__ == "__main__":
    main()