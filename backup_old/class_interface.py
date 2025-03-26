from abc import ABC, abstractmethod

class ClassInterface(ABC):
    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def request(self,conclusion):
        pass