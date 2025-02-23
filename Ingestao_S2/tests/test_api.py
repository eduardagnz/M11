import pytest
import requests
from unittest.mock import patch, MagicMock
from src.api import get_charmander, get_bulbasaur, get_squirtle

mock_pokemon_data = {
    "charmander": {"name": "Charmander", "type": "Fire"},
    "bulbasaur": {"name": "Bulbasaur", "type": "Grass"},
    "squirtle": {"name": "Squirtle", "type": "Water"},
}

class MockResponse:
    def __init__(self, json_data, status_code=200):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data

    def raise_for_status(self):
        if self.status_code != 200:
            raise requests.exceptions.HTTPError(f"HTTP {self.status_code}")

@pytest.mark.parametrize("pokemon, function", [
    ("charmander", get_charmander),
    ("bulbasaur", get_bulbasaur),
    ("squirtle", get_squirtle),
])
@patch("src.api.requests.get")
@patch("src.api.upload_to_supabase")
def test_get_pokemon(mock_upload, mock_get, pokemon, function):
    """Testa as funções de busca dos Pokémon e upload para o Supabase"""
    mock_get.return_value = MockResponse(mock_pokemon_data[pokemon])

    function()

    mock_get.assert_called_once_with(f"https://pokeapi.co/api/v2/pokemon/{pokemon}")

    mock_upload.assert_called_once_with(mock_pokemon_data[pokemon])


@patch("src.api.requests.get")
def test_get_pokemon_request_error(mock_get):
    """Testa erro de requisição na API"""
    mock_get.side_effect = requests.exceptions.RequestException("Erro na requisição")

    with patch("builtins.print") as mock_print:
        get_charmander()  # Testa com Charmander, mas pode ser qualquer Pokémon
        mock_print.assert_called_with("Erro ao buscar Charmander: Erro na requisição")