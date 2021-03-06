import abc

import sqlite3
import redis


class Idea:
    def __init__(self):
        self.idea_id = None
        self.title = None
        self.description = None
        self.rating = None
        self.votes = None
        self.email = None

    def add_rating(self, rating: float):
        self.rating += float(rating)

    def __str__(self):
        return 'Idea(idea_id={}, title={}, rating={})'.format(self.idea_id, self.title, self.rating)


class IdeaRepository(abc.ABC):

    @abc.abstractmethod
    def find_by_id(self, idea_id: str):
        pass

    @abc.abstractmethod
    def update(self, idea: Idea):
        pass


class Sqlite3IdeaRepository(IdeaRepository):

    def __init__(self, db_path):
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()

    def find_by_id(self, idea_id: str):
        # finding the idea in the database
        sql = 'SELECT * from Ideas where IdeaId = ?'
        row = self.cursor.execute(sql, idea_id).fetchone()
        if not row:
            raise ValueError('Idea does not exist')

        # Building the Idea from database
        idea_id, title, description, rating, votes, email = row
        idea = Idea()
        idea.idea_id = idea_id
        idea.title = title
        idea.description = description
        idea.rating = rating
        idea.votes = votes
        idea.email = email

        return idea

    def update(self, idea: Idea):
        update_statement = "UPDATE Ideas SET Rating='{}' WHERE IdeaId='{}'"
        self.cursor.execute(update_statement.format(idea.rating, idea.idea_id))
        self.connection.commit()


class RedisIdeaRepository(IdeaRepository):

    def __init__(self):
        self.client = redis.Redis(host='localhost', port=6379, db=0)

    def find_by_id(self, idea_id: str):
        title = self.client.hmget(idea_id, 'title')[0].decode()
        description = self.client.hmget(idea_id, 'description')[0].decode()
        rating = float(self.client.hmget(idea_id, 'rating')[0])
        votes = float(self.client.hmget(idea_id, 'votes')[0])
        email = self.client.hmget(idea_id, 'email')[0].decode()

        idea = Idea()
        idea.idea_id = idea_id
        idea.title = title
        idea.description = description
        idea.rating = rating
        idea.votes = votes
        idea.email = email

        return idea

    def update(self, idea: Idea):
        idea_id = idea.idea_id

        idea_dict = dict(
            idea_id=idea.idea_id,
            title=idea.title,
            description=idea.description,
            rating=idea.rating,
            votes=idea.votes,
            email=idea.email
        )

        self.client.hmset(idea_id, idea_dict)


class IdeaController:

    def __init__(self, request: dict):
        self.request = request

    def rate_action(self):
        idea_id = self.request.get('id')
        new_rating = self.request.get('rating')

        # repository = Sqlite3IdeaRepository('../db.sqlite3')
        repository = RedisIdeaRepository()

        use_case = RateIdeaUseCase(repository)
        input_data = RateIdeaRequest(idea_id, new_rating)
        idea = use_case.execute(input_data)

        return RateIdeaResponse(idea)


class RateIdeaRequest:

    def __init__(self, idea_id, rating):
        self.idea_id = idea_id
        self.rating = rating


class RateIdeaResponse:

    def __init__(self, idea):
        self.idea = idea


class RateIdeaUseCase:

    def __init__(self, idea_repository: IdeaRepository):
        self.idea_repository = idea_repository

    def execute(self, request: RateIdeaRequest) -> Idea:
        # find idea
        try:
            idea = self.idea_repository.find_by_id(request.idea_id)
        except Exception:
            raise RepositoryNotAvailableException()

        if not idea:
            raise IdeaDoesNotExistException()

        # add user rating
        # save rating to repository
        try:
            idea.add_rating(request.rating)
            self.idea_repository.update(idea)
        except Exception:
            raise RepositoryNotAvailableException('Update is not work')

        return idea


class RepositoryNotAvailableException(Exception):
    pass


class IdeaDoesNotExistException(Exception):
    pass


if __name__ == '__main__':
    request = {
        'id': '1',
        'rating': 4
    }

    controller = IdeaController(request)
    result = controller.rate_action()

    print(result.idea)
