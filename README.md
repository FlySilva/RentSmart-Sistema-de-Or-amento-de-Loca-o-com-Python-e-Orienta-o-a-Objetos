# RentSmart - Orçamento de Locação (R.M Imóveis)

Aplicação em Python (POO) que calcula o orçamento mensal de locação, separa a taxa
contratual e gera a projeção de 12 meses em CSV.

## Como executar
Requisito: Python 3.8+ (sem bibliotecas externas).

```bash
python main.py
```
Responda às perguntas no terminal. Ao final, o orçamento é exibido e o arquivo
`projecao_12_meses.csv` é criado na pasta.

## Estrutura
| Arquivo | Conteúdo |
|---|---|
| `imoveis.py` | `Imovel` (classe abstrata), `Apartamento`, `Casa`, `Estudio` |
| `orcamento.py` | `Orcamento`: taxa contratual, parcelas, resumo e CSV |
| `main.py` | Interface de terminal e validação das entradas |

## Regras implementadas
- Aluguel-base: apartamento R$ 700, casa R$ 900, estúdio R$ 1.200.
- 2 quartos: +R$ 200 (apartamento) / +R$ 250 (casa).
- Garagem (casa/apartamento): +R$ 300.
- Estúdio: pacote de 2 vagas R$ 250 + R$ 60 por vaga adicional.
- Apartamento sem crianças: 5% de desconto sobre o aluguel após os adicionais.
- Taxa contratual: R$ 2.000 em 1 a 5 parcelas, mostrada separada do aluguel.

## Decisões de interpretação
- O desconto de 5% incide sobre base + quartos + garagem.
- Estacionamento do estúdio é opcional; se contratado, o mínimo é o pacote de 2 vagas.
- As parcelas da taxa são cobradas nos primeiros meses; a última ajusta os centavos.
- CSV com separador `;` e vírgula decimal, para abrir corretamente no Excel em português.

## Exemplo de saída (CSV)
Colunas: `Mes;Aluguel;Parcela_Taxa;Total_Mes;Acumulado`
