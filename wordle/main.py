import os
from app.views.main_view import MainView
from app.controllers.game_controller import GameController


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    words_path = os.path.join(base_dir, "app", "assets", "words.txt")

    controller = GameController(words_path)
    view = MainView(controller)
    view.run()


if __name__ == "__main__":
    main()
