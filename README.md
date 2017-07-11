# Video Counter

Counts the number of views for specified videos from YouTube or Facebook.

## Usage

First, edit counter.py to have the URLs you care about. Then:

```bash
[sudo] pip install virtualenv
git clone https://github.com/viggyfresh/video-counter.git
cd video-counter
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python counter.py
```

Finally, examine `counts.csv` to get your data!
