#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import json
import os

RESULT_FILE = "/usr/lib/zabbix/externalscripts/downdetector_result.json"

def load_result():
    """ Carrega o resultado do arquivo JSON """
    try:
        with open(RESULT_FILE, 'r') as result_file:
            data = json.load(result_file)
            return data
    except Exception as e:
        print(f"Erro ao ler o arquivo de resultado: {e}")
        return None

def output_result(status):
    """ Exibe o status final baseado no código """
    status_mapping = {'success': 1, 'warning': 2, 'danger': 3}
    print(status_mapping.get(status, 0))
    sys.exit(0)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(0)
        sys.exit(0)

    site = sys.argv[1]
    try:
        data = load_result()
        if not data:
            print(0)
            sys.exit(0)

        status = data.get(site, None)
        if not status:
            print(0)
            sys.exit(0)

        output_result(status)
    except Exception as e:
        print(0)
        sys.exit(0)