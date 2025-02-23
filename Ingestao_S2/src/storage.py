import json
import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Carregar variáveis de ambiente
load_dotenv()

# Configurar Supabase
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
bucket_name = os.getenv("BUCKET_NAME")

supabase: Client = create_client(supabase_url, supabase_key)

def upload_to_supabase(data, filename="pokemon.json"):
    try:
        # Converte JSON para bytes (binário)
        json_bytes = json.dumps(data, indent=4).encode("utf-8")

        print(f"\n📤 Enviando {filename} para o Supabase...")

        response = supabase.storage.from_(bucket_name).upload(
            path=f"pokemons/{filename}",  # Caminho dentro do bucket
            file=json_bytes,  # Arquivo em formato binário
            file_options={"content-type": "application/json"}
        )

        print(f"✅ Arquivo {filename} enviado com sucesso para o bucket {bucket_name}!")
        return response
    except Exception as e:
        print(f"❌ Erro ao enviar arquivo para o Supabase: {e}")
        return None