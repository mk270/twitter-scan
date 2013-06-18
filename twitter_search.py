import twitter
import json

def search(term):
    with file('twitter.conf') as f:
        auth = json.load(f)
    api = twitter.Api(**auth)
    for result in api.GetSearch(term=term, query_users=False, per_page=1000):
        yield result
