# curl -s -H "User-agent: 'myScript'" https://www.reddit.com/r/TikTokCringe/top.json\?sort\=top\&t\=day\&limit\=12 | jq '.' |  grep url_overridden_by_dest | grep -Eoh "https:\/\/v\.redd\.it\/\w{13}"

import requests


class RedditScrub:
    def __init__(self, subreddit, sort_by=None, time_filter=None, limit=None):
        self.subreddit = subreddit
        self.url = "https://www.reddit.com/r/"+subreddit + "/"
        self.sort_by = sort_by
        self.time_filter = time_filter
        self.limit = limit
        self.video_attribute = 'url_overridden_by_dest'
        self.headers  = {
            'User-agent': '\'myScript\'',
        }
        self.reddit_links = []


    def getTopVideosToday(self):
        url = self.url + "top.json?sort=top&t=day&limit=12"
        res = requests.get(url, headers = self.headers)
        if res.status_code != 200:
            print("something wrong with url")
            print(url)
            return
        json = res.json()
        data = json['data']['children']
        for link in data:
            print(link['data'][self.video_attribute])
            self.reddit_links.append(link)




params = (
    ('sort/', 'top/'),
    ('t/', 'day/'),
    ('limit/', '12'),
)

#response = requests.get('https://www.reddit.com/r/TikTokCringe/top.json', headers=headers, params=params)


tiktoks = RedditScrub("tiktokcringe")

tiktoks.getTopVideosToday()