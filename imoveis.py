"""Classes que representam os imóveis da R.M Imóveis e suas regras de preço."""
from abc import ABC, abstractmethod


class Imovel(ABC):
    """Classe base (abstrata): define o que TODO imóvel precisa saber fazer.

    Cada tipo de imóvel (subclasse) implementa suas próprias regras de
    adicionais, mas o cálculo do aluguel mensal é o mesmo para todos.
    """

    TIPO = ""
    ALUGUEL_BASE = 0.0

    def __init__(self, quartos=1, vagas=0):
        self.quartos = quartos
        self.vagas = vagas

    # --- regras específicas: cada subclasse decide ---
    @abstractmethod
    def adicional_quartos(self):
        """Valor extra mensal por quantidade de quartos."""

    @abstractmethod
    def valor_garagem(self):
        """Valor mensal das vagas de garagem/estacionamento."""

    # --- regras comuns: reaproveitadas por todos ---
    def aluguel_antes_desconto(self):
        return self.ALUGUEL_BASE + self.adicional_quartos() + self.valor_garagem()

    def desconto(self, possui_criancas=True):
        """Por padrão não há desconto; Apartamento sobrescreve este método."""
        return 0.0

    def aluguel_mensal(self, possui_criancas=True):
        return round(self.aluguel_antes_desconto() - self.desconto(possui_criancas), 2)

    def itens_detalhados(self, possui_criancas=True):
        """Lista (descrição, valor) para o resumo do orçamento."""
        itens = [(f"Aluguel-base ({self.TIPO})", self.ALUGUEL_BASE)]
        if self.adicional_quartos():
            itens.append((f"Adicional de {self.quartos} quartos", self.adicional_quartos()))
        if self.valor_garagem():
            itens.append((self.descricao_garagem(), self.valor_garagem()))
        if self.desconto(possui_criancas):
            itens.append(("Desconto de 5% (sem crianças)", -self.desconto(possui_criancas)))
        return itens

    def descricao_garagem(self):
        return f"Garagem ({self.vagas} vaga(s))"


class Apartamento(Imovel):
    TIPO = "Apartamento"
    ALUGUEL_BASE = 700.00
    ADICIONAL_2_QUARTOS = 200.00
    VAGA_GARAGEM = 300.00
    DESCONTO_SEM_CRIANCAS = 0.05

    def adicional_quartos(self):
        return self.ADICIONAL_2_QUARTOS if self.quartos == 2 else 0.0

    def valor_garagem(self):
        return self.VAGA_GARAGEM if self.vagas >= 1 else 0.0

    def desconto(self, possui_criancas=True):
        # 5% sobre o aluguel já com os adicionais aplicados
        if not possui_criancas:
            return round(self.aluguel_antes_desconto() * self.DESCONTO_SEM_CRIANCAS, 2)
        return 0.0


class Casa(Imovel):
    TIPO = "Casa"
    ALUGUEL_BASE = 900.00
    ADICIONAL_2_QUARTOS = 250.00
    VAGA_GARAGEM = 300.00

    def adicional_quartos(self):
        return self.ADICIONAL_2_QUARTOS if self.quartos == 2 else 0.0

    def valor_garagem(self):
        return self.VAGA_GARAGEM if self.vagas >= 1 else 0.0


class Estudio(Imovel):
    TIPO = "Estúdio"
    ALUGUEL_BASE = 1200.00
    PACOTE_INICIAL_VAGAS = 2
    VALOR_PACOTE = 250.00
    VAGA_ADICIONAL = 60.00

    def __init__(self, vagas=0):
        super().__init__(quartos=1, vagas=vagas)  # estúdio não tem opção de quartos

    def adicional_quartos(self):
        return 0.0

    def valor_garagem(self):
        if self.vagas <= 0:
            return 0.0
        extras = max(0, self.vagas - self.PACOTE_INICIAL_VAGAS)
        return self.VALOR_PACOTE + extras * self.VAGA_ADICIONAL

    def descricao_garagem(self):
        return f"Estacionamento ({self.vagas} vagas)"
