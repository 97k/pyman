import pytube
import sys
import os
import urllib.request
import urllib.error
import re
import time

def getPlaylistUrlID(url):
    if 'list=' in url:
        eq_idx = url.index('=') + 1
        pl_id = url[eq_idx:]
        if '&' in url:
            amp = url.index('&')
            pl_id = url[eq_idx:amp]
        return pl_id   
    else:
        print(url, "is not a youtube playlist.")
        exit(1)

def getFinalVideoUrl(vid_urls):
    final_urls = []
    for vid_url in vid_urls:
        url_amp = len(vid_url)
        if '&' in vid_url:
            url_amp = vid_url.index('&')
        final_urls.append('http://www.youtube.com/' + vid_url[:url_amp])
    return final_urls        

def printUrls(vid_urls):
    for url in vid_urls:
        print(url)
        time.sleep(0.04)    

def getPageHtml(url):
    try:
        yTUBE = urllib.request.urlopen(url).read()
        return str(yTUBE)
    except urllib.error.URLError as e:
        print(e.reason)
        exit(1)

def getPlaylistVideoUrls(page_content, url):
    # urls = []
    playlist_id = getPlaylistUrlID(url)

    vid_url_pat = re.compile(r'watch\?v=\S+?list=' + playlist_id)
    vid_url_matches = list(set(re.findall(vid_url_pat, page_content)))

    if vid_url_matches:
        final_vid_urls = getFinalVideoUrl(vid_url_matches)
        # urls.append(final_vid_urls)
        print("Found",len(final_vid_urls),"videos in playlist.")
        printUrls(final_vid_urls, '\n')
        return final_vid_urls
    else:
        print('No videos found.')
        exit(1)

if __name__ == '__main__':
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print('USAGE: python ytPlDl.py <playlistURL> OR python ytPlDl.py <playlistURL> <destination Path>')
        print('\nExample\n', """python ytPlDl.py https://www.youtube.com/playlist\?list\=PL3FW7Lu3i5JvHM8ljYj-zLfQRF3EO8sYv ~/Downloads/cs231n""")

        exit(1)
    else:
        url = sys.argv[1]
        directory = os.getcwd() if len(sys.argv) != 3 else sys.argv[2]
    
        # make directory if dir specified doesn't exist
        try:
            os.makedirs(directory, exist_ok=True)
        except OSError as e:
            print(e.reason)
            exit(1)

        if not url.startswith("http"):
            url = 'https://' + url

        playlist_page_content = getPageHtml(url)

        urls = getPlaylistVideoUrls(playlist_page_content, url)

        numofvids = len(urls)
        for vid in urls:
            yt = pytube.YouTube(vid)
            stream = yt.streams.first()

            stream.download(directory)
            numofvids -= 1
            print(len(urls)-numofvids, 'has been downloaded!', numofvids, 'videos left!')
