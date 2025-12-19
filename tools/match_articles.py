def match_articles(user_prompt: str, articles: list[dict]) -> list[dict]:
    query = user_prompt.lower()
    matches = []

    for article in articles:
        searchable_text = (
            article["headline"] +
            article["full_text"] +
            article["category"] +
            article["city"]
        ).lower()

        if any(word in searchable_text for word in query.split()):
            matches.append(article)

    return matches
