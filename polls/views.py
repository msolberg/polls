from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    """Home page"""
    return HttpResponse("Polls application. New Title!")

def health(request):
    """Takes an request as a parameter and gives the count of pageview objects as reponse"""
    return HttpResponse("Healthy!")

