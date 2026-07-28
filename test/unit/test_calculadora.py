import pytest
from calculadora import calcula_preco_final, calcula_desconto, calcula_imposto
from app import app as flask_app

pytestmark = pytest.mark.unit


# -- Validações caminhos válidos: desconto --
@pytest.mark.parametrize(
    "preco, desconto, esperado",
    [
        (100, 10, 90.00),
        (100, 0, 100.0),
        (100, 100, 0.0),
    ],
)
def test_desconto_valido(preco, desconto, esperado):
    assert calcula_desconto(preco, desconto) == esperado


# -- Validações caminhos válidos: imposto --
@pytest.mark.parametrize(
    "preco, aliquota, esperado",
    [
        (90, 10, 99.0),
        (100, 0, 100.0),
    ],
)
def test_imposto_valido(preco, aliquota, esperado):
    assert calcula_imposto(preco, aliquota) == esperado


# -- Validações caminhos válidos: fluxo completo --
def test_calculadora_completa():
    assert calcula_preco_final(100, 10, 18) == 106.2


# -- Erros: todas as entradas inválidas juntas --
@pytest.mark.parametrize(
    "preco, desconto, aliquota",
    [
        (100, 101, 10),  # desconto maior que 100%
        (100, -10, 10),  # desconto negativo
        (100, 10, -10),  # imposto negativo
        (-100, 10, 10),  # preço negativo
    ],
)
def test_entradas_invalidas_levantam_erro(preco, desconto, aliquota):
    with pytest.raises(ValueError):
        calcula_preco_final(preco, desconto, aliquota)


# -- Teste Flask
@pytest.mark.parametrize(
    "querystring,esperado",
    [
        ("preco=100&desconto=10&aliquota=5", 200),
        ("preco=100&desconto=10", 400),  # falta param
        ("preco=abc&desconto=10&aliquota=5", 400),  # não-numérico
        ("preco=100&desconto=150&aliquota=5", 400),  # regra de negócio
        ("preco=-50&desconto=10&aliquota=5", 400),  # preço negativo
    ],
)
def test_calc_status(client, querystring, esperado):
    resp = client.get(f"/calc?{querystring}")
    assert resp.status_code == esperado


@pytest.fixture
def client():
    flask_app.config.update({"TESTING": True})
    with flask_app.test_client() as client:
        yield client


def test_calc_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json == {"status": "ok"}
