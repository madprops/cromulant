from .window import Window

class Game:
    @staticmethod
    def update_view() -> None:
        scene = Window.view.scene()
        scene.addRect(0, 0, 10, 10)
        scene.addRect(10, 10, 10, 10)
        scene.addRect(20, 20, 10, 10)
        scene.addRect(30, 30, 10, 10)
        scene.addRect(40, 40, 10, 10)