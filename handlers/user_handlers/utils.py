async def dictionary_faculty_key(key):
    data = {
        "fkit": "фкіт",
        "fmmt": "фммт",
        "fbp": "фбп",
        "ftsost": "фцост",
        "ftmi": "фтмі",
        "fate": "фате",
        "fabd": "фабд",
        "general_gov": "загал",
        "profcom": "профком",
        "h1": "гурт1",
        "h2": "гурт2",
        "h3": "гурт3",
    }
    return data.get(key, "Невідомий факультет")