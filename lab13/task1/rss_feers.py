from flask import Flask, render_template, request
import feedparser

app = Flask(__name__)

BBC_FEED = "http://feeds.bbci.co.uk/news/rss.xml"


@app.route("/")
def headlines():

    # Store page and body title
    page_title = 'BBC Headline News'
    body_title = page_title

    # Get the RSS feed
    feed = feedparser.parse(BBC_FEED)

    # Fetch articles from the feeds
    articles = feed['entries']

    title = request.args.get('title') or ''

    # search the article title
    articles = [a for a in articles if title.lower() in a.title.lower()]

    # Render with the articles array
    return render_template('headlines.html',
                           page_title=page_title,
                           body_title=body_title,
                           articles=articles,
                           resultsNum=len(articles),
                           )


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4000)
