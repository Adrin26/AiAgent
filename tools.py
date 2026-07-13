import os
import requests
from typing import Dict, Any
from dotenv import load_dotenv
from langchain.tools import tool
from tavily import TavilyClient

load_dotenv()
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


@tool("calculator", description="Performs mathematical calculations.")
def tool1(expression: str) -> str:
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"


@tool("web_search", description="Search the web for information")
def tool2(query: str) -> Dict[str, Any]:
    return tavily_client.search(query)


@tool(
    "exchage_converter",
    description="Get exchange rate between currencies. Use 'latest' or date like '2024-01-15'.",
)
def tool3(currency_from: str, currency_to: str, date: str = "latest") -> str:
    try:
        if date == "latest":
            url = f"https://api.frankfurter.dev/v2/latest?base={currency_from}&symbols={currency_to}"
        else:
            url = f"https://api.frankfurter.dev/v2/{date}?base={currency_from}&symbols={currency_to}"

        response = requests.get(url, timeout=10)
        data = response.json()
        rate = data["rates"][currency_to.upper()]
        return f"{currency_from.upper()} to {currency_to.upper()} on {data.get('date', date)}: {rate}"
    except Exception:
        return f"Could not get rate for {currency_from} to {currency_to} on {date}"
