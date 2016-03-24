import json
import sys

from django.shortcuts import redirect, render

from tune_throwback.models import Song, Rank


def home_page(request):
    songs = list(Song.objects.values_list('title', flat=True).distinct())
    j_songs = json.dumps(songs)
    return render(request, 'home.html', {'songs':j_songs})

def results_page_helper(request, r_song):
    songs = list(Song.objects.values_list('title', flat=True).distinct())
    j_songs = json.dumps(songs)

    similar_songs = Rank.objects.filter(week=r_song.week).order_by('rank')[:25]
    return render(request, 'results.html', {'all_songs': j_songs, 'ranked': r_song, 'songs':similar_songs})

def results_page(request, song_id = None):
    if str(song_id).isdigit():
        try:
            s_temp = Song.objects.get(pk=song_id)
            r_song = Rank.objects.filter(song__title = s_temp.title).order_by('rank')[0]
            return results_page_helper(request, r_song)
        except:
            return redirect('/results')
    elif request.method == 'POST':
        try:
            r_song = Rank.objects.filter(song__title= request.POST["song_text"]).order_by('rank')[0]
            return results_page_helper(request, r_song)            
        except:
            return redirect('/')            
    else:
        return redirect('/')
