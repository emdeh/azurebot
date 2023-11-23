from web_scraper import search_website

def test_search_website():
    # Ask the user for a charity name
    test_query = input("Enter the name of the charity to search: ")
    print(f"Testing search with query: '{test_query}'")

    # Call the search function
    results = search_website(test_query)

    # Check if results are returned
    if results:
        print("Search successful! Results:")
        print(results)
    else:
        print("Search failed or returned no results.")

if __name__ == '__main__':
    test_search_website()