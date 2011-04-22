#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) 2011 Sebastian Oliva <tian2992@gmail.com>
#Permission to use, copy, modify, and/or distribute this software for any
#purpose with or without fee is hereby granted, provided that the above
#copyright notice and this permission notice appear in all copies.

#THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
#WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
#MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
#ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
#WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
#ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
#OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

import os
import xchat
import urllib2
from BeautifulSoup import BeautifulStoneSoup

__module_name__ = "XChat Last.fm Now Playing"
__module_version__ = "0.1"
__module_description__ = "A now playing status for last.fm"

API_ROOT = "http://ws.audioscrobbler.com/2.0/"
API_KEY  = "65de5693b849daf62e844a50c2e5acf6"

def get_playing_song(username):
  try:
    raw_page = urllib2.urlopen(API_ROOT+"/?method=user.getrecenttracks&user="+username+"&api_key="+API_KEY)
    page_data = BeautifulStoneSoup(raw_page)
    current_track = page_data.track
    artist = current_track.artist.text
    song = current_track.find("name").text #because .name returns other things
    album = current_track.album.text
    #let's make a status :3
    status = song + " - " + artist
    if album != "":
      status = status + " (" + album + ")"
    if username == xchat.get_info("nick"):
      xchat.command("me last listened to %s" % (status.encode('utf-8')))
    else:
      xchat.command("say "+username+" last listened to %s" % (status.encode('utf-8')))
  except:
    xchat.prnt("An error ocurred, probably a wrong Username")
    
def EXChatMPD(word, word_eol, userdata):
  current_nick = xchat.get_info("nick")
  if (len(word)<=1):
    get_playing_song(current_nick)
  else:
    get_playing_song(word[1])
  return xchat.EAT_ALL
  
xchat.hook_command("lastfm", EXChatMPD, help="/lastfm for your last played song, or /lastfm NICK, for NICK's current playing song")
