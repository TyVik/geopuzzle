from maps.factories import GameFactory


class QuizFactory(GameFactory):
    class Meta:
        model = 'quiz.Quiz'
