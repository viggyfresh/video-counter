"""Quick and dirty YouTube and Facebook video view counter."""
from collections import OrderedDict
import csv
import datetime
import re

import requests

YOUTUBE_DATA_URL = "https://www.googleapis.com/youtube/v3/videos"
YOUTUBE_API_KEY = ""  # Rohith: replace with API key

# yapf: disable
URLS = OrderedDict([
    ("Chaddh De", "https://youtu.be/Hpa7fY_bRnc"),
    ("Jiya Jale", "https://youtu.be/pZy8115sNXM"),
    ("AR Rahman Tribute Highlights", "https://youtu.be/WrNH3ybzbz4"),
    ("Yeh Jo Des Hai Tera", "https://youtu.be/0GWWcwpGosw"),
    ("Jaago Piya", "https://youtu.be/i1oivnBSBJc"),
    ("Arz-E-Niyaz", "https://youtu.be/EEc-4FJxTNI"),
    ("Pinha", "https://youtu.be/90P99N6S6rM"),
    ("5 Peace Band", "https://youtu.be/dn_1O3J56E8"),
    ("Manmohini Morey", "https://youtu.be/0PIF52qEjtQ"),
    ("Dil Chahta Hai", "https://youtu.be/TOwVbxpRtY8"),
    ("Jhini", "https://youtu.be/CiMSk_2-QbA"),
    ("Unnai 360", "https://youtu.be/gub20d7WI3I"),
    ("BIE Power Station BTS", "https://youtu.be/TMJGbW6Phxo"),
    ("Lullabies", "https://youtu.be/vFbaa9OmX8E"),
    ("Unnai 2D", "https://youtu.be/ySo9IDdRuck"),
    ("Ghoomar 360", "https://youtu.be/7NGExT9cPKA"),
    ("For Whom the Bell Tolls", "https://youtu.be/K_qpVXsRVio"),
    ("Bombay Theme (1 of 16)", "https://youtu.be/fgjjJOZkXbQ"),
    ("Yeh Jo Des Hai Tera (2 of 16)", "https://youtu.be/sjgdYqyxpWs"),
    ("Chaiyya Chaiyya (3 of 16)", "https://youtu.be/HZbprgd2Rus"),
    ("Jiya Jale (4 of 16)", "https://youtu.be/pYM1Y8ltZoo"),
    ("Romantic Medley (5 of 16)", "https://youtu.be/eJwzol6OoxE"),
    ("Desi Thoughts ft. Prasanna (6 of 16)", "https://youtu.be/ZgmUeeQkY0U"),
    ("Thee Thee & Malargale ft. Mohin Dey (7 of 16)", "https://youtu.be/hbcW7nxcP3E"),
    ("Lagaan Medley (8 of 16)", "https://youtu.be/PIrWquI_mQ0"),
    ("Slumdog Millionaire Medley (9 of 16)", "https://youtu.be/YdzcMNb9Aqk"),
    ("Vinnaithaandi Varuvaayaa (10 of 16)", "https://youtu.be/J_-yMsoJhfI"),
    ("Naan Yen (11 of 16)", "https://youtu.be/gtRSYh14z64"),
    ("Epic Medley (12 of 16)", "https://youtu.be/6oxkWWfiVHs"),
    ("Dil Se Re (13 of 16)", "https://youtu.be/vQnlEkdlXcI"),
    ("Kun Faya Kun (14 of 16)", "https://youtu.be/R-dXS5TI_dQ"),
    ("Tere Bina (15 of 16)", "https://youtu.be/qxmVVa-9xls"),
    ("Vande Mataram (16 of 16)", "https://youtu.be/Ss-kLGW2pHQ"),
    ("Dil Se Re OLD MIX", "https://youtu.be/qH002u7BRx0"),
    ("Clinton Cerejo - Residency", "https://youtu.be/3BX9SOB8S94"),
    ("Clinton Cerejo - Interview", "https://youtu.be/Ki-Uc8GHljY"),
    ("Indian, Middle Eastern, and West African Percussion at Berklee", "https://youtu.be/4aYMhm5hfm0"),
    ("Berklee's Favorite Rahman songs", "https://youtu.be/R0BjcTW96x4"),
    ("AR Rahman receives Berklee Honorary Degree", "https://youtu.be/aKZb3Vmh7GM"),
    ("AR Rahman Berklee Clinic ", "https://youtu.be/7IRuoTgrT98"),
    ("Sivamani - Solo Performance at Berklee College of Music", "https://youtu.be/pXmFlVIEt5M"),
    ("Bombay Theme FB (1 of 16)", "https://www.facebook.com/BerkleeIndia/videos/1901171146802374/"),
    ("Yeh Jo Des Hai Tera FB (2 of 16)", "https://www.facebook.com/BerkleeIndia/videos/1901171420135680/"),
    ("Chaiyya Chaiyya FB (3 of 16)", "https://www.facebook.com/BerkleeIndia/videos/1901174946801994/"),
    ("Jiya Jale FB (4 of 16)", "https://www.facebook.com/BerkleeIndia/videos/1910171595902329/"),
    ("Romantic Medley FB (5 of 16)", "https://www.facebook.com/BerkleeIndia/videos/1914533005466188/"),
    ("Desi Thoughts Prasanna FB (6 of 16)", "https://www.facebook.com/BerkleeIndia/videos/1920346968218125/"),
    ("Thee Thee & Malaragle FB (7 of 16)", "https://www.facebook.com/BerkleeIndia/videos/1929608037292018/"),
    ("Lagaan Medley FB (8 of 16)", "https://www.facebook.com/BerkleeIndia/videos/1935926956660126/"),
    ("Slumdog Millionaire FB (9 of 16)", "https://www.facebook.com/BerkleeIndia/videos/1946469168939238/"),
    ("Vinnaithaandi Varuvaayaa FB (10 of 16)", "https://www.facebook.com/BerkleeIndia/videos/1949246991994789/"),
    ("Naan Yen FB (11 of 16)", "https://www.facebook.com/BerkleeIndia/videos/1956079997978155/"),
    ("Epic Medley FB (12 of 16)", "https://www.facebook.com/BerkleeIndia/videos/1961835030735985/"),
    ("Dil Se Re FB (13 of 16)", "https://www.facebook.com/BerkleeIndia/videos/1966663196919835/"),
    ("Kun Faya Kun FB (14 of 16)","https://www.facebook.com/BerkleeIndia/videos/1976604999258988/"),
    ("Tere Bina FB (15 of 16)", "https://www.facebook.com/BerkleeIndia/videos/1983039721948849/"),
    ("Vande Mataram FB (16 of 16)", "https://www.facebook.com/BerkleeIndia/videos/1989223867997101/"),
    ("Clinton Cerejo talks about Berklee", "https://www.facebook.com/BerkleeIndia/videos/1645429949043163/"),
    ("Vijay Prakash talks about Berklee", "https://www.facebook.com/BerkleeIndia/videos/1648933478692810/"),
    ("BIE Raghu Dixit Rehearsal for BGU (Sh.)", "https://www.facebook.com/BerkleeIndia/videos/1754146934838130/"),
    ("Yogev - BTGC May 2017", "https://www.facebook.com/BerkleeIndia/videos/1830606970525459/"),
    ("Yoel - BTGC May 2017", "https://www.facebook.com/BerkleeIndia/videos/1832598203659669/"),
    ("Guy - BTGC May 2017", "https://www.facebook.com/BerkleeIndia/videos/1834889750097181/"),
    ("Eren - BTGC May 2017", "https://www.facebook.com/BerkleeIndia/videos/1842287902690699/"),
    ("Giving Day 2018", "https://www.facebook.com/BerkleeIndia/videos/1979708045615350/"),
    ("2018 Clinics Teaser", "https://www.facebook.com/BerkleeIndia/videos/1999330116986476/"),
    ("2018 BIX Bootcamp Vocal Intensive Promo", "https://www.facebook.com/BerkleeIndia/videos/2001901626729325/"),
    ("2018 BIX Bootcamp 1st FB Live Promo", "https://www.facebook.com/BerkleeIndia/videos/2004502759802545/"),
    ("Manmohini Morey FB", "https://www.facebook.com/BerkleeIndia/videos/2007330632853091/"),
    ("Jhini FB", "https://www.facebook.com/indianoceanmusic/videos/288330265146786/"),
    ("Unnai 360 FB", "https://www.facebook.com/BerkleeCollege/videos/345481669604109/"),
    ("Ghoomar 360 FB", "https://www.facebook.com/powerstationatberkleenyc/videos/403311917206771/"),
    ("For Whom the Bell Tolls FB", "https://www.facebook.com/BerkleeIndia/videos/410146706311801/"),
    ("Madari", "https://youtu.be/przK5XoEdYA"),
    ("Percussion Jam", "https://youtu.be/OQNPx5C94KY"),
    ("Shuruaat - Behind the Scenes", "https://youtu.be/iahn9OTRHGI"),
    ("Ragam Talam Natyam - Excerpts", "https://youtu.be/Oimpy6bk4KU"),
    ("Natyanjali, Swaranjali Sneak Preview", "https://youtu.be/hF_6fkr_aw8"),
    ("Meet Clinton Cerejo", "https://youtu.be/17WV3t7CdxE"),
    ("Behind the Scenes - Chaddh De", "https://youtu.be/L2OfhuoOqxE"),
    ("What's that sound - series 1 (Bhapang) ", "https://youtu.be/-W0UZuf7TLI"),
    ("Are you the next Berklee Rahman Scholar? YT", "https://youtu.be/tROA8NfxQQQ"),
    ("Vijay Prakash Promo 1 (Katya)", "https://www.facebook.com/katya.krishnan/videos/1059082040789429/"),
    ("Vijay Prakash Promo 2 (Katya)", "https://www.facebook.com/berkleeindianensemble/videos/925493280875242/"),
    ("Vijay Prakash Promo 3 (Katya)", "https://www.facebook.com/berkleeindianensemble/videos/925945050830065/"),
    ("BGU Rehearsal Insta 1", "https://www.facebook.com/berkleeindianensemble/videos/1091463630944872/"),
    ("BGU Rehearsal Insta 2", "https://www.facebook.com/berkleeindianensemble/videos/1095848053839763/"),
    ("BGU Rehearsal Insta 3", "https://www.facebook.com/berkleeindianensemble/videos/1103636849727550/"),
    ("BGU - At Logan Airport Live", "https://www.facebook.com/berkleeindianensemble/videos/1104898602934708/"),
    ("SM Meets Berklee Rehearsal Insta 1", "https://www.facebook.com/berkleeindianensemble/videos/1163914957033072/"),
    ("SM Meets Berklee Recording Insta 2", "https://www.facebook.com/berkleeindianensemble/videos/1177089819048919/"),
    ("Shankar Mahadevan Promo 1 (Katya)", "https://www.facebook.com/berkleeindianensemble/videos/1200149310076303/"),
    ("Shreya Masterclass Promo", "https://www.facebook.com/berkleeindianensemble/videos/1560759530681944/"),
    ("Official Berklee Rahman Scholarship Announcement", "https://www.facebook.com/BerkleeCollege/videos/10153252720511198/"),
    ("Are you the next Berklee Rahman Scholar? FB", "https://www.facebook.com/BerkleeCollege/videos/10153302958366198/"),
    ("Arz-E-Niyaz: CLIP", "https://www.facebook.com/BerkleeCollege/videos/10154110104336198/"),
    ("Pinha: CLIP", "https://www.facebook.com/BerkleeCollege/videos/10154498523186198/"),
    ("5 Peace Band: CLIP", "https://www.facebook.com/BerkleeCollege/videos/10154673247221198/"),
    ("Madiba Wethu", "https://youtu.be/wfPP4wI_3Mc"),
    ("Ishwar Allah", "https://youtu.be/bTwby98fzyw"),
    ("Rhy-dhun", "https://youtu.be/ZKkoQzG-xlc"),
    ("Conference", "https://youtu.be/IbzyhCCY7E8"),
    ("Berklee Indian Ensemble @ BGU Promo", "https://youtu.be/NvNF_vB_Oo0"),
    ("Sur Niragas Ho BGU", "https://youtu.be/bT7SXP3o2QI"),
    ("Rasathi BGU", "https://youtu.be/t7a3tC5l4hc"),
    ("Jiya Jale BGU", "https://youtu.be/SBRVU8plT7I"),
    ("Romantic Medley BGU", "https://youtu.be/BgQuPO8uUVY"),
    ("Raasali BGU", "https://youtu.be/slnvVr2qGkk"),
    ("Lagaan Medley BGU", "https://youtu.be/E52BZ7yruxk"),
    ("Naane Varugiren BGU", "https://youtu.be/KfsGK2sj3eE"),
    ("Zikr BGU", "https://youtu.be/euuPNGgdFVY"),
    ("Manmohini Morey BGU", "https://youtu.be/LOwhNfUmFOY"),
    ("Dil Se Re BGU", "https://youtu.be/Mf9rElyI5-M"),
    ("Kodagana Koli Nungitha BGU", "https://youtu.be/u8C1e9SPjT4"),
    ("Lokada Kalaji BGU", "https://youtu.be/SG33nkNMyYg"),
    ("Epic Medley BGU", "https://youtu.be/5L3WpcEEK90"),
    ("Vande Mataram BGU", "https://youtu.be/REnfjjMPy9w"),
    ("Dil Se Re (Deccan Chronicle post on FB)", "https://www.facebook.com/deccannews/videos/10153799110537160/"),
    ("KFAI Radio Interview", "https://youtu.be/v0Y1xJgYdm4"),
    ("Behind the Scenes for ARR Tribute Show", "https://youtu.be/8ygely4jCLE"),
    ("Bhumi - Berklee Indian Ensemble", "https://youtu.be/IhCR_WFKI_c"),
    ("Pir Jalani - Berklee Indian Ensemble", "https://youtu.be/GoHChfSCqLM"),
    ("5 Peace Band Excerpt (Noor)", "https://www.facebook.com/RohithJayaramanMusic/videos/841934979283923/"),
    ("Rasathi Excerpt (Noor)", "https://www.facebook.com/clint.valladares/videos/10153395662617191/"),
    ("Unnai Kanaadhu Naan Excerpt (Noor)", "https://www.facebook.com/shankarlive/videos/10153776440238640/"),
    ("Shankar Meets Berklee Live 1", "https://www.facebook.com/shankarlive/videos/10154368398863640/"),
    ("Shankar Meets Berklee Live 2", "https://www.facebook.com/shankarlive/videos/10154368665308640/"),
    ("Shankar Meets Berklee Live 3", "https://www.facebook.com/shankarlive/videos/10154368824098640/"),
    ("Shankar Meets Berklee Live 4", "https://www.facebook.com/shankarlive/videos/10154369082718640/"),
    ("Shankar Mahadevan Promo (Sharayu)", "https://www.facebook.com/Mahalenator/videos/1278686858873365/"),
    ("Shreya Sundari Live FB", "https://www.facebook.com/shreyaghoshal/videos/10155943691696484/"),
    ("MGN Jiya Jale", "https://youtu.be/TMKPSpm_g6k"),
    ("Muzammil Jiya Jale", "https://youtu.be/HgYzU6V5Ty0"),
    ("Carl John Franz Jiya Jale", "https://youtu.be/9_ij7-V8fSQ"),
    ("Rukia Dagtan Jiya Jale", "https://youtu.be/D4HWAKa-mZM"),
    ("Ukraine India Calling Jiya Jale", "https://youtu.be/h7TS9FSsjMY"),
    ("Gots Whaat Jiya Jale", "https://youtu.be/EmCr4cu3xmk"),
    ("Indian Afghan Reaction Jiya Jale", "https://youtu.be/yP-wZLN_cNo"),
    ("Ab Bus Reaction Jiya Jale", "https://youtu.be/FKhN8UArjF0"),
    ("Crazy Reaction Jiya Jale", "https://youtu.be/3rAilPCB3zU"),
    ("Def Nuggets Jiya Jale", "https://youtu.be/8qHgXOmDEsg"),
    ("MichiKent Reacts Jiya Jale", "https://youtu.be/nyS62LX7uBU"),
    ("Our Stupid Reactions Jiya Jale", "https://youtu.be/sODd_Yq0qfU"),
    ("V Reacts Jiya Jale", "https://youtu.be/upQxTOK7ypo"),
    ("Gots Whaat Yeh Jo Des", "https://youtu.be/zgqX93sev8U"),
    ("Movie Community College Jiya Jale", "https://youtu.be/CuhGO_akd44"),
    ("TammyKikoy Jiya Jale", "https://youtu.be/oc4Fl2kXdf4"),
    ("ARR Concert Highlights Snippet 2", "https://youtu.be/EdOTr1A3S3s"),
    ("Jiya Jale - Audience Repost 2", "https://youtu.be/-3u_v9kjxLs"),
    ("Jiya Jale - Audience Repost 3", "https://youtu.be/zFcHCRs9PJw"),
    ("Jiya Jale - Audience Repost 4", "https://youtu.be/oYx8OGAc9R4"),
    ("Jaago Piya - Audience Repost 1", "https://www.facebook.com/houseofmusicsrilanka/videos/503301513206043/"),
    ("Rahman Tribute - Loft Show - Audience Camera", "https://youtu.be/mDndiI_feyc"),
    ("Rahman Tribute Highlights - Audience Camera", "https://youtu.be/KxgidoLK7ik"),
    ("Kun Faya Kun - Audience Camera", "https://youtu.be/kVy-dNsmjEU"),
    ("Vande Mataram Snippet - Audience Camera", "https://youtu.be/8rtH_VSSg3U"),
])
# yapf: disable


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
    return (
        regex.findall(page.content.decode("utf-8"))[0]
            .replace(" Views", "")
            .replace(" views", "")
    )


def dump_to_csv(counts):
    """Dumps a list of count objects to a CSV file."""
    with open("counts-%s.csv" % datetime.datetime.now().strftime("%Y-%m-%d"), "w") as csvfile:
        fieldnames = ["Video", "Link", "Count"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for count in counts:
            writer.writerow(count)


def main():
    """Main video counting function."""
    counts = []
    for name, url in URLS.items():
        if is_youtube_video(url):
            count = "Unknown"
            # count = youtube_count(url)
        elif is_facebook_video(url):
            count = facebook_count(url)
        else:
            raise ValueError("Invalid URL provided.")
        print(name, count)
        counts.append({"Video": name, "Link": url, "Count": count})
    dump_to_csv(counts)


if __name__ == "__main__":
    main()
