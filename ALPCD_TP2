from pkgutil import get_data
import requests
from bs4 import BeautifulSoup
import typer
import csv
import json
import re
import sys
from collections import defaultdict
from collections import Counter
from playwright.sync_api import sync_playwright
import math
from typing import Annotated, Optional

app = typer.Typer()

BASE_URL2 = "https://www.ambitionbox.com/jobs/search"
url = "https://api.itjobs.pt/job"
BASE_URL = "https://www.ambitionbox.com/list-of-companies?campaign=desktop_nav"
API_KEY = "09ad1042ebaf1704533805cd2fab64f1"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0"}


def request_api(metodo, params):
    url = "https://api.itjobs.pt/job"
    params['api_key'] = API_KEY

    if 'limit' in params:
        tamanho_pagina = 500
        total = params['limit']

        if total < tamanho_pagina:
            tamanho_pagina = total

        paginas_totais = (total // tamanho_pagina) + (1 if total % tamanho_pagina != 0 else 0)
        resultado = []

        for page in range(1, paginas_totais + 1):
            params['limit'] = tamanho_pagina
            params['page'] = page

            response = requests.get(f"{url}/{metodo}.json", headers=HEADERS, params=params)

            if response.status_code == 200:
                response_data = response.json()
                if 'results' in response_data:
                    resultado.extend(response_data['results'])
                if len(resultado) >= total:
                    break
                if len(response_data['results']) < tamanho_pagina:
                    break
            else:
                print(f"Erro ao acessar a API: {response.status_code}")
                return {}

        return {"results": resultado}

    else:
        response = requests.get(f"{url}/{metodo}.json", HEADERS={}, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Erro ao acessar a API: {response.status_code}")
            return {}

#a
def fetch_job_details(job_id: int):
    """
    Busca detalhes de um trabalho usando a API ITJobs.
    """
    url = f"https://api.itjobs.pt/job/get.json?api_key={API_KEY}&id={job_id}"
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        typer.echo(f"Erro ao acessar a API ITJobs: {e}")
        return None

def fetch_company_info(company_name: str):
    """
    Obtém informações sobre a empresa usando a página overview do AmbitionBox.
    """
    company_slug = company_name.lower().replace(" ", "-").replace(".", "-")
    url = f"https://www.ambitionbox.com/overview/{company_slug}-overview"

    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            typer.echo(f"Erro ao acessar {url}. Status Code: {response.status_code}")
            return {
                "rating": "N/A",
                "description": "Informações indisponíveis",
                "benefits": "Informações indisponíveis"
            }

        soup = BeautifulSoup(response.content, 'html.parser')

        # Procurar rating
        rating_tag = soup.find("span", class_="css-1jxf684 text-primary-text font-pn-700 text-[32px]")
        rating = rating_tag.text.strip() if rating_tag else "N/A"

        # Procurar descrição
        description_tag = soup.find("div", class_="css-146c3p1 font-pn-400 text-sm text-neutral mb-2")
        description = description_tag.text.strip() if description_tag else "Informações indisponíveis"

        # Procurar benefícios
        benefits_tags = soup.find_all("div", class_="css-146c3p1 font-pn-400 text-sm text-primary-text")
        benefits = [benefit.text.strip() for benefit in benefits_tags]
        benefits = ", ".join(benefits) if benefits else "Informações indisponíveis"

        return {
            "rating": rating,
            "description": description,
            "benefits": benefits
        }

    except requests.RequestException as e:
        typer.echo(f"Erro ao acessar o AmbitionBox: {e}")
        return {
            "rating": "N/A",
            "description": "Informações indisponíveis",
            "benefits": "Informações indisponíveis"
        }

@app.command("get")  # Adicionado este decorator
def get(job_id: int = typer.Argument(..., help="ID do trabalho a ser consultado"), export_csv: bool = False):
    """
    Busca informações de um trabalho usando o ITJobs e complementa com dados da empresa no AmbitionBox.
    
    Arguments:
        job_id: ID do trabalho a ser consultado.
        export_csv: Se verdadeiro, salva os resultados em um arquivo CSV.
    """
    job_details = fetch_job_details(job_id)
    if not job_details or 'error' in job_details:
        typer.echo(f"Trabalho com ID {job_id} não encontrado.")
        return

    company_name = job_details.get("company", {}).get("name", "N/A")
    company_info = fetch_company_info(company_name)

    result = {
        "job_id": job_id,
        "title": job_details.get("title", "N/A"),
        "company": company_name,
        "location": job_details.get("locations", [{}])[0].get("name", "N/A"),
        **company_info
    }

    typer.echo(json.dumps(result, indent=4, ensure_ascii=False))

    if export_csv:
        with open(f"job_{job_id}_details.csv", "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=result.keys())
            writer.writeheader()
            writer.writerow(result)
        typer.echo(f"Informações exportadas para job_{job_id}_details.csv")

#b
# Função para buscar informações da empresa no AmbitionBox

@app.command()
def statistics(region: str):
    """Filtra os dados do trabalho por localização e gera um arquivo CSV."""
    params = {"limit": 1500}
    jobs_data = request_api("search", params)

    if not jobs_data or "results" not in jobs_data:
        print("Erro: não é possível recuperar dados do trabalho.")
        return

    filtered_jobs = []

    for job in jobs_data["results"]:
        for location in job.get("locations", []):
            area = location["name"]

            if region.lower() in area.lower():
                filtered_jobs.append({
                    "title": job.get("title", "Not specified"),
                    "type": ", ".join(t["name"] for t in job.get("types", [])) or "Not specified",
                    "area": area
                })

    if not filtered_jobs:
        print(f"Nenhuma vaga encontrada para a região: {region}")
        return

    file_name = f"filtered_jobs_{region.replace(' ', '_').lower()}.csv"
    with open(file_name, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["title", "type", "area"])
        writer.writeheader()
        writer.writerows(filtered_jobs)

    print(f"Ficheiro CSV '{file_name}' criado com sucesso.")

@app.command()
def list_skills(main_url: str, export_csv: bool = False):
    """
    Pesquisa os 10 primeiros trabalhos e extrai as skills de cada trabalho,
    exibindo a contagem de ocorrências em formato JSON.
    Caso --export-csv seja passado, salva os resultados em um arquivo CSV.
    """
    # Fazer a requisição para a página principal
    response = requests.get(main_url, headers=HEADERS)
    if response.status_code != 200:
        print(f"Erro ao acessar a URL principal: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    # Encontrar os links dos 10 primeiros trabalhos
    job_cards = soup.find_all('div', class_='jobsInfoCardCont', limit=10)
    if not job_cards:
        print("Nenhum trabalho encontrado.")
        return

    all_skills = []

    for i, job_card in enumerate(job_cards, start=1):
        # Encontrar o link para a página do trabalho
        job_link = job_card.find('a', class_='title noclick')
        if job_link:
            job_url = "https://www.ambitionbox.com" + job_link['href']
            print(f"Trabalho {i}: {job_url}")

            # Fazer a requisição para a página do trabalho
            job_response = requests.get(job_url, headers=HEADERS)
            if job_response.status_code != 200:
                print(f"Erro ao acessar a página do trabalho {i}: {job_response.status_code}")
                continue

            job_soup = BeautifulSoup(job_response.text, 'html.parser')

            # Extrair as skills da página do trabalho
            skills_elements = job_soup.find_all('a', class_='body-medium chip')
            job_skills = [skill.get_text(strip=True) for skill in skills_elements]

            print(f"Skills do trabalho {i}: {job_skills}")
            all_skills.extend(job_skills)

    # Contar as habilidades repetidas
    skill_counts = Counter(all_skills)

    # Converter para o formato JSON
    result = [{"skill": skill, "count": count} for skill, count in skill_counts.items()]

    # Exibir o resultado em formato JSON
    print(json.dumps(result, indent=4))

    # Exportar para CSV se a flag for passada
    if export_csv:
        csv_filename = "skills_count.csv"
        with open(csv_filename, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["skill", "count"])
            writer.writeheader()
            writer.writerows(result)
        print(f"Resultados exportados para {csv_filename}")




def fetch_job_details(job_id: int):
    """
    Busca detalhes de um trabalho usando a API ITJobs.
    """
    url = f"https://api.itjobs.pt/job/get.json?api_key={API_KEY}&id={job_id}"
    try:
        response = requests.get(url, headers=HEADERS)
    
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        typer.echo(f"Erro ao acessar a API ITJobs: {e}")
        return None

def fetch_indeed_company_info(company_name: str):
    """
    Obtém informações sobre a empresa usando a página de overview do Indeed.
    """
    company_slug = company_name.lower().replace(" ", "-").replace(".", "-")
    url = f"https://www.indeed.com/cmp/{company_slug}"

    try:
        response = requests.get(url, headers= HEADERS)
        if response.status_code == 403:
            typer.echo(f"Erro ao acessar {url}. Status Code: 403 - Possível bloqueio de robôs.")
            return {
                "rating": "N/A",
                "review_count": "N/A",
                "benefits": "Informações indisponíveis"
            }
        elif response.status_code != 200:
            typer.echo(f"Erro ao acessar {url}. Status Code: {response.status_code}")
            return {
                "rating": "N/A",
                "review_count": "N/A",
                "benefits": "Informações indisponíveis"
            }

        soup = BeautifulSoup(response.content, 'html.parser')

        # Procurar rating
        rating_tag = soup.find("meta", {"name": "ratingValue"})
        rating = rating_tag["content"] if rating_tag else "N/A"

        # Procurar número de reviews
        review_tag = soup.find("meta", {"name": "reviewCount"})
        review_count = review_tag["content"] if review_tag else "N/A"

        # Procurar benefícios
        benefits_section = soup.find("div", class_="css-1qibq6a")
        benefits = benefits_section.text.strip() if benefits_section else "Informações indisponíveis"

        return {
            "rating": rating,
            "review_count": review_count,
            "benefits": benefits
        }

    except requests.RequestException as e:
        typer.echo(f"Erro ao acessar o Indeed: {e}")
        return {
            "rating": "N/A",
            "review_count": "N/A",
            "benefits": "Informações indisponíveis"
        }

def fetch_qualifications(job_details):
    """
    Busca as qualificações do trabalho fornecidas pelos detalhes do emprego.
    """
    qualifications = job_details.get("qualifications", "Informações não disponíveis")
    return qualifications

@app.command("get2")
def get2(job_id: int = typer.Argument(..., help="ID do trabalho a ser consultado"), export_csv: bool = False):
    """
    Busca informações de um trabalho usando o ITJobs e complementa com dados da empresa no Indeed.

    Arguments:
        job_id: ID do trabalho a ser consultado.
        export_csv: Se verdadeiro, salva os resultados em um arquivo CSV.
    """
    job_details = fetch_job_details(job_id)
    if not job_details or 'error' in job_details:
        typer.echo(f"Trabalho com ID {job_id} não encontrado.")
        return

    company_name = job_details.get("company", {}).get("name", "N/A")
    company_info = fetch_indeed_company_info(company_name)
    qualifications = fetch_qualifications(job_details)

    result = {
        "job_id": job_id,
        "title": job_details.get("title", "N/A"),
        "company": company_name,
        "location": job_details.get("locations", [{}])[0].get("name", "N/A"),
        "qualifications": qualifications,
        **company_info
    }

    typer.echo(json.dumps(result, indent=4, ensure_ascii=False))

    if export_csv:
        with open(f"job_{job_id}_indeed_details.csv", "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=result.keys())
            writer.writeheader()
            writer.writerow(result)
        typer.echo(f"Informações exportadas para job_{job_id}_indeed_details.csv")

if __name__ == "__main__":
    app()
