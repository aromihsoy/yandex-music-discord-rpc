from yandex_music import Client


client = Client().init()


def get_yandex_cover(artist, title):
    try:

        search_result = client.search(f"{artist} - {title}", type_="track")
        
        if search_result.tracks and search_result.tracks.results:
            track = search_result.tracks.results[0]
            
            if track.cover_uri:
                cover_url = f"https://{track.cover_uri.replace('%%', '1000x1000')}"
                print(f"Получена обложка для {cover_url}")
                return cover_url
            
    except Exception as e:
        print(f"Ошибка при получении обложки: {e}")

    return "yandex_logo"