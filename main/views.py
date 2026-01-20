from django.http import HttpRequest, HttpResponse


def landing_page_view(request: HttpRequest) -> HttpResponse:
    html_content = """
    <h1>The Ol' Game Site</h1>
    <p>Welcome to the Ol' Game Site!</p>
    """
    return HttpResponse(html_content)
