from winrt.windows.media.control import GlobalSystemMediaTransportControlsSessionManager as MediaManager
from winrt.windows.media.control import GlobalSystemMediaTransportControlsSessionPlaybackStatus as PlaybackStatus


async def get_current_music():

    sessions = await MediaManager.request_async()

    all_sessions = sessions.get_sessions()

    target_session = None

    for session in all_sessions:

        app_name = session.source_app_user_model_id.lower()

        if "yandex" in app_name:
            target_session = session
            break

    
    if not target_session:
        return None


        
    info = await target_session.try_get_media_properties_async()

    playback_info = target_session.get_playback_info()
    is_playing = playback_info.playback_status == PlaybackStatus.PLAYING
    is_paused = playback_info.playback_status == PlaybackStatus.PAUSED


    if not (is_playing or is_paused):
        return None

    return {
        'title': info.title,
        'artist': info.artist,
        'is_paused': is_paused,
    }