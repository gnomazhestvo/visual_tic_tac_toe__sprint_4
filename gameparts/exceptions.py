class FieldIndexError(IndexError):
    """Исключение, срабатывающее, если выбран индекс вне поля."""

    def __init__(self, message='Введено значение за пределами игрового поля!'):
        super().__init__(message)


class CellOccupiedError(ValueError):
    """Исключение, срабатывающее, если выбранная ячейка занята."""

    def __init__(self, message='Выбранная ячейка занята. Выберите другую.'):
        super().__init__(message)