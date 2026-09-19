from datetime import date, datetime

from models.cliente import Cliente


class Contrato:
    INDICE_PADRAO = 0.0

    def __init__(self, numero, cliente, valor_base, data_inicio, data_fim, indice_reajuste=None):
        self.set_numero(numero)
        self.set_cliente(cliente)
        self.set_valor_base(valor_base)
        self.set_periodo(data_inicio, data_fim)
        self.set_indice_reajuste(indice_reajuste)

    def _converter_data(self, valor):
        if isinstance(valor, date):
            return valor
        try:
            return datetime.strptime(str(valor), "%d/%m/%Y").date()
        except ValueError:
            raise ValueError(f"Data inválida: '{valor}'. Use o formato dd/mm/aaaa")

    def set_numero(self, numero):
        if str(numero).strip() == "":
            raise ValueError("Número do contrato não pode ser vazio")
        self.__numero = str(numero).strip()

    def get_numero(self):
        return self.__numero

    def set_cliente(self, cliente):
        if not isinstance(cliente, Cliente):
            raise ValueError("Contrato precisa de um objeto Cliente válido")
        self.__cliente = cliente

    def get_cliente(self):
        return self.__cliente

    def set_valor_base(self, valor_base):
        try:
            valor = float(valor_base)
        except (TypeError, ValueError):
            raise ValueError("Valor do contrato deve ser numérico")
        if valor <= 0:
            raise ValueError("Valor do contrato deve ser maior que zero")
        self.__valor_base = valor

    def set_indice_reajuste(self, indice):
        if indice is None:
            indice = self.INDICE_PADRAO
        try:
            valor = float(indice)
        except (TypeError, ValueError):
            raise ValueError("Índice de reajuste deve ser numérico")
        if valor < 0 or valor > 1:
            raise ValueError("Índice de reajuste deve estar entre 0 e 1")
        self.__indice_reajuste = valor

    def get_indice_reajuste(self):
        return self.__indice_reajuste

    def ciclos_de_reajuste(self, referencia=None):
        return self.meses_decorridos(referencia) // 12        

    def get_valor_base(self):
        return self.__valor_base

    def set_periodo(self, data_inicio, data_fim):
        inicio = self._converter_data(data_inicio)
        fim = self._converter_data(data_fim)
        if fim <= inicio:
            raise ValueError("Data de fim deve ser posterior à data de início")
        self.__data_inicio = inicio
        self.__data_fim = fim

    def get_data_inicio(self):
        return self.__data_inicio

    def get_data_fim(self):
        return self.__data_fim

    def dias_para_vencer(self, referencia=None):
        if referencia is None:
            referencia = date.today()
        return (self.__data_fim - referencia).days

    def esta_vencido(self, referencia=None):
        return self.dias_para_vencer(referencia) < 0

    def esta_ativo(self, referencia=None):
        if referencia is None:
            referencia = date.today()
        return self.__data_inicio <= referencia <= self.__data_fim

    def status(self, referencia=None):
        if referencia is None:
            referencia = date.today()
        if referencia < self.__data_inicio:
            return "nao iniciado"
        if referencia > self.__data_fim:
            return "vencido"
        return "ativo"

    def duracao_em_meses(self):
        anos = self.__data_fim.year - self.__data_inicio.year
        meses = self.__data_fim.month - self.__data_inicio.month
        total = anos * 12 + meses
        if self.__data_fim.day < self.__data_inicio.day:
            total -= 1
        return max(total, 0)

    def meses_decorridos(self, referencia=None):
        if referencia is None:
            referencia = date.today()
        if referencia > self.__data_fim:
            referencia = self.__data_fim
        if referencia < self.__data_inicio:
            return 0
        anos = referencia.year - self.__data_inicio.year
        meses = referencia.month - self.__data_inicio.month
        total = anos * 12 + meses
        if referencia.day < self.__data_inicio.day:
            total -= 1
        return max(total, 0)    

    def renovar(self, nova_data_fim):
        nova = self._converter_data(nova_data_fim)
        if nova <= self.__data_fim:
            raise ValueError("A renovação deve estender o contrato")
        self.__data_fim = nova

    def tipo(self):
        return "Contrato"

    def calcular_reajuste(self):
        raise NotImplementedError("Use ContratoMensal ou ContratoAnual")

    def valor_atual(self):
        raise NotImplementedError("Use ContratoMensal ou ContratoAnual")

    def valor_mensal_equivalente(self, referencia=None):
        raise NotImplementedError("Use ContratoMensal ou ContratoAnual")    

    def __eq__(self, outro):
        if not isinstance(outro, Contrato):
            return False
        return self.__numero == outro.get_numero()

    def __hash__(self):
        return hash(self.__numero)

    def __str__(self):
        inicio = self.__data_inicio.strftime("%d/%m/%Y")
        fim = self.__data_fim.strftime("%d/%m/%Y")
        return f"[{self.__numero}] {self.tipo()} | {self.__cliente.get_nome()} | {inicio} a {fim} | R$ {self.__valor_base:.2f}"

    def __repr__(self):
        return self.__str__()    