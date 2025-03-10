from setuptools import setup, find_packages

setup(
    name="meu_pacote",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "aiohappyeyeballs==2.4.6",
        "aiohttp==3.11.12",
        "aiosignal==1.3.2",
        "annotated-types==0.7.0",
        "anyio==4.8.0",
        "async-timeout==5.0.1",
        "attrs==25.1.0",
        "certifi==2025.1.31",
        "charset-normalizer==3.4.1",
        "deprecation==2.1.0",
        "exceptiongroup==1.2.2",
        "frozenlist==1.5.0",
        "gotrue==2.11.4",
        "h11==0.14.0",
        "h2==4.2.0",
        "hpack==4.1.0",
        "httpcore==1.0.7",
        "httpx==0.28.1",
        "hyperframe==6.1.0",
        "idna==3.10",
        "multidict==6.1.0",
        "packaging==24.2",
        "postgrest==0.19.3",
        "propcache==0.3.0",
        "pydantic==2.10.6",
        "pydantic_core==2.27.2",
        "python-dateutil==2.9.0.post0",
        "python-dotenv==1.0.1",
        "realtime==2.4.0",
        "requests==2.32.3",
        "six==1.17.0",
        "sniffio==1.3.1",
        "storage3==0.11.3",
        "StrEnum==0.4.15",
        "supabase==2.13.0",
        "supafunc==0.9.3",
        "typing_extensions==4.12.2",
        "urllib3==2.3.0",
        "websockets==14.2",
        "yarl==1.18.3",
    ],
    entry_points={
        "console_scripts": [
            "get_charmander=src.api:get_charmander",
            "get_bulbasaur=src.api:get_bulbasaur",
            "get_squirtle=src.api:get_squirtle",
        ],
    },
    author="Eduarda",
    description="Um pacote para obter informações de Pokémon e armazenar no Supabase",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)