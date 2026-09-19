# Gerenciador de Contratos

Projeto Computacional 1 — Programação Orientada a Objetos
Prof. Wesin Alves — UniCEUB
Análise e Desenvolvimento de Sistemas

## Descrição

O Gerenciador de Contratos é uma aplicação em Python, executada em linha de
comando, para o cadastro e acompanhamento de contratos de prestação de serviço.

O sistema registra clientes (pessoa física ou jurídica), vincula contratos a
esses clientes, calcula reajustes conforme o tipo de contrato, identifica quais
estão próximos do vencimento e gera alertas classificados por urgência. Também
emite um relatório consolidado com o total de contratos por situação, o
faturamento mensal previsto e as pendências que exigem ação.

## Justificativa

A escolha do tema partiu da convivência com ambientes administrativos que
lidam com contratos no dia a dia. Por já ter familiaridade com esse tipo de
rotina, optei por desenvolver algo próximo do que conheço na prática, o que
permitiu concentrar o esforço na modelagem orientada a objetos em vez de na
compreensão do problema.

O controle de contratos em pequenas e médias organizações costuma ser feito em
planilhas ou anotações avulsas, método que apresenta três falhas recorrentes:
não há validação dos dados inseridos, o vencimento só é percebido quando já
ocorreu, e o cálculo de reajuste é refeito manualmente a cada consulta. A perda
de um prazo de renovação tem custo direto, seja pela interrupção do serviço,
seja pela renovação em condições piores.

O domínio também se mostrou adequado ao paradigma orientado a objetos:
contratos compartilham atributos e comportamentos comuns, mas divergem na forma
de calcular reajuste, o que torna a herança e o polimorfismo soluções naturais
e não artificiais.

## Funcionalidades

- Cadastro de clientes com validação de CPF e CNPJ
- Cadastro de contratos mensais e anuais vinculados a um cliente
- Cálculo automático de reajuste conforme o tipo de contrato
- Consulta detalhada de um contrato específico
- Busca de contratos por nome ou documento do cliente
- Listagem de contratos por situação (ativo, vencido, não iniciado)
- Listagem de contratos próximos do vencimento, com prazo configurável
- Geração de alertas classificados por urgência e ordenados por gravidade
- Renovação de contrato com extensão da data de término
- Remoção de contratos
- Relatório consolidado com faturamento mensal previsto e pendências
- Carga de dados de exemplo para demonstração

## Temas abordados

**Classes e objetos**

O sistema é composto por seis classes. Cada arquivo do diretório `models`
contém uma única classe, e o diretório `services` concentra a classe
responsável pela coordenação do conjunto.

**Encapsulamento**

Todos os atributos são privados, declarados com duplo underscore, e o acesso
externo ocorre exclusivamente por métodos `get` e `set`. Os setters validam o
dado antes de atribuí-lo e levantam `ValueError` quando o valor é inválido,
impedindo que um objeto exista em estado inconsistente. O método
`listar_todos()` devolve uma cópia da lista interna, evitando que código
externo altere a coleção do gerenciador.

**Herança**

A classe `Contrato` concentra os atributos e comportamentos comuns: número,
cliente, valor base, período de vigência e índice de reajuste. As classes
`ContratoMensal` e `ContratoAnual` herdam essa estrutura e chamam o construtor
da superclasse por meio de `super().__init__()`, reaproveitando integralmente
a validação já implementada.

**Polimorfismo**

Os métodos `calcular_reajuste()`, `valor_atual()`, `valor_mensal_equivalente()`
e `tipo()` são sobrescritos nas subclasses. O contrato mensal aplica juros
simples; o anual aplica juros compostos e admite desconto por pagamento
antecipado. O método `faturamento_mensal_previsto()` do gerenciador percorre
uma lista que mistura os dois tipos e invoca o mesmo método em todos os
objetos, sem verificar a classe de cada um — cada instância responde conforme
sua própria implementação.

**Abstração**

A classe `Contrato` não é instanciável na prática: seus métodos de cálculo
levantam `NotImplementedError`, e o gerenciador recusa objetos dessa classe
base. Ela define o contrato de comportamento que as subclasses concretas devem
cumprir.

**Sobrecarga de operadores e métodos especiais**

As classes implementam `__str__` e `__repr__` para representação textual,
`__eq__` e `__hash__` para comparação por identidade de negócio (documento do
cliente, número do contrato) e `__lt__` na classe `Alerta`, que permite ordenar
alertas por gravidade com a função nativa `sorted()`. A classe
`GerenciadorContratos` implementa `__len__`, `__iter__` e `__contains__`,
comportando-se como uma coleção nativa do Python.

**Tratamento de exceções**

As validações levantam exceções nas classes de modelo, e o tratamento é
centralizado no laço principal de `main.py`. Dessa forma, erros de entrada
resultam em mensagens legíveis ao usuário, sem interromper a execução do
programa.

## Tecnologias

- Python 3
- Git e GitHub para versionamento
- Visual Studio Code como ambiente de desenvolvimento
- Interface em linha de comando

## Bibliotecas

O projeto utiliza apenas módulos da biblioteca padrão do Python, sem
dependências externas:

- `datetime` — manipulação de datas, cálculo de prazos e vigência
- `sys` e `pathlib` — resolução do caminho de importação dos módulos

A ausência de bibliotecas externas foi uma decisão de projeto: o sistema é
executável em qualquer instalação padrão do Python 3, sem etapa de instalação
de dependências.

## Estrutura do projeto

src/
main.py interface de linha de comando
models/
cliente.py dados e validação do cliente
contrato.py classe base dos contratos
contrato_mensal.py contrato com reajuste simples
contrato_anual.py contrato com reajuste composto
alerta.py classificação de urgência
services/
gerenciador.py coordenação, consultas e relatório
docs/
relatorio.md
diagrama-classes.png


## Distribuição das tarefas

Projeto desenvolvido individualmente. Todas as etapas — levantamento do
problema, modelagem das classes, implementação, testes e documentação — foram
executadas pelo autor.

## Como executar

Na raiz do projeto:

python3 src/main.py


A opção 10 do menu carrega oito contratos de exemplo, cobrindo todas as
situações possíveis do sistema: contratos vencidos, próximos do vencimento,
ainda não iniciados e em vigência normal.

## Autor

Enzo Noronha — UniCEUB, Análise e Desenvolvimento de Sistemas
