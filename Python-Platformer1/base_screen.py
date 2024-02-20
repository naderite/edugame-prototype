class BaseScreen:
    def __init__(self, window):
        self.window = window

    def run(self):
        raise NotImplementedError("Subclasses must implement this method.")

    def reset(self):
        pass
