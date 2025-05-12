import requests
from datetime import datetime

JIRA_URL = "https://jira-adiq.atlassian.net/rest/api/3/search"
API_TOKEN = "ATATT3xFfGF0v7cQA-g0xR9F8hBb3L5RL6BGZYQDzSFb_-FhgToJGqDqZtcGNiFviItKTZsA-kW1RshsAu7KAzMu_QvlOyxkIpc68_B2-t7koan-fivMzUm4C5WRIsKrT8cEspxVMuT7VucAhoRiBUtASOZVozgN630sZ1HreMLklcWGPC8t6_M=558D0F90"
EMAIL = "caique.pereira@adiq.com.br"

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

today = datetime.now().strftime("%Y-%m-%d")
# Substitua 12345 pelo ID correto após verificar com a API /field
jql = f'project = SDM AND issuetype = "Solicitação de Mudança" AND cf[12345] = "{today}"'
params = {
    "jql": jql,
    "maxResults": 50,
    "fields": "key,summary,customfield_12345"
}

try:
    response = requests.get(
        JIRA_URL,
        headers=headers,
        params=params,
        auth=(EMAIL, API_TOKEN)
    )
    
    response.raise_for_status()
    data = response.json()
    issues = data.get("issues", [])
    
    if issues:
        print("Chamados com mudanças planejadas para hoje (13 de abril de 2025):")
        for issue in issues:
            print(f"- {issue['key']}: {issue['fields']['summary']}")
            if issue['fields'].get('customfield_12345'):
                print(f"  Detalhes da mudança: {issue['fields']['customfield_12345']}")
    else:
        print("Nenhum chamado com mudança planejada encontrada para hoje.")
        
except requests.exceptions.HTTPError as e:
    print(f"Erro HTTP: {e}")
    if e.response.status_code == 400:
        print("Erro 400: Verifique a query JQL (projeto, tipo de issue ou campo personalizado).")
        print(f"Query enviada: {jql}")
        print("Sugestões:")
        print("- Confirme se o projeto 'SDM' existe.")
        print("- Verifique o nome exato do tipo de issue 'Solicitação de Mudança'.")
        print("- Valide o ID do campo personalizado 'cf[12345]' com a API /field.")
    elif e.response.status_code == 401:
        print("Erro 401: Credenciais inválidas. Verifique EMAIL e API_TOKEN.")
    elif e.response.status_code == 403:
        print("Erro 403: Usuário sem permissão para acessar o projeto ou campo.")
    else:
        print(f"Resposta do servidor: {e.response.text}")
except requests.exceptions.RequestException as e:
    print(f"Erro na requisição: {e}")
except ValueError as e:
    print(f"Erro ao processar JSON: {e}")