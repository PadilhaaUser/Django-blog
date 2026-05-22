from django.shortcuts import render
from django.http import HttpResponse

posts = [
    {
        'author': 'Paulo',
        'title': 'First Post',
        'content': 'This is the content of the first post.',
        'date_posted': '21 de janeiro de 2026'
    },
    {
        'author': 'Maria',
        'title': 'Second Post',
        'content': 'This is the content of the second post.',
        'date_posted': '23 de janeiro de 2026'
    },
    {
        'author': 'João',
        'title': 'Third Post',
        'content': 'This is the content of the third post.',
        'date_posted': '24 de janeiro de 2026'
    },

]

# views 
def home(request):
    context = {
        'posts': posts
    }
    return render(request, 'blog/home.html', context)

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})