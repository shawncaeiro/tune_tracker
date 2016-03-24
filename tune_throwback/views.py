import json
import sys

from django.shortcuts import redirect, render

from tune_throwback.models import SongRank


def home_page(request):
    songs = list(SongRank.objects.order_by()
        .values_list('song', flat=True).distinct())
    j_songs = json.dumps(songs)
    return render(request, 'home.html', {'songs':j_songs})

def results_page_helper(request, song):
    songs = list(SongRank.objects.order_by()
        .values_list('song', flat=True).distinct())
    j_songs = json.dumps(songs)

    similar_songs = SongRank.objects.filter(week=song.week).order_by('rank')[:25]
    return render(request, 'results.html', {'all_songs': j_songs, 'song': song, 'songs':similar_songs})

def results_page(request, song_id = None):
    if str(song_id).isdigit():
        try:
            s_temp = SongRank.objects.get(pk=song_id)
            s_ranked = SongRank.objects.filter(song=s_temp.song).order_by('rank')[0]
            return results_page_helper(request, s_ranked)
        except:
            return redirect('/results')
    elif request.method == 'POST':
        try:
            s = SongRank.objects.filter(song=request.POST['song_text']).order_by('rank')[0]
            return results_page_helper(request, s)            
        except:
            return redirect('/')            
    else:
        return redirect('/')
