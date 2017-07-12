"""Quick and dirty YouTube and Facebook video view counter."""
from collections import OrderedDict
import csv
import datetime
import re

import requests

YOUTUBE_DATA_URL = "https://www.googleapis.com/youtube/v3/videos"
YOUTUBE_API_KEY = "" # Rohith: replace with API key

URLS = OrderedDict([
    ("Jiya Jale", "https://youtu.be/pZy8115sNXM"),
    ("Yeh Jo Des Hai Tera", "https://youtu.be/0GWWcwpGosw"),
    ("Chaddh De ", "https://youtu.be/Hpa7fY_bRnc"),
    ("Jaago Piya", "https://youtu.be/i1oivnBSBJc"),
    ("Dil Se Re", "https://youtu.be/qH002u7BRx0"),
    ("Kun Faya Kun", "https://youtu.be/R-dXS5TI_dQ"),
    ("Arz-E-Niyaz", "https://youtu.be/EEc-4FJxTNI"),
    ("Pinha", "https://youtu.be/90P99N6S6rM"),
    ("5 Peace Band", "https://youtu.be/dn_1O3J56E8"),
    ("AR Rahman Tribute Highlights", "https://youtu.be/WrNH3ybzbz4"),
    ("Dil Se Re (Deccan Chronicle post on FB)",
     "https://www.facebook.com/deccannews/videos/10153799110537160/"),
    ("Berklee's Favorite Rahman songs", "https://youtu.be/R0BjcTW96x4"),
    ("AR Rahman receives Berklee Honorary Degree", "https://youtu.be/aKZb3Vmh7GM"),
    ("Clinton Cerejo - Interview", "https://youtu.be/Ki-Uc8GHljY"),
    ("Clinton Cerejo - Residency", "https://youtu.be/3BX9SOB8S94"),
    ("Official Berklee Rahman Scholarship Announcement",
     "https://www.facebook.com/BerkleeCollege/videos/10153252720511198/"),
    ("Clinton Cerejo talks about Berklee",
     "https://www.facebook.com/BerkleeIndia/videos/1645429949043163/"),
    ("Are you the next Berklee Rahman Scholar? (1)",
     "https://www.facebook.com/BerkleeCollege/videos/10153302958366198/"),
    ("Vijay Prakash talks about Berklee",
     "https://www.facebook.com/BerkleeIndia/videos/1648933478692810/"),
    ("Are you the next Berklee Rahman Scholar? (2)", "https://youtu.be/tROA8NfxQQQ"),
    ("AR Rahman Berklee Clinic ", "https://youtu.be/7IRuoTgrT98"),
    ("Sivamani - Solo Performance at Berklee College of Music", "https://youtu.be/pXmFlVIEt5M"),
    ("Indian, Middle Eastern, and West African Percussion at Berklee",
     "https://youtu.be/4aYMhm5hfm0"),
    ("Madari", "https://youtu.be/przK5XoEdYA"),
    ("Percussion Jam", "https://youtu.be/OQNPx5C94KY"),
    ("Shuruaat - Behind the Scenes", "https://youtu.be/iahn9OTRHGI"),
    ("Ragam Talam Natyam - Excerpts", "https://youtu.be/Oimpy6bk4KU"),
    ("Natyanjali, Swaranjali Sneak Preview", "https://youtu.be/hF_6fkr_aw8"),
    ("Meet Clinton Cerejo", "https://youtu.be/17WV3t7CdxE"),
    ("Behind the Scenes - Chaddh De", "https://youtu.be/L2OfhuoOqxE"),
    ("What's that sound - series 1 (Bhapang) ", "https://youtu.be/-W0UZuf7TLI"),
    ("Vijay Prakash Promo 1 (Katya)",
     "https://www.facebook.com/katya.krishnan/videos/1059082040789429/"),
    ("Vijay Prakash Promo 2 (Katya)",
     "https://www.facebook.com/berkleeindianensemble/videos/925493280875242/"),
    ("Vijay Prakash Promo 3 (Katya)",
     "https://www.facebook.com/berkleeindianensemble/videos/925945050830065/"),
    ("BGU Rehearsal Insta 1",
     "https://www.facebook.com/berkleeindianensemble/videos/1091463630944872/"),
    ("BGU Rehearsal Insta 2",
     "https://www.facebook.com/berkleeindianensemble/videos/1095848053839763/"),
    ("BGU Rehearsal Insta 3",
     "https://www.facebook.com/berkleeindianensemble/videos/1103636849727550/"),
    ("BGU - At Logan Airport Live",
     "https://www.facebook.com/berkleeindianensemble/videos/1104898602934708/"),
    ("BIE Raghu Dixit Rehearsal for BGU (Sh.)",
     "https://www.facebook.com/BerkleeIndia/videos/1754146934838130/"),
    ("SM Meets Berklee Rehearsal Insta",
     "https://www.facebook.com/berkleeindianensemble/videos/1163914957033072/"),
    ("SM Meets Berklee Recording Insta",
     "https://www.facebook.com/berkleeindianensemble/videos/1177089819048919/"),
    ("Shankar Mahadevan Promo 1 (Katya)",
     "https://www.facebook.com/berkleeindianensemble/videos/1200149310076303/"),
    ("Ishwar Allah", "https://youtu.be/bTwby98fzyw"),
    ("Rhy-dhun", "https://youtu.be/ZKkoQzG-xlc"),
    ("Conference", "https://youtu.be/IbzyhCCY7E8"),
    ("Berklee Indian Ensemble @ BGU Promo", "https://youtu.be/NvNF_vB_Oo0"),
    ("Sur Niragas Ho", "https://youtu.be/bT7SXP3o2QI"),
    ("Rasathi", "https://youtu.be/t7a3tC5l4hc"),
    ("Jiya Jale (BGU)", "https://youtu.be/SBRVU8plT7I"),
    ("Romantic Medley", "https://youtu.be/BgQuPO8uUVY"),
    ("Raasali", "https://youtu.be/slnvVr2qGkk"),
    ("Lagaan Medley", "https://youtu.be/E52BZ7yruxk"),
    ("Naane Varugiren", "https://youtu.be/KfsGK2sj3eE"),
    ("Zikr", "https://youtu.be/euuPNGgdFVY"),
    ("Manmohini Morey", "https://youtu.be/LOwhNfUmFOY"),
    ("Huttidare", "https://youtu.be/UXTszZr6c9A"),
    ("Dil Se Re (BGU)", "https://youtu.be/Mf9rElyI5-M"),
    ("Kodagana Koli Nungitha", "https://youtu.be/u8C1e9SPjT4"),
    ("Lokada Kalaji", "https://youtu.be/SG33nkNMyYg"),
    ("Epic Medley", "https://youtu.be/5L3WpcEEK90"),
    ("Vande Mataram", "https://youtu.be/REnfjjMPy9w"),
    ("KFAI Radio Interview", "https://youtu.be/v0Y1xJgYdm4"),
    ("Behind the Scenes for ARR Tribute Show", "https://youtu.be/8ygely4jCLE"),
    ("Bhumi - Berklee Indian Ensemble", "https://youtu.be/IhCR_WFKI_c"),
    ("ARR Concert Highlights Snippet 2", "https://youtu.be/EdOTr1A3S3s"),
    ("Jiya Jale - Audience Repost 2", "https://youtu.be/-3u_v9kjxLs"),
    ("Jiya Jale - Audience Repost 3", "https://youtu.be/zFcHCRs9PJw"),
    ("Jiya Jale - Audience Repost 4", "https://youtu.be/oYx8OGAc9R4"),
    ("Jaago Piya - Audience Repost 1",
     "https://www.facebook.com/houseofmusicsrilanka/videos/503301513206043/"),
    ("Pir Jalani - Berklee Indian Ensemble", "https://youtu.be/GoHChfSCqLM"),
    ("Rahman Tribute - Loft Show - Audience Camera", "https://youtu.be/mDndiI_feyc"),
    ("Rahman Tribute Highlights - Audience Camera", "https://youtu.be/KxgidoLK7ik"),
    ("Kun Faya Kun - Audience Camera", "https://youtu.be/kVy-dNsmjEU"),
    ("Vande Mataram Snippet - Audience Camera", "https://youtu.be/8rtH_VSSg3U"),
    ("Unnai Kanaadhu Naan Excerpt (Noor)",
     "https://www.facebook.com/shankarlive/videos/10153776440238640/"),
    ("5 Peace Band Excerpt (Noor)",
     "https://www.facebook.com/RohithJayaramanMusic/videos/841934979283923/"),
    ("Rasathi Excerpt (Noor)",
     "https://www.facebook.com/clint.valladares/videos/10153395662617191/"),
    ("Shankar Meets Berklee Live 1",
     "https://www.facebook.com/shankarlive/videos/10154368398863640/"),
    ("Shankar Meets Berklee Live 2",
     "https://www.facebook.com/shankarlive/videos/10154368665308640/"),
    ("Shankar Meets Berklee Live 3",
     "https://www.facebook.com/shankarlive/videos/10154368824098640/"),
    ("Shankar Meets Berklee Live 4",
     "https://www.facebook.com/shankarlive/videos/10154369082718640/"),
    ("Shankar Mahadevan Promo (Sharayu)",
     "https://www.facebook.com/Mahalenator/videos/1278686858873365/")
])


def is_youtube_video(url):
    """Checks whether a given URL is from YouTube or not."""
    return "youtu.be" in url or "youtube.com" in url


def is_facebook_video(url):
    """Checks whether a given URL is from Facebook or not."""
    return "facebook.com" in url


def youtube_count(url):
    """Counts the number of views on a Youtube video."""
    video_id = url.split("/")[-1]
    payload = {"id": video_id, "part": "statistics", "key": YOUTUBE_API_KEY}
    resp = requests.get(YOUTUBE_DATA_URL, params=payload)
    try:
        return resp.json()["items"][0]["statistics"]["viewCount"]
    except IndexError:
        return 0


def facebook_count(url):
    """Counts the number of views on a Facebook video."""
    page = requests.get(url)
    regex = re.compile(r"[\d|,]+ [v|V]iews")
    return regex.findall(page.content)[0].replace(" Views", "")


def dump_to_csv(counts):
    """Dumps a list of count objects to a CSV file."""
    with open("counts-%s.csv" % datetime.datetime.now().strftime("%Y-%m-%d"), "wb") as csvfile:
        fieldnames = ["Video", "Link", "Count"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for count in counts:
            writer.writerow(count)


def main():
    """Main video counting function."""
    counts = []
    for name, url in URLS.iteritems():
        if is_youtube_video(url):
            count = youtube_count(url)
        elif is_facebook_video(url):
            count = facebook_count(url)
        else:
            raise ValueError("Invalid URL provided.")
        print name, count
        counts.append({"Video": name, "Link": url, "Count": count})
    dump_to_csv(counts)


if __name__ == "__main__":
    main()
