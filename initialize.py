#initialize.py
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import platform
import shutil
import subprocess
import sys
import socket
from dotenv import load_dotenv

load_dotenv()

environment_type = os.getenv('ENVIRONMENT_TYPE', 'development').upper()
# Configurações de IP para Staging e Produção
STAGING_IPS = os.getenv('STAGING_IPS', '').split(',')
PRODUCTION_IPS = os.getenv('PRODUCTION_IPS', '').split(',')  

def is_windows():
    """Verifica se o sistema operacional é Windows."""
    return platform.system().lower() == 'windows'

def get_linux_ip_address():
    """Obtém o endereço IP local em uma máquina Linux."""
    try:
        # Cria um socket temporário para determinar o IP local
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Conecta a um servidor DNS público (não envia dados)
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
    except Exception as e:
        print(f"Não foi possível obter o endereço IP: {e}")
        return None

def find_docker_compose_file():
    """
    Verifica a existência do arquivo docker-compose.yml.

    Retorna o caminho do arquivo se encontrado, caso contrário, None.
    """
    docker_compose_file = "docker/docker-compose.yml"
    
    print(f"Checking for docker-compose file at: {os.path.abspath(docker_compose_file)}") # Debug
    if not os.path.exists(docker_compose_file):
        print(f"Erro: Arquivo {docker_compose_file} não encontrado.")
        return None
        
    return docker_compose_file

def remove_existing_containers(docker_compose_file):
    """Remove os containers existentes."""

    print("Parando e removendo containers existentes...")
    down_command = ["docker", "compose", "-f", docker_compose_file, "down"]
    if is_windows():
        subprocess.run(down_command, shell=True, check=True)
    else:
        subprocess.run(down_command, check=True)
    
    return True

def define_command_docker_compose_linux(docker_compose_file):
    # Em sistemas Linux, usa o perfil de produção
    print("Executando docker-compose no Linux com perfil de produção...")
    #command = ["docker", "compose", "-f", docker_compose_file, "--profile", "production", "up", "--build", "-d"]
    #command = ["docker", "compose", "-f", docker_compose_file, "--profile", "staging", "up", "--build", "-d"]
    ip_address = get_linux_ip_address()
    if ip_address:
        print(f"Endereço IP detectado: {ip_address}")
        # Os IPs de staging e produção agora são globais (STAGING_IPS, PRODUCTION_IPS)

        if ip_address in STAGING_IPS:
            print("Configurando para ambiente de Staging com base no IP.")
            command = ["docker", "compose", "-f", docker_compose_file, "--profile", "development", "up", "--build", "-d"]
        elif ip_address in PRODUCTION_IPS:
            print("Configurando para ambiente de Produção com base no IP.")
            command = ["docker", "compose", "-f", docker_compose_file, "--profile", "development", "up", "--build", "-d"]
        else:
            print("IP não corresponde a Staging nem Produção. Usando perfil padrão (staging).")
            command = ["docker", "compose", "-f", docker_compose_file, "--profile", "development", "up", "--build", "-d"]
    else:
        print("Não foi possível obter o IP. Usando perfil padrão (staging).")
        command = ["docker", "compose", "-f", docker_compose_file, "--profile", "staging", "up", "--build", "-d"]
    
    print(f"Comando para executar docker-compose: {command}") # Debug
    return command

def run_docker_compose():
    """Executa os passos para iniciar o docker-compose com base no sistema operacional."""

    print(f"Current working directory: {os.getcwd()}") # Debug

    # Primeiro, encontra o arquivo docker-compose.yml
    docker_compose_file = find_docker_compose_file()
    if not docker_compose_file: return False
    
    # Segundo, remove os containers online relacionados ao arquivo docker-compose.yml
    remove_existing_containers(docker_compose_file)

    try:
        # Comando para executar docker-compose
        if platform.system().lower() == 'linux': 
            command = define_command_docker_compose_linux(docker_compose_file)
        else:
            print("Comando para executar docker-compose no Windows/Mac com perfil de desenvolvimento...")
            command = ["docker", "compose", "-f", docker_compose_file, "--profile", "development", "up", "--build", "-d"]
        
        # Formato de execução do docker-compose para windows e diferentes sistemas operacionais
        if is_windows():
            print("Executando docker-compose no Windows...")
            result = subprocess.run(command, shell=True, check=True)
        else:
            print("Executando docker-compose no Linux/Mac...")
            result = subprocess.run(command, check=True)
        
        if result.returncode == 0:
            print("Docker Compose executado com sucesso!")
            return True
        else:
            print(f"Erro ao executar Docker Compose. Código de saída: {result.returncode}")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar Docker Compose: {e}")
        return False
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return False

def main():
    """Função principal."""
    # Muda o diretório de trabalho para o diretório deste arquivo initialize.py
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    print(f"Changed working directory to: {os.getcwd()}") # Debug
    
    print(f"Iniciando configuração no sistema operacional: {platform.system()}")

    # Verifica e imprime o IP (se Linux)
    if platform.system().lower() == 'linux':
        ip_address = get_linux_ip_address()
        if ip_address: print(f"Endereço IP: {ip_address}")
        else: pass # A função get_linux_ip_address já imprime mensagem de erro, nenhuma ação adicional necessária aqui
    elif platform.system().lower() != 'windows':
        print(f"Sistema operacional: {platform.system()} (não Windows nem Linux)")
    
    # Executa o docker-compose
    if run_docker_compose():
        print("Inicialização concluída com sucesso!")
    else:
        print("Falha ao executar docker-compose.")
        sys.exit(1)
    

if __name__ == "__main__":
    main() 