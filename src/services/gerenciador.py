from datetime import date

from models.contrato import Contrato
from models.alerta import Alerta


class GerenciadorContratos:
    def __init__(self, contratos=None):
        self.__contratos = []
        if contratos is not None:
            for contrato in contratos:
                self.adicionar(contrato)

    def adicionar(self, contrato):
        if not isinstance(contrato, Contrato):
            raise ValueError("Só é possível adicionar objetos Contrato")
        if type(contrato) is Contrato:
            raise ValueError("Use uma subclasse concreta (ContratoMensal ou ContratoAnual)")
        if self.buscar_por_numero(contrato.get_numero()) is not None:
            raise ValueError(f"Já existe um contrato com o número {contrato.get_numero()}")
        self.__contratos.append(contrato)
        return contrato

    def remover(self, numero):
        contrato = self.buscar_por_numero(numero)
        if contrato is None:
            raise ValueError(f"Contrato {numero} não encontrado")
        self.__contratos.remove(contrato)
        return contrato

    def buscar_por_numero(self, numero):
        alvo = str(numero).strip()
        if alvo == "":
            return None
        for contrato in self.__contratos:
            if contrato.get_numero() == alvo:
                return contrato
        return None

    def buscar_por_cliente(self, termo):
        termo = str(termo).strip().lower()
        if termo == "":
            return []
        encontrados = []
        for contrato in self.__contratos:
            cliente = contrato.get_cliente()
            if termo in cliente.get_nome().lower() or termo in cliente.get_documento():
                encontrados.append(contrato)
        return encontrados

    def listar_todos(self):
        return list(self.__contratos)

    def listar_ativos(self, referencia=None):
        return [c for c in self.__contratos if c.status(referencia) == "ativo"]

    def listar_vencidos(self, referencia=None):
        return [c for c in self.__contratos if c.status(referencia) == "vencido"]

    def listar_vencendo(self, dias=45, referencia=None):
        encontrados = []
        for contrato in self.__contratos:
            if contrato.status(referencia) != "ativo":
                continue
            if contrato.dias_para_vencer(referencia) <= dias:
                encontrados.append(contrato)
        return sorted(encontrados, key=lambda c: c.dias_para_vencer(referencia))

    def gerar_alertas(self, referencia=None):
        return sorted(Alerta(c, referencia) for c in self.__contratos)

    def alertas_que_exigem_acao(self, referencia=None):
        return [a for a in self.gerar_alertas(referencia) if a.exige_acao()]

    def faturamento_mensal_previsto(self, referencia=None):
        total = 0.0
        for contrato in self.listar_ativos(referencia):
            total += contrato.valor_mensal_equivalente(referencia)
        return total

    def total_por_tipo(self):
        resumo = {}
        for contrato in self.__contratos:
            chave = contrato.tipo()
            resumo[chave] = resumo.get(chave, 0) + 1
        return resumo

    def cliente_com_mais_contratos(self):
        if not self.__contratos:
            return None
        contagem = {}
        for contrato in self.__contratos:
            cliente = contrato.get_cliente()
            contagem[cliente] = contagem.get(cliente, 0) + 1
        return max(contagem.items(), key=lambda item: item[1])

    def relatorio(self, referencia=None):
        if referencia is None:
            referencia = date.today()

        linha = "  " + "─" * 48
        partes = ["", f"  Relatório de contratos — {referencia.strftime('%d/%m/%Y')}", linha]

        if not self.__contratos:
            partes.append("  Nenhum contrato cadastrado.")
            return "\n".join(partes)

        partes.append(f"  Total de contratos   {len(self.__contratos)}")
        partes.append(f"  Ativos               {len(self.listar_ativos(referencia))}")
        partes.append(f"  Vencidos             {len(self.listar_vencidos(referencia))}")

        for tipo, quantidade in self.total_por_tipo().items():
            partes.append(f"  {tipo:<20} {quantidade}")

        partes.append("")
        partes.append(f"  Faturamento mensal previsto   R$ {self.faturamento_mensal_previsto(referencia):.2f}")

        destaque = self.cliente_com_mais_contratos()
        if destaque is not None:
            partes.append(f"  Cliente com mais contratos    {destaque[0].get_nome()} ({destaque[1]})")

        pendentes = self.alertas_que_exigem_acao(referencia)
        partes.append("")
        partes.append(f"  Pendências ({len(pendentes)})")
        for alerta in pendentes:
            partes.append(f"    {alerta}")

        return "\n".join(partes)

    def __len__(self):
        return len(self.__contratos)

    def __iter__(self):
        return iter(self.__contratos)

    def __contains__(self, item):
        if isinstance(item, Contrato):
            return item in self.__contratos
        return self.buscar_por_numero(item) is not None

    def __str__(self):
        return f"GerenciadorContratos com {len(self.__contratos)} contrato(s)"