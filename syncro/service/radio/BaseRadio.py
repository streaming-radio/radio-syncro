class BaseRadio:
    def __init__(self, name, playlist, spotify):
        self.__playlist = playlist
        self.__name = name
        self.__spotify = spotify

    def execute(self):
        print(self.__name + " Is Running ..")

        for music in self.get_last_musics():
            track_id = self.__spotify.get_track_id_spotify(music[0], music[1])

            if track_id is not None:
                if not self.__spotify.track_already_exist(track_id, self.__playlist, 0):
                    self.__spotify.add_music_to_playlist(track_id, self.__playlist)
                    print(self.__name + " Add : " + music[0] + " " + music[1])
                    # else:
                # log = open("log.txt", "a")
                # log.write("Can't find the music " + music + "\n")

    def get_last_musics(self) -> dict:
        pass
