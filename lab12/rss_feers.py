from flask import Flask, render_template
import feedparser

app = Flask(__name__)

BBC_FEED = "http://feeds.bbci.co.uk/news/rss.xml"


@app.route("/")
@app.route("/<int:limit>")
def headline(limit=5):
    # Limit of the post

    # Store page and body title
    page_title = 'BBC Headline News'
    body_title = page_title

    # Get the RSS feed
    feed = feedparser.parse(BBC_FEED)

    # Fetch articles from the feeds
    articles = feed['entries']

    # Render with the articles array
    return render_template('layout.html', body_title = body_title, page_title = page_title, articles = articles[:limit])


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)

