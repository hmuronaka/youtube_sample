#!/usr/bin/python

import os
import pprint
from apiclient.errors import HttpError
from oauth2client.tools import argparser
from get_youtube import authenticated_youtube_developer_key, authenticated_youtube_oauth, get_youtube

def get_caption(id, tfmt):
  pp = pprint.PrettyPrinter(indent=4)
  y = get_youtube()
  result = y.captions().download(
    id=id,
    tfmt=tfmt
  ).execute()
  pp.pprint(result)
 

def get_captions(id):
  pp = pprint.PrettyPrinter(indent=4)
  y = get_youtube()
  result = y.captions().list(
    part='snippet',
    videoId=id
  ).execute()
  pp.pprint(result)
    

def get_video(id, partIdx):
  pp = pprint.PrettyPrinter(indent=4)
  y = get_youtube()
  parts = ['id', 'snippet', 'contentDetails', 'fileDetails', 'liveStreamingDetails', 'player', 'processingDetails', 'recodingDetails', 'statistics', 'status',
    'suggestions', 'topicDetails']
  result = y.videos().list(
    part=parts[partIdx],
    id=id
  ).execute()
  pp.pprint(result)

def youtube_search(options):
  youtube = get_youtube()

  # Call the search.list method to retrieve results matching the specified
  # query term.
  search_response = youtube.search().list(
    q=options.q,
    part="id,snippet",
    maxResults=options.max_results
  ).execute()

  videos = []
  channels = []
  playlists = []

  # Add each result to the appropriate list, and then display the lists of
  # matching videos, channels, and playlists.
  for search_result in search_response.get("items", []):
    if search_result["id"]["kind"] == "youtube#video":
      videos.append("%s (%s)" % (search_result["snippet"]["title"],
                                 search_result["id"]["videoId"]))
    elif search_result["id"]["kind"] == "youtube#channel":
      channels.append("%s (%s)" % (search_result["snippet"]["title"],
                                   search_result["id"]["channelId"]))
    elif search_result["id"]["kind"] == "youtube#playlist":
      playlists.append("%s (%s)" % (search_result["snippet"]["title"],
                                    search_result["id"]["playlistId"]))

  print "Videos:\n", "\n".join(videos), "\n"
  print "Channels:\n", "\n".join(channels), "\n"
  print "Playlists:\n", "\n".join(playlists), "\n"


if __name__ == "__main__":
  argparser.add_argument("--q", help="Search term", default="UF8uR6Z6KLc")
  argparser.add_argument("--cmd", help="Search term", default="search")
  argparser.add_argument("--max-results", help="Max results", default=25)
  argparser.add_argument("--part", help="part index", default=1)
  argparser.add_argument("--tfmt", help="srt, ttml...", default="ttml")
  argparser.add_argument("--oauth", help="1: developerkey, 0:oauth", default=0)
  args = argparser.parse_args()

  actions = {
    'search': (lambda args: youtube_search(args)),
    'video': (lambda args: get_video(args.q, int(args.part))),
    'captions': (lambda args: get_captions(args.q)),
    'caption': (lambda args: get_caption(args.q, args.tfmt))
  } 
  try:
    if int(args.oauth) == 1:
      authenticated_youtube_oauth(args)
    else:
      authenticated_youtube_developer_key()  
    actions[args.cmd](args)
  except HttpError, e:
    print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)
