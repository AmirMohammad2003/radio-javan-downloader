import requests
import urllib.parse
import re
# import fake_useragent


class Downloader:
    base_url = "https://www.radiojavan.com"
    mp3s_host = base_url + "/mp3s/mp3_host"
    podcasts_host = base_url + "/podcasts/podcast_host"
    videos_host = base_url + "/videos/video_host"

    def __init__(self, url):
        self.url = url
        # self.user_agent = fake_useragent.UserAgent(
        #     fallback="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36"
        # ).random
        self.cookies = None
        self.id = None
        self.token = None
        self.identify_type()
        self.get_page()

    def get_page(self):
        # headers = {"User-Agent": self.user_agent}
        response = requests.get(
            self.url,
            # headers=headers,
        )
        self.cookies = response.cookies
        self.id = urllib.parse.urlparse(self.url).path.split("/")[-1]

        token = re.findall(
            r"<meta name=\"csrf-token\" content=\".*\" />", response.text
        )
        self.token = token[0].split()[-2].split("=", 1)[-1][1:-1]

    def get_download_link(self):
        headers = {
            # "User-Agent": self.user_agent,
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "content-type": "application/x-www-form-urlencoded",
            "x-requested-with": "XMLHttpRequest",
            "x-csrf-token": self.token,
            "referer": self.url,
            "origin": Downloader.base_url,
        }

        extension = "mp3"
        if self.type == "mp3":
            host_sub_url = "mp3/mp3-256/"
            get_host_url = Downloader.mp3s_host

        elif self.type == "podcast":
            host_sub_url = "podcast/mp3-192/"
            get_host_url = Downloader.podcasts_host

        elif self.type == "video":
            host_sub_url = "music_video/hd/"
            extension = "mp4"
            get_host_url = Downloader.videos_host

        r = requests.post(
            get_host_url, cookies=self.cookies,
            data={"id": self.id}, headers=headers
        )

        host = r.json()["host"]
        return host + "/media/" + host_sub_url + self.id + "." + extension

    def identify_type(self):
        if (self.url.find("/mp3s/mp3/") != -1):
            self.type = "mp3"

        elif (self.url.find("/videos/video/") != -1):
            self.type = "video"

        elif (self.url.find("/podcasts/podcast/") != -1):
            self.type = "podcast"
