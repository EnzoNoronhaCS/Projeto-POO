from models.contrato import Contrato


class ContratoMensal(Contrato):
    INDICE_PADRAO = 0.05

    def calcular_reajuste(self, referencia=None):
        ciclos = self.ciclos_de_reajuste(referencia)
        return self.get_valor_base() * self.get_indice_reajuste() * ciclos

    def valor_atual(self, referencia=None):
        return self.get_valor_base() + self.calcular_reajuste(referencia)

    def valor_total_do_periodo(self, referencia=None):
        return self.valor_atual(referencia) * self.duracao_em_meses()

    def tipo(self):
        return "Contrato mensal"

    def __str__(self):
        return f"{super().__str__()} | parcela atual R$ {self.valor_atual():.2f}"

    def valor_mensal_equivalente(self, referencia=None):
        return self.valor_atual(referencia)