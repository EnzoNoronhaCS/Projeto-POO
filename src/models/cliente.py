class Cliente:
    def __init__(self, nome, documento, email="", telefone=""):
        self.set_nome(nome)
        self.set_documento(documento)
        self.set_email(email)
        self.set_telefone(telefone)

    def set_nome(self, nome):
        if nome and len(str(nome).strip()) >= 3:
            self.__nome = str(nome).strip()
        else:
            raise ValueError("Nome deve ter pelo menos 3 caracteres")

    def get_nome(self):
        return self.__nome

    def set_documento(self, documento):
        apenas_numeros = "".join(c for c in str(documento) if c.isdigit())
        if len(apenas_numeros) in (11, 14):
            self.__documento = apenas_numeros
        else:
            raise ValueError("Documento deve ser um CPF (11 dígitos) ou CNPJ (14 dígitos)")

    def get_documento(self):
        return self.__documento

    def set_email(self, email):
        email = str(email).strip()
        if email == "" or ("@" in email and "." in email.split("@")[-1]):
            self.__email = email
        else:
            raise ValueError("E-mail inválido")

    def get_email(self):
        return self.__email

    def set_telefone(self, telefone):
        apenas_numeros = "".join(c for c in str(telefone) if c.isdigit())
        if apenas_numeros == "" or len(apenas_numeros) in (10, 11):
            self.__telefone = apenas_numeros
        else:
            raise ValueError("Telefone deve ter 10 ou 11 dígitos")

    def get_telefone(self):
        return self.__telefone

    def eh_pessoa_juridica(self):
        return len(self.__documento) == 14

    def documento_formatado(self):
        d = self.__documento
        if self.eh_pessoa_juridica():
            return f"{d[:2]}.{d[2:5]}.{d[5:8]}/{d[8:12]}-{d[12:]}"
        return f"{d[:3]}.{d[3:6]}.{d[6:9]}-{d[9:]}"

    def telefone_formatado(self):
        t = self.__telefone
        if t == "":
            return "não informado"
        if len(t) == 11:
            return f"({t[:2]}) {t[2:7]}-{t[7:]}"
        return f"({t[:2]}) {t[2:6]}-{t[6:]}"

    def __eq__(self, outro):
        if not isinstance(outro, Cliente):
            return False
        return self.__documento == outro.get_documento()

    def __hash__(self):
        return hash(self.__documento)

    def __str__(self):
        tipo = "PJ" if self.eh_pessoa_juridica() else "PF"
        return f"{self.__nome} ({tipo} - {self.documento_formatado()})"

    def __repr__(self):
        return self.__str__()    