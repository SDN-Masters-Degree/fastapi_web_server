class DomainError(Exception):
    def __init__(self, message):
        super().__init__(message)


class NeuralModelError(DomainError):
    def __init__(self, message):
        super().__init__(message)


class AudioError(DomainError):
    def __init__(self, message):
        super().__init__(message)


class UserError(DomainError):
    def __init__(self, message):
        super().__init__(message)
