import json
# import asyncio
import random
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from mainapp.models import *
from django.db import transaction
# from asgiref.sync import sync_to_async
import time

def random_sleep(min_sec=2, max_sec=5):
    time.sleep(random.uniform(min_sec, max_sec))

def create_browser_context(playwright):
    browser = playwright.chromium.launch(headless=True, args=[
        "--disable-blink-features=AutomationControlled",
        "--no-sandbox",
    ])
    context = browser.new_context(
        viewport={"width": 1366, "height": 768},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        locale='en-US',
        timezone_id="America/New_York",
    )
    return browser, context

def extract_paa_questions(page, parent_kw, max_questions):
    questions_data = []
    try:
        page.wait_for_selector('div[jsname="yEVEwb"]', timeout=7000)
    except PlaywrightTimeoutError:
        return []

    boxes = page.query_selector_all('div[jsname="yEVEwb"]')
    boxes = boxes[:max_questions]

    # Expand answers by clicking on each box
    for box in boxes:
        try:
            box.click()
            random_sleep(0.8, 1.5)
        except Exception:
            continue

    # Re-fetch boxes after expansion
    boxes = (page.query_selector_all('div[jsname="yEVEwb"]'))[:max_questions]

    for box in boxes:
        try:
            question_el = box.query_selector('div.related-question-pair')
            answer_el = box.query_selector('div[data-attrid], span.hgKElc')
            link_el = box.query_selector('a')
            title_el = link_el.query_selector('h3')

            question = question_el.get_attribute("data-q") if question_el else None
            answer = (answer_el.inner_text()).strip() if answer_el else None
            title = (title_el.inner_text()).strip() if title_el else None
            
            href = link_el.get_attribute("href")
            if href and href.startswith("/url"):
                link = f"https://www.google.com{href}"
            else:
                link = href

            if question and answer:
                questions_data.append({
                    "link": link,
                    "title": title,
                    "parent_kw": parent_kw,
                    "question": question.strip(),
                    "answer": answer,
                })
        except Exception:
            continue

    return questions_data

def scrape_single_query(context, query, max_questions):
    page = context.new_page()
    try:
        print(f"Scraping: {query}")
        search_url = f"https://www.google.com/search?q={query}"
        page.goto(search_url, wait_until="domcontentloaded", timeout=15000)

        # Detect CAPTCHA
        if "sorry/index" in page.url or "captcha" in page.url.lower():
            print(f"CAPTCHA detected for query: {query}")
            return []

        random_sleep(3, 6)
        questions = extract_paa_questions(page, parent_kw=query, max_questions=max_questions)
        return questions
    except PlaywrightTimeoutError:
        print(f"Timeout loading page for query: {query}")
        return []
    finally:
        page.close()

def scrape_single_query_with_retry(context, query, max_questions, retries=2):
    for attempt in range(retries):
        try:
            return scrape_single_query(context, query, max_questions)
        except PlaywrightTimeoutError:
            print(f"Timeout loading page for query: {query}, attempt {attempt+1}")
            time.sleep(3 * (attempt+1))
    return []

def scrape_main_keyword(context, main_kw, max_depth, max_questions):
    results = []
    visited = set()
    current_level_queries = [main_kw]

    for depth in range(1, max_depth + 1):
        print(f"Scraping depth {depth}...")
        next_level_queries = []
        for q in current_level_queries:
            questions = scrape_single_query_with_retry(context, q, max_questions)
            print(f"Found {len(questions)} questions.")

            results.extend(questions)
            for item in questions:
                next_q = item.get("question")
                if next_q and next_q not in visited:
                    visited.add(next_q)
                    next_level_queries.append(next_q)
        if not next_level_queries:
            print("No more new questions found, stopping recursion.")
            break
        current_level_queries = next_level_queries

    return results

def save_results_to_db(main_kw, results):
    with transaction.atomic():
        main_kw_obj = MainKW.objects.create(name=main_kw)
        items = [
            GPaaResult(
                main_kw=main_kw_obj,
                parent_kw=item["parent_kw"],
                question=item["question"],
                answer=item["answer"],
                link=item["link"],
                title=item["title"]
            )
            for item in results
        ]
        GPaaResult.objects.bulk_create(items)
    return main_kw_obj

def scrape_google_paa(main_kw):
    start_time = time.time()
    max_depth = 3
    max_questions = 4

    with sync_playwright() as playwright:
        browser, context = create_browser_context(playwright)
        results = scrape_main_keyword(context, main_kw, max_depth=max_depth, max_questions=max_questions)
        print(f"Scraping complete. Total questions scraped: {len(results)}")

        # with open("google_paa_results.json", "w", encoding="utf-8") as f:
        #     json.dump(results, f, ensure_ascii=False, indent=2)

        # print("Saved results into json file.")
        main_kw_obj = save_results_to_db(main_kw, results)
        print("Saved results to DB.")
        context.close()
        browser.close()

    end_time = time.time()
    print(f"Total time taken: {end_time - start_time:.2f} seconds")
    return main_kw_obj

# scrape_google_paa("affordable web hosting")
# main_kw_obj = asyncio.run(scrape_google_paa("affordable web hosting"))