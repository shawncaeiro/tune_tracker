import json
import sys
import random
import requests
import urllib
import base64
from requests.auth import HTTPBasicAuth
from django.contrib import messages


from django.shortcuts import redirect, render

from tune_throwback.models import Song, Rank
import tune_throwback.spotify_web_api as spot


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
    ranked_song = random.choice(Rank.objects.filter(rank__lte = 25))
    return redirect('/results/{0}/'.format(ranked_song.song.pk))

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

def spotify_success(request):
    playlist = request.POST["sel1"]
    token = request.session["at"]
    s_id = request.session["s_id"]
    songs = request.POST.getlist('song_choices')
    m, success = spot.add_songs_to_playlist(s_id, token, playlist, songs)
    if success:
        messages.add_message(request, messages.INFO, 'Songs successfully added!')
    else:
        messages.add_message(request, messages.WARNING, str(m))        
    return render(request, 'success.html', {'ck': songs, 'p':playlist})

def spotify_return(request):
    try:
        code = request.GET.get("code", request.GET["state"])
        state = request.GET["state"]
        request.session["state"] = state
    except:
        return redirect('/')
    sp_redirect = "http://127.0.0.1:8000/spotify_return/"
    
    at, success = spot.get_auth_token(code, state, sp_redirect)
    if not success:
        return redirect('/')
    request.session['at'] = at

    s_id, success = spot.get_spotify_user_id(at)
    if not success:
        return redirect('/')
    request.session['s_id'] = s_id

    playlists, success = spot.get_spotify_user_playlists(at, s_id)
    if not success:
        return redirect('/')

    org_song = Rank.objects.filter(song__pk=state).order_by('rank')[0]
    similar_songs = Rank.objects.filter(week=org_song.week).exclude(song__spotify_id="").order_by('rank')[:25]

    return render(request, 'spotify_upload.html', {'playlists':playlists, 'songs':similar_songs})

def spotify_auth(request, state):
    url, success = spot.get_spotify_code_url(state)
    if not success:
        return redirect('/')
    return redirect(url)
