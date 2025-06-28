import azure.functions as func
import logging
import requests
from bs4 import BeautifulSoup
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="CrawlerToJson")
def CrawlerToJson(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    try:
        url = "https://quotes.toscrape.com/"
        res = requests.get(url)
        res.raise_for_status()

        soup = BeautifulSoup(res.text, "html.parser")
        quotes = soup.select(".quote")
        results = []

        for quote in quotes:
            text = quote.select_one(".text").get_text()
            author = quote.select_one(".author").get_text()
            tags = [tag.get_text() for tag in quote.select(".tags .tag")]
            results.append({
                "text": text,
                "author": author,
                "tags": tags
            })

        json_str = json.dumps(results, ensure_ascii=False, indent=2)
        return func.HttpResponse(json_str, mimetype="application/json")

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return func.HttpResponse(
            f"Internal Server Error: {str(e)}",
            status_code=500
        )