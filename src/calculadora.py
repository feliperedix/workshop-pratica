import argparse


def calcula_desconto(preco_base: float, desconto: int) -> float:
    if preco_base < 0:
        raise ValueError("Preço base não pode ser negativo")
    if desconto < 0 or desconto > 100:
        raise ValueError("Desconto deve estar entre 0 e 100")
    valor_com_desconto = preco_base - ((preco_base * desconto) / 100)
    return round(valor_com_desconto, 2)


def calcula_imposto(preco: float, aliquota_imposto: float) -> float:
    if aliquota_imposto < 0:
        raise ValueError("Alíquota não pode ser negativa")
    valor_com_imposto = preco + ((preco * aliquota_imposto) / 100)
    return round(valor_com_imposto, 2)


def calcula_preco_final(
    preco_base: float, desconto: int, aliquota_imposto: float
) -> float:
    preco_com_desconto = calcula_desconto(preco_base, desconto)
    preco_com_imposto = calcula_imposto(preco_com_desconto, aliquota_imposto)
    return preco_com_imposto


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="A script to process custom double-dash flags."
    )
    parser.add_argument("--preco", type=float, help="Preço do produto")
    parser.add_argument("--desconto", type=int, help="Desconto do produto")
    parser.add_argument("--aliquota", type=float, help="Alíquota de imposto do produto")

    args = parser.parse_args()
    if args.preco is None:
        args.preco = float(input("Informe o preço base: "))
    if args.desconto is None:
        args.desconto = int(input("Informe o desconto: "))
    if args.aliquota is None:
        args.aliquota = float(input("Informe a aliquota de imposto: "))
    print(calcula_preco_final(args.preco, args.desconto, args.aliquota))
