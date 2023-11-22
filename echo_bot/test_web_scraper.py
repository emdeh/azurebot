from web_scraper import search_website

def test_search_website():
    test_query = 'test query'
    print(f"Testing search with query: {test_query}")

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