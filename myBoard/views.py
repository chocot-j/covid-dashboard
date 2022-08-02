from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .covid import deathCnt_plot, decideCnt_plot
from .covid2 import stateRank_plot, map_plot, totalCnt_plot, covid_incDec, vaccine_plot

def index(request):
    death_plot = deathCnt_plot()
    decide_plot = decideCnt_plot()
    stateR_plot = stateRank_plot()
    kmap_plot = map_plot()
    total_plot = totalCnt_plot()
    vac_plot = vaccine_plot()
    incDec, incDecK, incDecF = covid_incDec()
    context = {
        'death_plot': death_plot,
        'decide_plot': decide_plot,
        'stateR_plot': stateR_plot,
        'kmap_plot': kmap_plot,
        'total_plot': total_plot,
        'vac_plot': vac_plot,
        'incDec':incDec,
        'incDecK':incDecK,
        'incDecF':incDecF,
    }
    return render(request, 'dashBoard.html', context=context)