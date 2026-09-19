from models.contrato import Contrato


class ContratoAnual(Contrato):
    INDICE_PADRAO = 0.08
    DESCONTO_ANTECIPACAO = 0.10

    def __init__(self, numero, cliente, valor_base, data_inicio, data_fim, indice_reajuste=None, pagamento_antecipado=False):
        super().__init__(numero, cliente, valor_base, data_inicio, data_fim, indice_reajuste)
        self.set_pagamento_antecipado(pagamento_antecipado)

    def set_pagamento_antecipado(self, antecipado):
        self.__pagamento_antecipado = bool(antecipado)

    def get_pagamento_antecipado(self):
        return self.__pagamento_antecipado

    def calcular_reajuste(self, referencia=None):
        ciclos = self.ciclos_de_reajuste(referencia)
        base = self.get_valor_base()
        return base * ((1 + self.get_indice_reajuste()) ** ciclos - 1)

    def valor_atual(self, referencia=None):
        valor = self.get_valor_base() + self.calcular_reajuste(referencia)
        if self.__pagamento_antecipado:
            valor = valor * (1 - self.DESCONTO_ANTECIPACAO)
        return valor

    def valor_total_do_periodo(self, referencia=None):
        anos = self.duracao_em_meses() / 12
        return self.valor_atual(referencia) * anos

    def tipo(self):
        return "Contrato anual"

    def __str__(self):
        marcador = " | à vista" if self.__pagamento_antecipado else ""
        return f"{super().__str__()} | anuidade atual R$ {self.valor_atual():.2f}{marcador}"

    def valor_mensal_equivalente(self, referencia=None):
        return self.valor_atual(referencia) / 12