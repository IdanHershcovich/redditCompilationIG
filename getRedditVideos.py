# curl -s -H "User-agent: 'myScript'" https://www.reddit.com/r/TikTokCringe/top.json\?sort\=top\&t\=day\&limit\=12 | jq '.' |  grep url_overridden_by_dest | grep -Eoh "https:\/\/v\.redd\.it\/\w{13}"

import requests
import youtube_dl
import os
import subprocess


class RedditScrub:
    def __init__(self, subreddit, sort_by=None, time_filter=None, limit=None):
        self.subreddit = subreddit
        self.url = "https://www.reddit.com/r/"+subreddit + "/"
        self.sort_by = sort_by
        self.time_filter = time_filter
        self.limit = limit
        self.video_attribute = 'url_overridden_by_dest'
        self.headers = {
            'User-agent': '\'myScript\'',
        }
        self.reddit_links = []

    def getTopVideosToday(self):
        url = self.url + "top.json?sort=top&t=day&limit=12"
        res = requests.get(url, headers=self.headers)
        if res.status_code != 200:
            print("something wrong with url")
            print(url)
            return
        json = res.json()
        data = json['data']['children']
        for link in data:
            self.reddit_links.append(link['data'][self.video_attribute])

    def downloadVideos(self):
        # TODO: add a way to only run if it hasnt been done before, to avoid downloading videos each time
        dl = youtube_dl.YoutubeDL()
        ydl_opts = {
            'outtmpl': 'mp4/%(title)s.%(ext)s'
        }
        for video in self.reddit_links:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video])

    def getDirectoryVideos(self):
        import glob
        dir = './mp4/'
        # videos = os.path.basename(glob.glob(os.path.join(dir, '*.mp4')))
        videos = [os.path.basename(x) for x in glob.glob(dir)]
        return videos

    def mergeVideos(self):
        # os.system('for f in mp4/*.mp4; do echo "file $f" >> list.txt; done && ffmpeg -f concat -i list.txt final.mp4 && rm list.txt')
        os.system('for f in mp4/*.mp4 ; do echo " file $f" >> list.txt; done && ffmpeg -f concat -safe 0 -i list.txt -s 1280x720 -crf 24 stitched-video.mp4 && rm list.txt')

        #os.system('ffmpeg -f concat -safe 0 -i list.txt -s 1280x720 -crf 24 stitched-video.mp4 && rm list.txt')



    def blurVideos(self):
        for video in self.getDirectoryVideos():
            command = ' ffmpeg -i %s -lavfi \'[0:v]scale=ih*16/9:-1,boxblur=luma_radius=min(h\,w)/20:luma_power=1:chroma_radius=min(cw\,ch)/20:chroma_power=1[bg];[bg][0:v]overlay=(W-w)/2:(H-h)/2,crop=h=iw*9/16\' -vb 800K ./blur/blurred%s ;' % (video, video)
            os.system(command)



tiktoks = RedditScrub("tiktokcringe")

# tiktoks.getTopVideosToday()

# tiktoks.downloadVideos()

# print(tiktoks.getDirectoryVideos())

# tiktoks.blurVideos()

tiktoks.mergeVideos()

