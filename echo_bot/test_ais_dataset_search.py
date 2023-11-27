import asyncio
from ais_dataset_search import retrieve_charity_data, format_charity_info

async def test_retrieve_charity_data():
    # Ask the user for a charity name
    query = input("Enter the name of the charity to search: ")
    print(f"Testing search with query: '{query}'")

    # Call the api search function
    data = await retrieve_charity_data(query)
    formatted_data = format_charity_info(data)
    print("Retrieved Data:")
    print(formatted_data)

if __name__ == "__main__":
    asyncio.run(test_retrieve_charity_data())