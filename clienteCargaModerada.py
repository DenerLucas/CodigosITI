import requests
import time

POST_URL = "http://192.168.1.2:8081/files"
GET_URL = "http://192.168.1.2:8081/files/{}"

def post_file(file_name, key, length):
    data = {
        'fileName': file_name,
        'key': key,
        'length': length
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(POST_URL, json=data, headers=headers)
    
    if response.status_code == 201:
        print(f"Arquivo {file_name} enviado com sucesso.")
    else:
        print(f"Falha ao enviar o arquivo. Status code: {response.status_code}")
    
    return response.elapsed.total_seconds()

def get_file(file_name, key):
    url = GET_URL.format(file_name)
    data = {'key': key}
    headers = {'Content-Type': 'application/json'}
    response = requests.get(url, json=data, headers=headers)
    
    if response.status_code == 200:
        print(f"Arquivo {file_name} baixado com sucesso.")
    else:
        print(f"Falha ao baixar o arquivo. Status code: {response.status_code}")
    
    return response.elapsed.total_seconds()

if __name__ == "__main__":
    start_time = time.time()
    key = "abcdefghijklmnop"
    file_name = "medium_load_file.txt"
    length = 500

    operation_count = 0

    while time.time() - start_time < 60:  # Executa por 1 minuto
        post_time = post_file(file_name, key, length)
        print(f"Tempo de upload: {post_time:.2f} segundos")
        
        get_time = get_file(file_name, key)
        print(f"Tempo de download: {get_time:.2f} segundos")
        
        operation_count += 1
        time.sleep(0.2)  # Intervalo de 0.2 segundos (5 operações por segundo)

    print(f"Total de operações realizadas em 1 minuto: {operation_count}")
