from django.http import HttpResponse, Http404
from medapp.models import Article



def sorted_articles_view(request, username):
    """
    Get a list of articles sorted according to the user's specified preferences.

    """
    sort_by = request.GET.get('sort_by', 'title')
    valid_sort_options = ['title', 'date']
    if sort_by not in valid_sort_options:
        raise Http404('Invalid sorting parameter')

    articles = Article.objects.filter(author__username=username)
    if sort_by == 'title':
        sorted_articles = articles.order_by('title')
    elif sort_by == 'date':
        sorted_articles = articles.order_by('-created_at')
    else:
        sorted_articles = None
    if sorted_articles is not None:
        article_titles = '\n'.join(article.title for article in sorted_articles)
        return HttpResponse(article_titles, content_type='text/plain')
    else:
        raise Http404('User not found')
        