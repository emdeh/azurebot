import asyncio
from ais_dataset_search import retrieve_charity_data

async def test_retrieve_charity_data():
    query = "test charity"  # Replace with a relevant test query
    data = await retrieve_charity_data(query)
    print("Retrieved Data:")
    print(data)

if __name__ == "__main__":
    asyncio.run(test_retrieve_charity_data())
