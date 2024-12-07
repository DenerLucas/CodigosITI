import requests
import time

# URLs para POST e GET no balanceador
POST_URL = "http://192.168.1.2/files"  # Substitua pelo endereço do Traefik
GET_URL = "http://192.168.1.2/files/{}"  # Substitua pelo endereço do Traefik

def post_file(file_name, key, length):
    """
    Envia um arquivo para o servidor via POST e coleta métricas.
    """
    data = {
        'fileName': file_name,
        'key': key,
        'length': length
    }
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(POST_URL, json=data, headers=headers, timeout=5)
        elapsed_time = response.elapsed.total_seconds()

        if response.status_code == 200:
            print(f"[POST] Arquivo {file_name} enviado com sucesso.")
        else:
            print(f"[POST] Falha ao enviar arquivo. Status code: {response.status_code}")

        # Coletar o servidor que respondeu (se disponível nos cabeçalhos)
        server = response.headers.get("Server", "Desconhecido")

        return elapsed_time, server

    except requests.exceptions.RequestException as e:
        print(f"[POST] Erro na requisição: {e}")
        return None, None


def get_file(file_name, key):
    """
    Faz o download de um arquivo do servidor via GET e coleta métricas.
    """
    url = GET_URL.format(file_name)
    data = {'key': key}
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.get(url, json=data, headers=headers, timeout=5)
        elapsed_time = response.elapsed.total_seconds()

        if response.status_code == 200:
            print(f"[GET] Arquivo {file_name} baixado com sucesso.")
        else:
            print(f"[GET] Falha ao baixar arquivo. Status code: {response.status_code}")

        # Coletar o servidor que respondeu (se disponível nos cabeçalhos)
        server = response.headers.get("Server", "Desconhecido")

        return elapsed_time, server

    except requests.exceptions.RequestException as e:
        print(f"[GET] Erro na requisição: {e}")
        return None, None


if __name__ == "__main__":
    # Configuração inicial
    start_time = time.time()
    key = "abcdefghijklmnop"  # Chave de 16 bytes como esperado pelo servidor
    length = 100000 # Tamanho do arquivo
    operation_count = 0  # Contador de operações

    # Armazenar métricas
    metrics = {
        "POST": [],
        "GET": []
    }
    servers_used = {
        "POST": {},
        "GET": {}
    }

    # Executa os ciclos de operações por 1 minuto
    while time.time() - start_time < 60:  # 1 minuto de teste
        file_name = f"testfile_{operation_count}.txt"

        # Realiza o POST
        post_time, post_server = post_file(file_name, key, length)
        if post_time is not None:
            metrics["POST"].append(post_time)
            servers_used["POST"][post_server] = servers_used["POST"].get(post_server, 0) + 1
            print(f"Tempo de upload: {post_time:.2f} segundos - Servidor: {post_server}")

        # Realiza o GET
        get_time, get_server = get_file(file_name, key)
        if get_time is not None:
            metrics["GET"].append(get_time)
            servers_used["GET"][get_server] = servers_used["GET"].get(get_server, 0) + 1
            print(f"Tempo de download: {get_time:.2f} segundos - Servidor: {get_server}")

        operation_count += 1
        time.sleep(0.05)  # Pequeno intervalo entre as operações

    # Exibe resumo das métricas
    print("\nResumo de métricas:")
    print(f"Total de operações realizadas: {operation_count}")
    print(f"Média de tempo de upload (POST): {sum(metrics['POST']) / len(metrics['POST']):.2f} segundos")
    print(f"Média de tempo de download (GET): {sum(metrics['GET']) / len(metrics['GET']):.2f} segundos")

    print("\nDistribuição de servidores utilizados:")
    for operation, servers in servers_used.items():
        print(f"\n{operation}:")
        for server, count in servers.items():
            print(f"  Servidor: {server} - Requisições: {count}")
