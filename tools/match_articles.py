# def match_articles(user_prompt: str, articles: list[dict]) -> list[dict]:
#     query = user_prompt.lower()
#     matches = []

#     for article in articles:
#         searchable_text = (
#             article["headline"] +
#             article["full_text"] +
#             article["category"] +
#             article["city"]
#         ).lower()

#         if any(word in searchable_text for word in query.split()):
#             matches.append(article)

#     return matches


#new one
def safe_str(value) -> str:
    return value if isinstance(value, str) else " "

def match_articles(user_prompt: str, articles: list[dict]) -> list[dict]:
    query_words = user_prompt.lower().split()
    matches = []

    for article in articles:
        searchable_text = " ".join([
            safe_str(article.get("headline")),
            safe_str(article.get("full_text")),
            safe_str(article.get("category")),
            safe_str(article.get("city")),
        ]).lower()

        if any(word in searchable_text for word in query_words):
            matches.append(article)

    return matches
