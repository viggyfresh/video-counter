# Video Counter

Counts the number of views for specified videos from YouTube or Facebook.

## Initial Usage

1. Open up a Terminal window.

2. Run the following commands:
    ```bash
    sudo pip install virtualenv
    git clone https://github.com/viggyfresh/video-counter.git
    cd video-counter
    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3. Edit counter.py to have the URLs you care about.

4. Run `python counter.py` from the Terminal.

5. Finally, examine `counts.csv` to get your data!

## Subsequent Usage

1. If needed, make edits to the URLs.

2. Open up a Terminal window.

3. Run the following commands:
    ```bash
    cd /path/to/video-counter
    source venv/bin/activate
    python counter.py
    ```

4. Examine `counts.csv` to get your data!
