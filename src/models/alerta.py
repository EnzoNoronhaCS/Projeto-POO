from datetime import date

from models.contrato import Contrato


class Alerta:
    NIVEIS = {
        "informativo": 0,
        "atencao": 1,
        "urgente": 2,
        "vencido": 3,
    }

    LIMITE_URGENTE = 15
    LIMITE_ATENCAO = 45

    def __init__(self, contrato, referencia=None):
        self.set_contrato(contrato)
        self.__referencia = referencia if referencia is not None else date.today()
        self.__nivel = self.__definir_nivel()
        self.__mensagem = self.gerar_mensagem()

    def set_contrato(self, contrato):
        if not isinstance(contrato, Contrato):
            raise ValueError("Alerta precisa de um objeto Contrato válido")
        self.__contrato = contrato

    def get_contrato(self):
        return self.__contrato

    def get_nivel(self):
        return self.__nivel

    def get_mensagem(self):
        return self.__mensagem

    def get_referencia(self):
        return self.__referencia

    def __definir_nivel(self):
        status = self.__contrato.status(self.__referencia)
        if status == "vencido":
            return "vencido"
        if status == "nao iniciado":
            return "informativo"
        dias = self.__contrato.dias_para_vencer(self.__referencia)
        if dias <= self.LIMITE_URGENTE:
            return "urgente"
        if dias <= self.LIMITE_ATENCAO:
            return "atencao"
        return "informativo"

    def gerar_mensagem(self):
        numero = self.__contrato.get_numero()
        nome = self.__contrato.get_cliente().get_nome()
        dias = self.__contrato.dias_para_vencer(self.__referencia)

        if self.__nivel == "vencido":
            return f"Contrato {numero} ({nome}) venceu há {abs(dias)} dia(s)."
        if self.__nivel == "urgente":
            return f"Contrato {numero} ({nome}) vence em {dias} dia(s). Renovação urgente."
        if self.__nivel == "atencao":
            return f"Contrato {numero} ({nome}) vence em {dias} dia(s). Iniciar tratativas."
        return f"Contrato {numero} ({nome}) sem pendências. Vence em {dias} dia(s)."

    def exige_acao(self):
        return self.NIVEIS[self.__nivel] >= self.NIVEIS["atencao"]

    def prioridade(self):
        return self.NIVEIS[self.__nivel]

    def __lt__(self, outro):
        if not isinstance(outro, Alerta):
            return NotImplemented
        if self.prioridade() != outro.prioridade():
            return self.prioridade() > outro.prioridade()
        return self.__contrato.dias_para_vencer(self.__referencia) < outro.get_contrato().dias_para_vencer(outro.get_referencia())

    def __eq__(self, outro):
        if not isinstance(outro, Alerta):
            return False
        return self.__contrato == outro.get_contrato() and self.__nivel == outro.get_nivel()

    def __hash__(self):
        return hash((self.__contrato.get_numero(), self.__nivel))

    def __str__(self):
        return f"[{self.__nivel.upper()}] {self.__mensagem}"

    def __repr__(self):
        return self.__str__()    

    def atualizar(self, referencia=None):
        if referencia is not None:
            self.__referencia = referencia
        self.__nivel = self.__definir_nivel()
        self.__mensagem = self.gerar_mensagem()    