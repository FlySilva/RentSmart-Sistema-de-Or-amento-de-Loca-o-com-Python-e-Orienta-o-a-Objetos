"""RentSmart - interface de terminal: coleta e valida os dados, monta o orçamento."""
from imoveis import Apartamento, Casa, Estudio
from orcamento import Orcamento


def ler_inteiro(mensagem, minimo, maximo):
    """Repete a pergunta até o usuário digitar um inteiro dentro do intervalo."""
    while True:
        texto = input(mensagem).strip()
        if texto.lstrip("-").isdigit() and minimo <= int(texto) <= maximo:
            return int(texto)
        print(f"  Entrada inválida. Digite um número inteiro de {minimo} a {maximo}.")


def ler_sim_nao(mensagem):
    while True:
        texto = input(mensagem + " (s/n): ").strip().lower()
        if texto in ("s", "sim"):
            return True
        if texto in ("n", "nao", "não"):
            return False
        print("  Entrada inválida. Digite 's' ou 'n'.")


def montar_imovel():
    print("\nTipo de imóvel:\n  1 - Apartamento\n  2 - Casa\n  3 - Estúdio")
    tipo = ler_inteiro("Escolha: ", 1, 3)
    possui_criancas = True

    if tipo == 3:
        print("\nEstúdio: pacote inicial de 2 vagas (R$ 250,00) + R$ 60,00 por vaga extra.")
        if ler_sim_nao("Deseja estacionamento?"):
            vagas = ler_inteiro("Quantas vagas no total (mínimo 2, máximo 10)? ", 2, 10)
        else:
            vagas = 0
        return Estudio(vagas), possui_criancas

    quartos = ler_inteiro("Quantidade de quartos (1 ou 2): ", 1, 2)
    vagas = 1 if ler_sim_nao("Deseja vaga de garagem?") else 0
    if tipo == 1:
        possui_criancas = ler_sim_nao("Possui crianças?")
        return Apartamento(quartos, vagas), possui_criancas
    return Casa(quartos, vagas), possui_criancas


def main():
    print("RentSmart - R.M Imóveis")
    imovel, possui_criancas = montar_imovel()
    parcelas = ler_inteiro("\nTaxa contratual de R$ 2.000,00 em quantas parcelas (1 a 5)? ", 1, 5)

    orcamento = Orcamento(imovel, parcelas, possui_criancas)
    print(orcamento.resumo())
    arquivo = orcamento.exportar_csv()
    print(f"\nProjeção de 12 meses salva em: {arquivo}")


if __name__ == "__main__":
    main()
