#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import random
import json
import os
import asyncio
import time
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

# Lista de User-Agents
USER_AGENT_LIST = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
]

LOG_FILE = "/usr/lib/zabbix/externalscripts/downdetector.log"
RESULT_FILE = "/usr/lib/zabbix/externalscripts/downdetector_result.json"
SITES_FILE = "/usr/lib/zabbix/externalscripts/downdetectorlist.list"

def log_message(message):
    with open(LOG_FILE, 'a') as log_file:
        log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")

async def create_playwright_browser():
    """ Configura o Playwright com cabeçalhos e User-Agent """
    user_agent = random.choice(USER_AGENT_LIST)
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=True)
    context = await browser.new_context(
        user_agent=user_agent,
        viewport={'width': 1920, 'height': 1080},
        ignore_https_errors=True
    )
    return browser, context

async def make_request_playwright(site):
    """ Realiza uma requisição usando Playwright """
    url = f"https://downdetector.com.br/fora-do-ar/{site}/"
    browser, context = await create_playwright_browser()
    page = await context.new_page()
    try:
        await page.goto(url)
        await page.wait_for_timeout(10000)  # Aguarda o carregamento da página
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
        await page.wait_for_timeout(5000)  # Aguarda 5 segundos após a rolagem

        page_content = await page.content()
        return page_content
    except Exception as e:
        # log_message(f"Erro ao acessar o site com Playwright: {e}")
        return None
    finally:
        await browser.close()

def parse_status(response_text):
    """ Faz o parsing do HTML e identifica o status pelas classes """
    try:
        bs = BeautifulSoup(response_text, 'html.parser')
        success = bs.find("span", {"class": "color-success"})
        warning = bs.find("span", {"class": "color-warning"})
        danger = bs.find("span", {"class": "color-danger"})

        if success:
            return 'success'
        elif warning:
            return 'warning'
        elif danger:
            return 'danger'
        else:
            return None
    except Exception as e:
        # log_message(f"Erro ao processar a resposta: {e}")
        return None

def save_result(site, status):
    """ Salva o resultado no arquivo JSON """
    if os.path.exists(RESULT_FILE):
        with open(RESULT_FILE, 'r') as result_file:
            data = json.load(result_file)
    else:
        data = {}

    data[site] = status
    with open(RESULT_FILE, 'w') as result_file:
        json.dump(data, result_file, indent=4)

def load_sites():
    """ Carrega a lista de sites do arquivo """
    try:
        with open(SITES_FILE, 'r') as sites_file:
            sites = []
            for line in sites_file.readlines():
                line_data = line.rstrip().split(';')
                if line_data[0] == '1':
                    sites.append(line_data[1])
            return sites
    except Exception as e:
        # log_message(f"Erro ao carregar a lista de sites: {e}")
        return []

async def monitor_site(site):
    """ Monitora o status de um site periodicamente """
    response_text = await make_request_playwright(site)
    if not response_text:
        # log_message(f"Falha ao obter a resposta para o site: {site}")
        return

    status = parse_status(response_text)
    if not status:
        # log_message(f"Falha ao determinar o status para o site: {site}")
        return

    save_result(site, status)
    # log_message(f"Resultado salvo com sucesso para o site: {site}, Status: {status}")

async def main():
    request_count = 0
    start_time = time.time()
    max_runtime = 2 * 60 * 60  # 2 horas em segundos

    while True:
        if time.time() - start_time > max_runtime:
            # log_message("Tempo máximo de execução atingido. Encerrando o script.")
            break

        sites = load_sites()
        if not sites:
            # log_message("Não há sites para consultar.")
            sys.exit(0)

       
        random.shuffle(sites)

       
        for site in sites:
            await monitor_site(site)
            await asyncio.sleep(60)  # Aguarda 1 minuto entre cada consulta de site
            request_count += 1

            
            if request_count % 5 == 0:
                # log_message("Pausando por 2 minutos após 5 consultas.")
                await asyncio.sleep(120)  # Pausa por 2 minutos

       
            if request_count % 10 == 0:
                # log_message("Pausando por 4 minutos após 10 consultas.")
                await asyncio.sleep(240)  # Pausa por 4 minutos

   
        # log_message("Pausando por 30 minutos após terminar a lista de sites.")
        await asyncio.sleep(1800)  # Pausa por 30 minutos

if __name__ == '__main__':
    asyncio.run(main())