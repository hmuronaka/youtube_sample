#!/usr/bin/python

import pprint
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser


# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = ""
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def get_youtube():
  return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

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
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

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
  argparser.add_argument("--q", help="Search term", default="Ga3maNZ0x0w")
  argparser.add_argument("--max-results", help="Max results", default=25)
  argparser.add_argument("--part", help="part index", default=1)
  args = argparser.parse_args()

  try:
    #youtube_search(args)
    # get_video(args.q, int(args.part))
    #get_captions(args.q)
  except HttpError, e:
    print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)
