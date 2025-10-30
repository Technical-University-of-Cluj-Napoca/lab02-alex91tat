import sys
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://juniors.ro/jobs"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

CITY_IDS = {
    "Bucuresti": "2715",
    "Cluj-Napoca": "5587",
    "Timisoara": "5752",
    "Iasi": "8115",
    "Sibiu": "13751",
}

EXPERIENCE_MAP = {
    "1": "100",  # fara experienta
    "2": "200",  # 0 - 1 an
    "3": "300",  # > 1 an
}


def get_search_filters() -> dict:
    print("Find Jobs on juniors.ro: ")
    programming_language = input("Enter the programming language (press Enter to skip): ")
    print("\nAvailable cities:")
    for city in CITY_IDS.keys():
        print(f"  - {city}")
    city = input("\nEnter the city name (press Enter to skip): ")
    
    print("Select Experience Level:")
    print("  1: Fără experiență")
    print("  2: 0 - 1 an")
    print("  3: > 1 an")
    experience_level = input("Enter choice (1, 2, 3, or Enter to skip): ")

    query_parts = []
    if programming_language:
        query_parts.append(programming_language.strip())
    
    final_query = " ".join(query_parts)

    experience_id = EXPERIENCE_MAP.get(experience_level, None)
    city_id = CITY_IDS.get(city.strip(), None)
    
    if not final_query and not experience_level and not city_id:
        print("\nError: At least one filter (programming language, experience, or city) must be provided.", file=sys.stderr)
        sys.exit(1)

    filters = {
        "q": final_query if final_query else None,
        "experienta": experience_id,
        "city_id": city_id
    }

    return filters

def fetch_page_content(filters: dict) -> str:

    request_url = BASE_URL
    params = {}

    if filters.get("experienta"):
        request_url = f"{BASE_URL}/experienta:{filters['experienta']}"

    if filters.get("q"):
        params["q"] = filters["q"]
    if filters.get("city_id"):
        params["city_id"] = filters["city_id"]

    search_desc_parts = []
    if params.get("q"):
        search_desc_parts.append(f"q='{params['q']}'")
    if filters.get("experienta"):
        search_desc_parts.append(f"experienta='{filters['experienta']}'")
    if filters.get("city_id"):
        search_desc_parts.append(f"city_id='{filters['city_id']}'")

    search_desc = " and ".join(search_desc_parts)
    if not search_desc:
        search_desc = "all jobs"

    try:
        response = requests.get(request_url, headers=HEADERS, params=params)
        response.raise_for_status()
        return response.text
    
    except requests.exceptions.RequestException as e:
        print(f"Error: Could not fetch page. {e}", file=sys.stderr)
        sys.exit(1)

def parse_jobs(html_content: str) -> list:
    soup = BeautifulSoup(html_content, 'html.parser')

    job_cards = soup.find_all("li", class_="job") 
    
    if not job_cards:
        print("No jobs found for these filters.")
        return []
    
    return job_cards[:7]


def extract_jobs_details(job_cards: list) -> list[dict[str, str]]:
    extracted_jobs = []
    
    for card in job_cards:
        title_element = card.select_one("div.job_header_title h3")
        title = title_element.text.strip() if title_element else "N/A"

        loc_date_element = card.select_one("div.job_header_title strong")
        location = ""
        date = ""
        if loc_date_element:
            text = ' '.join(loc_date_element.text.split())
            parts = text.split('|') 
            if len(parts) == 2:
                location = parts[0].strip()
                date = parts[1].strip()
            else:
                location = text.strip()

        tech_elements = card.select("ul.job_tags li")
        technologies = [el.text.strip() for el in tech_elements]
        tech_string = " ".join(technologies) if technologies else ""

        company_name = "N/A"
        
        requirements_lis = card.select("ul.job_requirements li")
        for li in requirements_lis:
            strong_tag = li.find("strong") 
            if strong_tag and strong_tag.text.strip() == "Companie:":
                company_name = li.text.replace("Companie:", "").strip()
                break 

        link_element = card.select_one('div.job_header_buttons a[target="_blank"]')
        link = link_element['href'] if link_element and link_element.get('href') else "N/A"

        extracted_jobs.append({
            "title": title,
            "company": company_name,
            "location": location,
            "date": date,
            "technologies": tech_string,
            "link": link
        })
        
    return extracted_jobs

def display_jobs(jobs: list[dict[str, str]]) -> None:
    if not jobs:
        print("No job details to display.")
        return
    
    print("\nFound jobs:")

    for i, job in enumerate(jobs, start=1):

        title = job.get('title', 'N/A')
        company = job.get('company', 'N/A')
        location = job.get('location', 'N/A')
        date = job.get('date', 'N/A')
        technologies = job.get('technologies', 'N/A')
        link = job.get('link', 'N/A')

        print(f"Job {i}:")
        print(f"  Job Title: {title}")
        print(f"  Company: {company}")
        print(f"  Location: {location}")
        print(f"  Date Posted: {date}")
        print(f"  Technologies: {technologies}")
        print(f"  Link: {link}\n")


def main() -> None:
    filters = get_search_filters()
    html = fetch_page_content(filters)
    job_cards = parse_jobs(html)
    job_list = extract_jobs_details(job_cards)
    display_jobs(job_list)

if __name__ == "__main__":
    main()