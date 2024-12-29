# Monitoramento de Status de Serviço com Zabbix, Grafana e DownDetector

## Visão Geral

Este projeto oferece uma solução integrada para monitorar o status de serviços online usando o Zabbix para coleta de dados, Grafana para visualização, e DownDetector como fonte de dados. Ele é baseado no projeto original de [remontti - downdetector_zbx_grafana](https://github.com/remontti/downdetector_zbx_grafana) mas foi adaptado com várias melhorias para atender às minhas necessidades específicas e está funcionando de forma eficaz.

## Componentes Principais

- **Zabbix - Grafana - DownDetector**

## Arquivos Incluídos

- `downdetector.py`: Script principal para realizar consultas ao DownDetector intercalando tempo de consulta e pausas. 
- `downdetector_check.py`: Script auxiliar para verificar o status da consulta zabbix.
- `downdetectorDiscovery.py`: Script para descoberta automática de novos status consulta zabbix.
- `downdetectorlist.list`: Lista configurável de serviços a serem monitorados.
- `downdetector_result.json`: Arquivo que armazena os resultados das consultas.
- `zbx_templates.xml`: Template Zabbix para importar configurações de itens e triggers.
- `zbx_templates.xml`: Para visualização dos dados no painel.

## Pré-requisitos

- **Python 3**: Certifique-se de que o Python 3 está instalado.
- **Zabbix**: Com suporte para scripts externos.
- **Grafana**: Para visualização dos dados coletados.
- **Playwright**: Para automação de navegador.

## Instalação

#### Debian /Ubuntu ####
1. **Instale as dependências**:
```sh
sudo apt update
sudo apt install git
sudo apt install python3.9 python3.9-venv python3.9-dev
apt install python3-pip; \
pip install beautifulsoup4 playwright
```

2. **Clone o repositório e mova arquivos:**:
```sh
cd /tmp/
git clone https://github.com/davidebsen/zabbixdowndetector.git
cd zabbixdowndetector/
```
# Mover os arquivos para o diretório de scripts do Zabbix
```sh
sudo mv downdetector.py /usr/lib/zabbix/externalscripts
sudo mv downdetector_check.py /usr/lib/zabbix/externalscripts
sudo mv downdetectorDiscovery.py /usr/lib/zabbix/externalscripts
sudo mv downdetector_result.json /usr/lib/zabbix/externalscripts
sudo mv downdetectorlist.list /usr/lib/zabbix/externalscripts
```
# Ajustar as permissões dos arquivos
```sh
sudo chmod 755 /usr/lib/zabbix/externalscripts/downdetector.py
sudo chmod 755 /usr/lib/zabbix/externalscripts/downdetector_check.py
sudo chmod 755 /usr/lib/zabbix/externalscripts/downdetectorDiscovery.py
sudo chmod 755 /usr/lib/zabbix/externalscripts/downdetector_result.json
sudo chmod 755 /usr/lib/zabbix/externalscripts/downdetectorlist.list
```
# Alterar a propriedade dos arquivos para o usuário zabbix
```sh
sudo chown zabbix. /usr/lib/zabbix/externalscripts/downdetector*
```

3. **Configuração do Zabbix**:
- Importe zbx_templates.xml no Zabbix.

4. **Configuração do Grafana**:

- Importe o template JSON no Grafana.

5. **Configuração do Cron**:

Para automatizar a execução do script downdetector.py, configure o cron da seguinte forma:
- Executar Cron
```sh
crontab -e
```
- Executar em caso de reinicio do sistema:
```sh
@reboot /usr/bin/python3 /usr/lib/zabbix/externalscripts/downdetector.py
```
- Executar a cada 2 horas:
```sh
0 */2 * * * /usr/bin/python3 /usr/lib/zabbix/externalscripts/downdetector.py
```

6. **Configuração do downdetectorlist.list**:
Formato: status;site_id;Nome_do_Site
- 1: O serviço será monitorado.
- 0: O serviço não será monitorado.


Nota Importante: Alterar do tempo de consulta do script pode levar a bloqueios pelo Cloudflare, que reconhece consultas excessivas como atividades de bot. Faça alterações por sua conta e risco.
