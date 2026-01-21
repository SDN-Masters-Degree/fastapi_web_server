class DomainError(Exception):
    pass


class NeuralModelError(DomainError):
    pass


class AudioError(DomainError):
    pass


class UserError(DomainError):
    pass
