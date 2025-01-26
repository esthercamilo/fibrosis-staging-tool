import time

import requests

for i in range(10):
    # URL de exemplo
    url = "https://zineverdeverso.noblogs.org/o-blog-definitivo/"

    # Header simulando um navegador de computador
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
        )
    }

    # Fazendo a request com o header
    response = requests.get(url, headers=headers)

    # Verificando o status e conteúdo da resposta
    print(response.status_code)
    time.sleep(5)
