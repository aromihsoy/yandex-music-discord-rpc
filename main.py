import asyncio
import time
import threading
import pystray

from PIL import Image, ImageDraw
from pypresence import Presence

from config import CLIENT_ID
from yandex_api import get_yandex_cover
from windows_media import get_current_music


# Управляет жизнью программы
is_running = True


def run_discord_rpc():
    global is_running
    print("Подключаемся к Discord...")

    try:
        rpc = Presence(CLIENT_ID)
        rpc.connect()
        print("Подключение успешно!")
    except Exception as e:
        print(f"Не удалось подключиться к Discord: {e}")
        return
    
    current_track_name = ""
    current_cover = "yandex_logo"


    while is_running:
        try:
            music = asyncio.run(get_current_music())

            if music and music['title']:
                track_full_name = f"{music['artist']} - {music['title']}"

                if track_full_name != current_track_name:
                    print(f"Новый трек! Ищем обложку для: {track_full_name}")
                    current_cover = get_yandex_cover(music["artist"], music["title"])
                    current_track_name = track_full_name

                if music['is_paused']:
                    state_text = f"⏸ На паузе: {music['artist']} - {music['title']}"
                else:
                    state_text = f"Исполнитель: {music['artist']}"
                
                rpc.update(
                    details=f"Трек: {music['title']}",
                    state=state_text,
                    large_image=current_cover,
                    large_text="Яндекс Музыка"
                )
            else:
                rpc.clear()
                current_track_name = ""


            for _ in range(15):
                if not is_running:
                    break
                time.sleep(1)
        
        except Exception as e:
            print(f"Ошибка RPC: {e}")
            time.sleep(15)
    

    rpc.clear()
    rpc.close()
    print("Отключение от Discord.")


def create_image():
    image = Image.new('RGB', (64,64), color=(20,20,20))
    dc = ImageDraw.Draw(image)
    dc.ellipse((16,16,48,48), fill=(255,0,0))
    return image

def on_quit(icon, item):
    global is_running
    is_running = False
    icon.stop()

def setup_tray():
    image = create_image()

    menu = pystray.Menu(
        pystray.MenuItem('Выход', on_quit)
    )


    icon = pystray.Icon("YandexRPC", image, "Yandex Music RPC", menu)
    print("Программа запущена. Ищите кнопку в системном трее!")
    icon.run()

if __name__ == "__main__":
    rpc_thread = threading.Thread(target=run_discord_rpc)
    rpc_thread.start()

    setup_tray()