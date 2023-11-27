import aiohttp
import json
import asyncio

async def retrieve_charity_data(query, limit=5):
    url = f'https://data.gov.au/data/api/3/action/datastore_search?resource_id=bbb19fa5-2f63-49cb-96b2-523e25828f27&limit={limit}&q={query}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.text()
                json_data = json.loads(data)
                if json_data.get('success'):
                    return json_data['result']['records']
            return None

def format_charity_info(data):
    if not data:
        return "No information available."

    info = data[0]  # Assuming you're interested in the first record
    formatted_info = (
        f"Charity Name: {info.get('charity name', 'N/A')}\n"
        f"Registration Status: {info.get('registration status', 'N/A')}\n"
        f"Website: {info.get('charity website', 'N/A')}\n"
        f"Size: {info.get('charity size', 'N/A')}\n"
        f"Activities Conducted: {'Yes' if info.get('conducted activities') == 'y' else 'No'}\n"
        f"Staff: Full Time - {info.get('staff - full time', '0')}, Volunteers - {info.get('staff - volunteers', '0')}\n"
        f"Revenue: Government - ${info.get('revenue from government', '0')}, Donations - ${info.get('donations and bequests', '0')}, Services - ${info.get('revenue from goods and services', '0')}\n"
        f"Total Revenue: ${info.get('total revenue', '0')}\n"
        f"Total Expenses: ${info.get('total expenses', '0')}\n"
        f"Net Surplus/Deficit: ${info.get('net surplus/deficit', '0')}\n"
        f"Total Assets: ${info.get('total assets', '0')}\n"
        f"Total Liabilities: ${info.get('total liabilities', '0')}\n"
        f"Purpose: {info.get('how purposes were pursued', 'N/A')}\n"
    )
    return formatted_info
