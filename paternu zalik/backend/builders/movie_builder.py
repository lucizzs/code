from backend.models.movie import MovieSchema

class MovieBuilder:
    def __init__(self):
        self.reset()

    def reset(self):
        self._movie = {
            "movie_id": "",
            "title": "",
            "overview": "",
            "release_date": "",
            "vote_average": 0.0,
            "poster_path": None
        }

    @property
    def movie(self) -> MovieSchema:
        movie = MovieSchema(**self._movie)
        self.reset()
        return movie

    def set_movie_id(self, movie_id: str):
        self._movie["movie_id"] = movie_id
        return self

    def set_title(self, title: str):
        self._movie["title"] = title
        return self

    def set_overview(self, overview: str):
        self._movie["overview"] = overview
        return self

    def set_release_date(self, release_date: str):
        self._movie["release_date"] = release_date
        return self

    def set_vote_average(self, vote_average: float):
        self._movie["vote_average"] = vote_average
        return self

    def set_poster_path(self, poster_path: str):
        self._movie["poster_path"] = poster_path
        return self 