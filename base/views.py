from django.shortcuts import render


def preview(request):
    return render(request, 'base/preview.html')