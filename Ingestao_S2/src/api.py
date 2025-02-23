import requests
from .storage import upload_to_supabase

BASE_URL = "https://pokeapi.co/api/v2/pokemon/"

def get_charmander():
    try:
        response = requests.get(f"{BASE_URL}charmander")
        response.raise_for_status()
        upload_to_supabase(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar Charmander: {e}")


def get_bulbasaur():
    try:
        response = requests.get(f"{BASE_URL}bulbasaur")
        response.raise_for_status()
        upload_to_supabase(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar Bulbasaur: {e}")


def get_squirtle():
    try:
        response = requests.get(f"{BASE_URL}squirtle")
        response.raise_for_status()
        upload_to_supabase(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar Squirtle: {e}")
