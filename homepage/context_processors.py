from homepage.forms import SearchForm

def insert_search_form (request):
    return {
        "search_form": SearchForm()
    }