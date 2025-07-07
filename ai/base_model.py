from abc import ABC, abstractmethod

class AIBaseModel(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def generate(self, *args, **kwargs):
        pass