from .hatchet import hatchet
from hatchet_sdk import Context
import requests
from bs4 import BeautifulSoup

"""
Setup the workflow
This is the main workflow that will trigger both the TechCrunch and Google News scraping workflows.
It streams the progress and results to the client.
"""
@hatchet.workflow(on_events=["scraper:start"])
class ScraperWorkflow:

    @hatchet.step()
    async def start(self, context: Context):
        # Start the TechCrunch scraping workflow
        techcrunchHomePageResult = await (
                await context.aio.spawn_workflow(
                    "TechCrunchAIScraperWorkflow", {}
                )
            ).result()
        print("techcrunchHomePageResult", techcrunchHomePageResult)

        # Start the Google News scraping workflow
        googleNewsHomePageResult = await (
                await context.aio.spawn_workflow(
                    "GoogleNewsScraperWorkflow", {}
                )
            ).result()
        print("googleNewsHomePageResult", googleNewsHomePageResult)

        # Return the results of both workflows
        return {
            "techCrunchArticles": techcrunchHomePageResult,
            "googleNewsArticles": googleNewsHomePageResult
        }
    
    
@hatchet.workflow(on_events=["scraper:techcrunch_ai_homepage"])
class TechCrunchAIScraperWorkflow:

    @hatchet.step()
    async def fetch_homepage(self, context: Context):
        print("Fetching TechCrunch AI homepage articles")
        url = "https://techcrunch.com/category/artificial-intelligence/"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            articles_data = []
            for article in soup.find_all('div', class_='wp-block-tc23-post-picker'):
                title_element = article.find('h2', class_='wp-block-post-title')
                author_element = article.find('div', class_='wp-block-tc23-author-card-name')
                link_element = title_element.find('a', href=True) if title_element else None
                excerpt_element = article.find('div', class_='wp-block-post-excerpt__excerpt')
                time_element = article.find('time')
                image_element = article.find('img', src=True)

                if title_element and author_element and link_element:
                    articles_data.append({
                        "title": title_element.get_text(strip=True),
                        "author": author_element.get_text(strip=True),
                        "link": link_element['href'],
                        "excerpt": excerpt_element.get_text(strip=True) if excerpt_element else "",
                        "published_time": time_element.get_text(strip=True) if time_element else "",
                        "image_url": image_element['src'] if image_element else ""
                    })

            return {"articles_data": articles_data}
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching TechCrunch AI homepage: {e}")
            return {
                "status": "error",
                "message": str(e),
                "articles_data": []
            }

    @hatchet.step(parents=["fetch_homepage"])
    async def parse_articles(self, context: Context):

        articles_data = context.step_output("fetch_homepage")['articles_data']
        
        if not articles_data:
            return {
                "status": "error",
                "message": "No articles data found"
            }

        articles = []

        for article in articles_data:
            if article['title'] and article['author'] and article['link']:
                articles.append({
                    "title": article['title'],
                    "author": article['author'],
                    "link": article['link'],
                    "excerpt": article['excerpt'] or "",
                    "published_time": article['published_time'] or "",
                    "image_url": article['image_url'] or "",
                })
        
        return {
            "status": "success",
            "articles": articles
        }
        
        
@hatchet.workflow(on_events=["scraper:google_news_homepage"])
class GoogleNewsScraperWorkflow:

    @hatchet.step()
    async def fetch_homepage(self, context: Context):
        print("Fetching Google News homepage articles")
        url = "https://news.google.com/topstories"

        try:
            response = requests.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            articles_data = []
            print('Soup all articles', soup.find_all('article'))
            for article in soup.find_all('article'):
                title_element = article.find('h3')
                link_element = article.find('a', href=True)
                time_element = article.find('time')
                source_element = article.find('a', class_='wEwyrc')
                image_element = article.find('img', src=True)

                title_text = title_element.get_text(strip=True) if title_element else "No Title"
                link_href = link_element['href'] if link_element else "#"
                time_text = time_element.get_text(strip=True) if time_element else "Unknown Time"
                source_text = source_element.get_text(strip=True) if source_element else "Unknown Source"
                image_src = image_element['src'] if image_element else ""

                if link_href != "#":
                    articles_data.append({
                        "title": title_text,
                        "author": source_text,
                        "link": link_href,
                        "excerpt": "",
                        "published_time": time_text,
                        "image_url": image_src
                    })

            return {"articles_data": articles_data}
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching Google News homepage: {e}")
            return {
                "status": "error",
                "message": str(e),
                "articles_data": []
            }

    @hatchet.step(parents=["fetch_homepage"])
    async def parse_articles(self, context: Context):

        articles_data = context.step_output("fetch_homepage")['articles_data']
        
        if not articles_data:
            return {
                "status": "error",
                "message": "No articles data found"
            }

        articles = []

        for article in articles_data:
            if article['title'] and article['author'] and article['link']:
                articles.append({
                    "title": article['title'],
                    "author": article['author'],
                    "link": article['link'],
                    "excerpt": article['excerpt'] or "",
                    "published_time": article['published_time'] or "",
                    "image_url": article['image_url'] or "",
                    "status": "queued"
                })
        
        return {
            "status": "success",
            "articles": articles
        }
        
# The above code defines a Python class `GoogleNewsScraperWorkflow` that is part of a Hatchet
# workflow. The workflow has two asynchronous methods: `fetch_homepage` and `parse_articles`.
@hatchet.workflow(on_events=["scraper:google_news_homepage"])
class GoogleNewsScraperWorkflow:

    @hatchet.step()
    async def fetch_homepage(self, context: Context):
        print("Fetching Google News homepage articles")
        url = "https://news.google.com/topstories"

        try:
            response = requests.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            articles_data = []
            for article in soup.find_all('article'):
                # Attempt to find the link element
                link_element = article.find('a', href=True)
                link_href = link_element['href'] if link_element else "#"

                # Attempt to find the title element
                title_element = article.find('a', class_='gPFEn')
                title_text = title_element.get_text(strip=True) if title_element else "No Title"

                # Attempt to find the source (author)
                source_element = article.find('div', class_='vr1PYe')
                source_text = source_element.get_text(strip=True) if source_element else "Unknown Source"

                # Attempt to find the published time
                time_element = article.find('time')
                time_text = time_element.get_text(strip=True) if time_element else "Unknown Time"

                # Attempt to find the image element
                image_element = article.find('img', class_='Quavad', src=True)
                image_src = image_element['src'] if image_element else ""

                # Construct the article data dictionary
                if link_href != "#":
                    articles_data.append({
                        "title": title_text,
                        "author": source_text,
                        "link": link_href,
                        "published_time": time_text,
                        "image_url": image_src
                    })

            return {"articles_data": articles_data}

        except requests.exceptions.RequestException as e:
            print(f"Error fetching Google News homepage: {e}")
            return {
                "status": "error",
                "message": str(e),
                "articles_data": []
            }

    @hatchet.step(parents=["fetch_homepage"])
    async def parse_articles(self, context: Context):

        articles_data = context.step_output("fetch_homepage")['articles_data']

        if not articles_data:
            return {
                "status": "error",
                "message": "No articles data found"
            }

        articles = []

        for article in articles_data:
            if article['title'] and article['author'] and article['link']:
                articles.append({
                    "title": article['title'],
                    "author": article['author'],
                    "link": f"https://news.google.com{article['link'][1:]}",
                    "published_time": article['published_time'] or "",
                    "image_url": article['image_url'] or "",
                })

        return {
            "status": "success",
            "articles": articles
        }
