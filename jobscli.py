import typer
import requests
import re
import csv
import json
import datetime

app = typer.Typer()

BASE_URL = "https://api.itjobs.pt/job/list.json"
BASE_URL2 = "https://api.itjobs.pt/job/search.json"
BASE_URL3 = "https://api.itjobs.pt/job/get.json"
API_KEY = "abb6681e6327ee767a67008c1f40d190"
CIDADES = {
    "Açores": 2,
    "Aveiro": 1,
    "Beja": 3,
    "Braga": 4,
    "Bragança": 5,
    "Castelo Branco": 6,
    "Coimbra": 8,
    "Évora": 10,
    "Faro": 9,
    "Guarda": 11,
    "Internacional": 29,
    "Leiria": 13,
    "Lisboa": 14,
    "Madeira": 15,
    "Portalegre": 12,
    "Porto": 18,
    "Santarém": 20,
    "Setúbal": 17,
    "Viana do Castelo": 22,
    "Vila Real": 21,
    "Viseu": 16
}


@app.command()
def top(n: int, export_csv: bool = False):
    """Lista os N trabalhos mais recentes publicados."""

    if n <= 0:
        typer.echo("Erro: O número de trabalhos deve ser um valor inteiro positivo.")
        return
    if n > 100:
        typer.echo("Erro: O número máximo de trabalhos deve ser no máximo 100.")
        return

    try:
        typer.echo(f"\Os {n} trabalhos mais recentes:\n")

        headers = {
            "User-Agent": "",
        }

        response = requests.get(BASE_URL, params={"limit": n, "api_key": API_KEY}, headers=headers)
        response.raise_for_status()

        data = response.json()
        jobs = data.get("results", [])

        if not jobs:
            typer.echo("Nenhum trabalho encontrado!")
            return

        # Exportar para CSV, se solicitado
        if export_csv:
            export_to_csv(jobs, "top_jobs.csv")

        for i, job in enumerate(jobs, 1):
            company = job.get("company", {})
            title = job.get("title", "Sem título")
            location = ", ".join([loc["name"] for loc in job.get("locations", [])]) or "Local não especificado"
            description = job.get("body", "").strip()
            company_name = company.get("name", "Empresa não informada")
            company_url = company.get("url", "")

            # Remover tags HTML e limitar a descrição
            clean_description = re.sub(r"<.*?>", "", description)
            limited_description = (clean_description[:300] + '...') if len(clean_description) > 300 else clean_description

            # Exibir as informações formatadas
            typer.echo(f"{'=' * 60}")
            typer.echo(f"Vaga {i}: {title}")
            typer.echo(f"Empresa: {company_name}")
            if company_url:
                typer.echo(f"Website: {company_url}")
            typer.echo(f"Localização: {location}")
            typer.echo(f"Descrição: {limited_description}")
            typer.echo(f"{'-' * 60}\n")

    except requests.RequestException as e:
        typer.echo(f"Erro ao acessar a API: {e}")
    except Exception as e:
        typer.echo(f"Erro geral: {e}")

@app.command()
def search(localidade: str, empresa: str, n: int, export_csv: bool = False):
    """Lista de trabalhos full-time de uma empresa numa localidade específica e exporta para CSV opcionalmente."""
    
    if n <= 0:
        typer.echo("Erro: O número de trabalhos deve ser um valor inteiro positivo.")
        return
    if n > 100:
        typer.echo("Erro: O número máximo de trabalhos deve ser no máximo 100.")
        return

    # Verifica se a cidade fornecida existe no dicionário
    localidade_id = CIDADES.get(localidade)
    if not localidade_id:
        typer.echo(f"Erro: A cidade '{localidade}' não foi encontrada. Tente uma das seguintes cidades: {', '.join(CIDADES.keys())}.")
        return

    try:
        # Faz a requisição para a API
        headers = {"User-Agent": ""}
        response = requests.get(BASE_URL2, params={
            "limit": n,
            "locality": localidade_id,  # Usando ID da cidade aqui
            "company": empresa,
            "fulltime": "true",  # Garantir que só sejam retornadas vagas full-time
            "api_key": API_KEY
        }, headers=headers)

        # Verifica se a requisição foi bem-sucedida
        response.raise_for_status()
        jobs = response.json().get("results", [])

        # Verifica se existem vagas
        if not jobs:
            typer.echo("Nenhum trabalho encontrado para os critérios fornecidos.")
            return

        # Limita o número de resultados, se necessário
        jobs_limited = jobs[:n]

        # Exibe os resultados no terminal
        for job in jobs_limited:
            title = job.get("title", "Sem título")
            company = job.get("company", {}).get("name", "Sem empresa")
            location = ", ".join([loc['name'] for loc in job.get('locations', [])])
            published_at = job.get("publishedAt", "Data não disponível")
            job_url = f"https://www.itjobs.pt/oferta/{job.get('id', '')}"

            print(f"\nTítulo: {title}")
            print(f"Empresa: {company}")
            print(f"Localização: {location}")
            print(f"Data de Publicação: {published_at}")
            print(f"Link: {job_url}")
            print("-" * 50)  # Separador

        # Exporta para CSV se solicitado
        if export_csv:
            export_to_csv(jobs_limited, "search_jobs.csv")
            typer.echo(f"Dados exportados para 'search_jobs.csv'.")

    except requests.RequestException as e:
        typer.echo(f"Erro ao acessar a API: {e}")


@app.command()
def salary(job_id: int, export_csv: bool = False):
    """
    Extrai o salário oferecido para um determinado job id.
    """
    try:
        typer.echo(f"A procurar as informações de salário para o job id: {job_id}...")

        headers = {
            "User-Agent": "jobs-cli"  
        }

        # Faz a requisição para a API
        response = requests.get(
            BASE_URL2.format(job_id=job_id),
            headers=headers,
            params={"api_key": API_KEY}
        )

        # Verifica se a requisição foi bem-sucedida
        response.raise_for_status()
        data = response.json()

        job = data.get("results", [])[0]

        wage = job.get("wage")
        body = job.get("body", "")

        salary_data = {
            "salary": wage if wage else "Não especificado"
        }

        # Expressão regular para buscar possíveis menções a salários no corpo da descrição
        salary_matches = re.findall(
            r'(\d{1,3}(?:\.\d{3})*,?\d{0,2}\s*(?:EUR|€|euro|euros|k))', body, re.IGNORECASE
        )

        if salary_matches:
            salary_data["salary_matches"] = ", ".join(salary_matches)

        if export_csv:
            export_to_csv([salary_data], "salary_jobs.csv")

        typer.echo(json.dumps(salary_data, indent=2, ensure_ascii=False))

    except requests.RequestException as e:
        typer.echo(f"Erro ao acessar a API: {e}")
    except Exception as e:
        typer.echo(f"Erro inesperado: {e}")

@app.command()
def skills(skills: str, data_inicial: str, data_final: str, export_csv: bool = False):
    """
    Mostra quais os trabalhos que requerem uma determinada lista de skills em um período de tempo.
    Recebe uma lista de skills e um intervalo de datas (data_inicial e data_final).
    """
    try:
        # Remover os colchetes e dividir a string para criar uma lista de skills
        skills = skills.strip("[]").split(",")
        skills_list = [skill.strip().lower() for skill in skills]  # Remover espaços extras das skills e garantir que tudo seja minúsculo

        # Validar se a skills_list é uma lista não vazia
        if not skills_list or not isinstance(skills_list, list):
            print("Erro: A lista de skills deve ser uma lista válida.")
            return

        # Convertendo as datas para o formato datetime
        start_date = datetime.datetime.strptime(data_inicial, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(data_final, "%Y-%m-%d")

        # Validar as datas
        if start_date > end_date:
            print("Erro: A data inicial não pode ser posterior à data final.")
            return

        headers = {"User-Agent": "jobs-cli"}
        response = requests.get(BASE_URL, params={"api_key": API_KEY}, headers=headers)

        response.raise_for_status()
        jobs = response.json().get("results", [])

        # Filtrar os trabalhos que têm as skills e estão dentro do período de tempo
        filtered_jobs = []
        for job in jobs:
            job_date_str = job.get("publishedAt", "").split(" ")[0]  # Pegar a data sem hora
            if job_date_str:
                try:
                    job_date = datetime.datetime.strptime(job_date_str, "%Y-%m-%d")
                except ValueError:
                    continue  # Caso a data esteja no formato errado, ignore o trabalho
            else:
                continue  # Caso não tenha data, ignore o trabalho

            # Procurar por skills no corpo da descrição do trabalho
            job_body = job.get("body", "").lower()  # Garantir que o texto do corpo esteja em minúsculas

            # Verificar se todas as skills estão presentes no corpo da descrição
            if all(skill in job_body for skill in skills_list) and start_date <= job_date <= end_date:
                filtered_jobs.append(job)

        # Exibir os resultados em formato JSON
        if not filtered_jobs:
            print("Nenhum trabalho encontrado para as skills e período especificados.")
            return

        if export_csv:
            export_to_csv(filtered_jobs, "filtered_jobs.csv")

        # Exibir os resultados em formato mais legível
        for job in filtered_jobs:
            title = job.get('title', 'N/A')
            company = job.get('company', {}).get('name', 'N/A')
            description = job.get('body', 'N/A')
            publication_date = job.get('publishedAt', 'N/A').split(' ')[0]
            salary = job.get('wage', 'N/A')
            location = ', '.join(location['name'] for location in job.get('locations', []))

            print(f"Título: {title}")
            print(f"Empresa: {company}")
            print(f"Descrição: {description}")
            print(f"Data de Publicação: {publication_date}")
            print(f"Salário: {salary}")
            print(f"Localização: {location}")
            print("-" * 50)

    except requests.RequestException as e:
        print(f"Erro ao acessar a API: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

def export_to_csv(jobs, filename):
    """Exporta a lista de jobs para um arquivo CSV."""
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        # Adicionar cabeçalho baseado nos campos do job
        writer.writerow(["titulo", "empresa", "descrição", "data de publicação", "skills"])

        for job in jobs:
            skills = [skill["name"] for skill in job.get("skills", [])]
            writer.writerow([
                job.get("title", "N/A"),
                job.get("company", {}).get("name", "N/A"),
                job.get("body", "N/A"),
                job.get("date", "N/A"),
                ", ".join(skills)
            ])
        typer.echo(f"Dados exportados para {filename}")

def export_to_csv(jobs, filename):
    """Exporta a lista de jobs para um arquivo CSV."""
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        # Adicionar cabeçalho baseado nos campos do job
        if filename == "salary_jobs.csv":
            writer.writerow(["job_id", "title", "company", "location", "description", "salary", "salary_matches"])
        else:
            writer.writerow(["titulo", "empresa", "descrição", "data de publicação", "salário", "localização"])

        for job in jobs:
            writer.writerow([
                job.get("job_id", "N/A"),
                job.get("title", "N/A"),
                job.get("company", "N/A"),
                job.get("location", "N/A"),
                job.get("description", "N/A"),
                job.get("salary", "N/A"),
                job.get("salary_matches", "N/A")  # Para salary_jobs.csv
            ])
        typer.echo(f"Dados exportados para {filename}")

if __name__ == "__main__":
    app()
