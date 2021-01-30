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
            # print(link['data'][self.video_attribute])
            self.reddit_links.append(link['data'][self.video_attribute])

    def downloadVideos(self):
        # TODO: add a way to only run if it hasnt been done before, to avoid downloading videos each time
        dl = youtube_dl.YoutubeDL()
        ydl_opts = {}
        for video in self.reddit_links:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video])

    def getDirectoryVideos(self):
        import glob
        dir = '.'
        # videos = os.path.basename(glob.glob(os.path.join(dir, '*.mp4')))
        videos = [os.path.basename(x)
                  for x in glob.glob(os.path.join(dir, '*.mp4'))]
        return videos

    def mergeVideos(self):
        pass

    def blurVideos(self):
        for video in self.getDirectoryVideos():
            command = ' ffmpeg -i %s -lavfi \'[0:v]scale=ih*16/9:-1,boxblur=luma_radius=min(h\,w)/20:luma_power=1:chroma_radius=min(cw\,ch)/20:chroma_power=1[bg];[bg][0:v]overlay=(W-w)/2:(H-h)/2,crop=h=iw*9/16\' -vb 800K blurred%s ;' % (
                video, video)
            os.system(command)



def shellquote(s):
    return "'" + s.replace("'", "'\\''") + "'"



tiktoks = RedditScrub("tiktokcringe")

tiktoks.getTopVideosToday()

tiktoks.blurVideos()

# os.system("find *.mp4 | sed 's:\ :\\\ :g'| sed 's/^/file /' > fl.txt; ffmpeg -f concat -i fl.txt -c copy output.mp4; rm fl.txt")
# os.system(tiktoks.shellquote("ffmpeg -i output.mp4 -vf 'split [original][copy]\; [copy] crop=ih*9/16:ih:iw/2-ow/2:0, scale=1280:2282, gblur=sigma=20[blurred]\; [blurred][original]overlay=(main_w-overlay_w)/2:(main_h-overlay_h)/2' blurred.mp4"))
