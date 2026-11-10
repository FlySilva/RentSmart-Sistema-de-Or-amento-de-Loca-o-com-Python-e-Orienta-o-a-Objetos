"""Orçamento de locação: junta imóvel + taxa contratual e gera a projeção em CSV."""
import csv


class Orcamento:
    TAXA_CONTRATUAL = 2000.00
    MAX_PARCELAS = 5
    MESES_PROJECAO = 12

    def __init__(self, imovel, parcelas_taxa, possui_criancas=True):
        if not 1 <= parcelas_taxa <= self.MAX_PARCELAS:
            raise ValueError(f"A taxa pode ser paga em 1 a {self.MAX_PARCELAS} parcelas.")
        self.imovel = imovel
        self.parcelas_taxa = parcelas_taxa
        self.possui_criancas = possui_criancas

    def aluguel_mensal(self):
        return self.imovel.aluguel_mensal(self.possui_criancas)

    def valores_parcelas_taxa(self):
        """Divide a taxa em parcelas; a última absorve a diferença de centavos."""
        valor = round(self.TAXA_CONTRATUAL / self.parcelas_taxa, 2)
        parcelas = [valor] * (self.parcelas_taxa - 1)
        parcelas.append(round(self.TAXA_CONTRATUAL - sum(parcelas), 2))
        return parcelas

    def projecao_12_meses(self):
        """Retorna lista de dicts: um por mês, com aluguel, parcela da taxa, total e acumulado."""
        parcelas = self.valores_parcelas_taxa()
        aluguel = self.aluguel_mensal()
        linhas, acumulado = [], 0.0
        for mes in range(1, self.MESES_PROJECAO + 1):
            parcela = parcelas[mes - 1] if mes <= len(parcelas) else 0.0
            total = round(aluguel + parcela, 2)
            acumulado = round(acumulado + total, 2)
            linhas.append({"Mes": mes, "Aluguel": aluguel, "Parcela_Taxa": parcela,
                           "Total_Mes": total, "Acumulado": acumulado})
        return linhas

    def total_12_meses(self):
        return self.projecao_12_meses()[-1]["Acumulado"]

    def resumo(self):
        """Texto do orçamento detalhado."""
        def brl(v):
            return "R$ " + f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

        linhas = ["", "=" * 52, "        RENTSMART - ORÇAMENTO DE LOCAÇÃO", "=" * 52]
        linhas.append(f"Imóvel: {self.imovel.TIPO}")
        linhas.append("-" * 52)
        linhas.append("ALUGUEL MENSAL")
        for desc, valor in self.imovel.itens_detalhados(self.possui_criancas):
            texto = ("-" if valor < 0 else "") + brl(abs(valor))
            linhas.append(f"  {desc:<34}{texto:>15}")
        linhas.append(f"  {'TOTAL MENSAL':<34}{brl(self.aluguel_mensal()):>15}")
        linhas.append("-" * 52)
        linhas.append("TAXA CONTRATUAL (cobrada à parte)")
        linhas.append(f"  Valor total: {brl(self.TAXA_CONTRATUAL)}")
        parcelas = self.valores_parcelas_taxa()
        linhas.append(f"  Parcelamento: {len(parcelas)}x (última: {brl(parcelas[-1])})"
                      if parcelas[-1] != parcelas[0]
                      else f"  Parcelamento: {len(parcelas)}x de {brl(parcelas[0])}")
        linhas.append("-" * 52)
        linhas.append(f"Total pago nos primeiros 12 meses: {brl(self.total_12_meses())}")
        linhas.append("=" * 52)
        return "\n".join(linhas)

    def exportar_csv(self, caminho="projecao_12_meses.csv"):
        """Grava a projeção em CSV (separador ';' e UTF-8 com BOM: abre certo no Excel BR)."""
        with open(caminho, "w", newline="", encoding="utf-8-sig") as arq:
            escritor = csv.DictWriter(
                arq, fieldnames=["Mes", "Aluguel", "Parcela_Taxa", "Total_Mes", "Acumulado"],
                delimiter=";")
            escritor.writeheader()
            for linha in self.projecao_12_meses():
                escritor.writerow({k: (f"{v:.2f}".replace(".", ",") if k != "Mes" else v)
                                   for k, v in linha.items()})
        return caminho
