from syncro.service.platform.Spotify import get_token, get_track_id_spotify, track_already_exist, add_music_to_playlist


class BaseRadio:
    def __init__(self, playlist):
        self.__playlist = playlist

    def execute(self, token, client_id, client_secret):
        new_token = get_token(token, client_id, client_secret)

        for music in self.get_last_musics():
            track_id = get_track_id_spotify(music, new_token)

            if track_id is not None:
                if not track_already_exist(track_id, self.__playlist, 0, new_token):
                    add_music_to_playlist(track_id, self.__playlist, new_token)
                    # else:
                # log = open("log.txt", "a")
                # log.write("Can't find the music " + music + "\n")

    def get_last_musics(self) -> dict:
        pass
