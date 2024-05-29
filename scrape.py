import asyncio
import csv
from pyppeteer import launch
from pyppeteer.errors import TimeoutError
from dotenv import load_dotenv
import os

load_dotenv()
user_agent = os.getenv('USER_AGENT')
page_url = os.getenv('PAGE_URL')

async def fetch_stock_data(stock_id, stock_name):
    browser = await launch(headless=True)
    page = await browser.newPage()
    await page.goto(page_url)
    await page.setUserAgent(user_agent)

    try:
        # Wait for the search input to be available and clear it
        await page.waitForSelector('input[name="search"]', timeout=10000)
        await page.evaluate('''document.querySelector('input[name="search"]').value = '';''')

        # Input the stock_id into the search field
        await page.type('input[name="search"]', stock_id)
        await asyncio.sleep(2)  # Wait for 2 seconds to allow search results to load

        # Wait for the specific sgx-table-row to load
        await page.waitForSelector(f'sgx-table-row[data-row-id="{stock_id}"]', timeout=10000)

        # Extract the row data for the stock_id
        stock_data = await page.evaluate('''
            (stock_id, stock_name) => {
                const element = document.querySelector(`sgx-table-row[data-row-id="${stock_id}"]`);
                if (element) {
                    const cells = {};
                    cells['name'] = stock_name;
                    cells['nc'] = element.querySelector('sgx-table-cell-text[data-column-id="nc"]').innerText.trim();
                    cells['lt'] = element.querySelector('sgx-table-cell-number[data-column-id="lt"]').innerText.trim();
                    cells['c'] = element.querySelector('sgx-table-cell-number[data-column-id="c"]').innerText.trim();
                    cells['p'] = element.querySelector('sgx-table-cell-number[data-column-id="p"]').innerText.trim();
                    cells['vl'] = element.querySelector('sgx-table-cell-number[data-column-id="vl"]').innerText.trim();
                    cells['v'] = element.querySelector('sgx-table-cell-number[data-column-id="v"]').innerText.trim();
                    cells['bv'] = element.querySelector('sgx-table-cell-number[data-column-id="bv"]').innerText.trim();
                    cells['b'] = element.querySelector('sgx-table-cell-number[data-column-id="b"]').innerText.trim();
                    cells['s'] = element.querySelector('sgx-table-cell-number[data-column-id="s"]').innerText.trim();
                    cells['sv'] = element.querySelector('sgx-table-cell-number[data-column-id="sv"]').innerText.trim();
                    cells['o'] = element.querySelector('sgx-table-cell-number[data-column-id="o"]').innerText.trim();
                    cells['h'] = element.querySelector('sgx-table-cell-number[data-column-id="h"]').innerText.trim();
                    cells['l'] = element.querySelector('sgx-table-cell-number[data-column-id="l"]').innerText.trim();
                    return [cells];
                }
                return [];
            }
        ''', stock_id, stock_name)

        print(f"{stock_name} Data:", stock_data)

    except TimeoutError:
        print(f"TimeoutError: Could not find the selector for stock '{stock_name}' with ID '{stock_id}' within the timeout period.")

    await browser.close()

async def main():
    with open('stocks.csv', 'r') as file:
        reader = csv.DictReader(file)
        stock_data = [row for row in reader]

    for stock in stock_data:
        stock_id = stock['ID']
        stock_name = stock['NAME']
        await fetch_stock_data(stock_id, stock_name)

asyncio.get_event_loop().run_until_complete(main())
