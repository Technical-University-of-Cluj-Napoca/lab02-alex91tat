import sys
import requests
from bs4 import BeautifulSoup

def get_definition(word):
    url = f"https://dexonline.ro/definitie/{word}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  
        soup = BeautifulSoup(response.text, 'html.parser')

        not_found_tag = soup.find('h1', string=lambda text: text and 'nu este în dicționar' in text)
        if not_found_tag:
            return "error word not found"

        first_meaning_container = soup.find('div', class_='meaningContainer')
        
        if first_meaning_container:
            definition_span = first_meaning_container.find('span', class_='tree-def html')
            
            if definition_span:
                definition_text = definition_span.get_text(strip=True)
                return definition_text
        
        return "error couldn't parse the definition."
    except requests.exceptions.HTTPError as http_err:
        if http_err.response.status_code == 404:
            return "error word not found"
        else:
            return f"HTTP error occurred: {http_err}"
    except requests.exceptions.RequestException as req_err:
        return f"an error occurred during the request: {req_err}"
    except Exception as e:
        return f"unexpected error occurred: {e}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1) 

    word_to_define = sys.argv[1]
    
    definition = get_definition(word_to_define)
    print(definition)