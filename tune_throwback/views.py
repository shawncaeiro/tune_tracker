import json
import sys
import random

from django.shortcuts import redirect, render

from tune_throwback.models import Song, Rank


def home_page(request):
    songs = list(Song.objects.values_list('title', 'artist').distinct())
    j_songs = []
    for song in songs:
        j_songs.append("{0} -- {1}".format(song[0],song[1]))
    j_songs = list(set(i.lower().title() for i in j_songs))
    j_songs = json.dumps(j_songs)
    return render(request, 'home.html', {'songs':j_songs})

def results_page_helper(request, r_song):
    songs = list(Song.objects.values_list('title', 'artist').distinct())
    j_songs = []
    for song in songs:
        j_songs.append("{0} -- {1}".format(song[0],song[1]))
    j_songs = list(set(i.lower().title() for i in j_songs))
    j_songs = json.dumps(j_songs)

    similar_songs = Rank.objects.filter(week=r_song.week).order_by('rank')[:25]
    spotify_ids = Rank.objects.filter(week=r_song.week).exclude(song__spotify_id = "").order_by('rank')[:25]
    return render(request, 'results.html', {'all_songs': j_songs, 'ranked': r_song, 'songs':similar_songs, 'spotify_ids':spotify_ids})

def results_page_random(request):
    #song = random.choice(Song.objects.all())
    #ranked_song = Rank.objects.filter(song__title = song.title, song__artist = song.artist).order_by('rank')[0]
    ranked_song = random.choice(Rank.objects.filter(rank__lte = 25))
    return redirect('/results/{0}/'.format(ranked_song.song.pk))

#def results_page_post

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
            s, a = request.POST["song_text"].split(' -- ')
            r_song = Rank.objects.filter(song__title__iexact= s, song__artist__iexact= a).order_by('rank')[0]
            return redirect('/results/{0}/'.format(r_song.song.pk))
        except:
            return redirect('/')            
    else:
        return redirect('/')
