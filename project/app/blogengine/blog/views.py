from django.shortcuts import render

# Create your views here.
def posts_list(request):
    n = ['Oleg', 'Masha', 'Watson']
    return render(request, 'blog/index.html', context={'names': n})
