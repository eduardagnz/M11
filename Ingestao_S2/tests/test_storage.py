import pytest
import json
from unittest.mock import patch, MagicMock
from src.storage import upload_to_supabase

mock_data = {"name": "Charmander", "type": "Fire"}
mock_filename = "charmander.json"

@patch("src.storage.supabase")
def test_upload_to_supabase(mock_supabase):
    """Testa o upload de um arquivo JSON para o Supabase."""
    mock_storage = mock_supabase.storage.from_.return_value
    mock_storage.upload.return_value = {"status": "success"}

    response = upload_to_supabase(mock_data, mock_filename)

    mock_storage.upload.assert_called_once_with(
        path=f"pokemons/{mock_filename}",
        file=json.dumps(mock_data, indent=4).encode("utf-8"),
        file_options={"content-type": "application/json"}
    )
    
    assert response == {"status": "success"}


@patch("src.storage.supabase")
def test_upload_to_supabase_failure(mock_supabase):
    """Testa falha ao enviar um arquivo para o Supabase."""
    mock_storage = mock_supabase.storage.from_.return_value
    mock_storage.upload.side_effect = Exception("Erro ao enviar")

    with patch("builtins.print") as mock_print:
        response = upload_to_supabase(mock_data, mock_filename)
        
        mock_storage.upload.assert_called_once()
        mock_print.assert_called_with("❌ Erro ao enviar arquivo para o Supabase: Erro ao enviar")
        assert response is None
