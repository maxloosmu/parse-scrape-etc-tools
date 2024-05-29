import asyncio
import csv
from pyppeteer import launch
from pyppeteer.errors import TimeoutError, ElementHandleError

async def fetch_stock_data(page, stock_id, stock_name):
    # Scroll within the sgx-table-list to load all rows
    await auto_scroll_within_table(page)

    try:
        # Wait for the specific sgx-table-row to load
        await page.waitForSelector(f'sgx-table-row[data-row-id="{stock_id}"]', timeout=10000)

        # Extract the row data for the stock_id
        stock_data = await page.evaluate(f'''(stock_id, stock_name) => {{
            const elements = Array.from(document.querySelectorAll('sgx-table-row'));
            let data = [];
            elements.forEach(element => {{
                if (element.getAttribute('data-row-id') === stock_id) {{
                    const cells = {{}};
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
                    data.push(cells);
                }}
            }});
            return data;
        }}''', stock_id, stock_name)

        print(f"{stock_name} Data:", stock_data)

    except TimeoutError:
        print(f"TimeoutError: Could not find the selector for stock '{stock_name}' with ID '{stock_id}' within the timeout period.")
    except ElementHandleError as e:
        print(f"ElementHandleError: {e}")

async def auto_scroll_within_table(page):
    await page.evaluate('''async () => {
        const table = document.querySelector('sgx-table-list');
        if (!table) {
            throw new Error("sgx-table-list element not found");
        }
        const distance = 100; // distance to scroll
        let totalHeight = 0;

        while (totalHeight < table.scrollHeight) {
            table.scrollBy(0, distance);
            totalHeight += distance;
            await new Promise(resolve => setTimeout(resolve, 100)); // small delay to allow loading
        }
    }''')

async def main():
    browser = await launch(headless=True)
    page = await browser.newPage()
    await page.goto('https://www.sgx.com/securities/securities-prices?code=stocks')

    with open('stocks.csv', 'r') as file:
        reader = csv.DictReader(file)
        stock_data = [row for row in reader]

    for stock in stock_data:
        stock_id = stock['ID']
        stock_name = stock['NAME']
        await fetch_stock_data(page, stock_id, stock_name)

    await browser.close()

asyncio.get_event_loop().run_until_complete(main())
