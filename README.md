# Monitoramento de Status de Serviço com Zabbix, Grafana e DownDetector

## Visão Geral

Este projeto oferece uma solução integrada para monitorar o status de serviços online usando o Zabbix para coleta de dados, Grafana para visualização, e DownDetector como fonte de dados. Ele é baseado no projeto original de [remontti - downdetector_zbx_grafana](https://github.com/remontti/downdetector_zbx_grafana) mas foi adaptado com várias melhorias para atender às minhas necessidades específicas e está funcionando de forma eficaz.

## Componentes Principais

- **Zabbix**: Utilizado para coletar e armazenar dados de status de serviços.
- **Grafana**: Ferramenta de visualização para apresentar os dados de forma gráfica.
- **DownDetector**: Fonte de informações de status dos serviços monitorados.

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
  - Instalação: `pip install playwright`
  - Inicialização: `playwright install`

## Instalação

1. **Clone o repositório**:
   git clone https://github.com/seuusuario/seuprojeto.git
   cd seuprojeto

2. **Configuração do Zabbix**:

- Importe zbx_templates.xml no Zabbix.
- Coloque downdetector.py, downdetector_check.py, e downdetectorDiscovery.py em /usr/lib/zabbix/externalscripts. com permissoes 0755

3. **Configuração do Grafana**:

- Importe o template JSON no Grafana.

4. **Configuração do Cron**:

Para automatizar a execução do script downdetector.py, configure o cron da seguinte forma:

- Executar em caso de reinicio do sistema:
  @reboot /usr/bin/python3 /usr/lib/zabbix/externalscripts/downdetector.py

- Executar a cada 2 horas:
  0 */2 * * * /usr/bin/python3 /usr/lib/zabbix/externalscripts/downdetector.py


4. **Configuração do downdetectorlist.list**:
Formato: status;site_id;Nome_do_Site
- 1: O serviço será monitorado.
- 0: O serviço não será monitorado.


Nota Importante: Alterar do tempo de consulta do script pode levar a bloqueios pelo Cloudflare, que reconhece consultas excessivas como atividades de bot. Faça alterações por sua conta e risco.
