import csv
from pathlib import Path

from .disciplines import Discipline
from .test_name import TestName

__all__ = ['Student']

# Список доступных дисциплин
_DISCIPLINES = ["Математика",
                "Физика",
                "Химия",
                "История",
                "Литература",
                ]


class Student:
    """Класс студент."""
    family = TestName()
    name = TestName()
    second_name = TestName()

    def __init__(self, family: str, name: str, second_name: str):
        """Инициализация экземпляра."""
        self.family = family  # фамилия
        self.name = name  # имя
        self.second_name = second_name  # отчество
        self._progress = []  # успеваемость по предметам список из Discipline
        self._load_progress()

    @property
    def progress(self):
        """Прогресс обучения делаем свойством, добавление новой дисциплины через метод append_to_progress"""
        return self._progress

    @property
    def short_name(self):
        """Свойство для получения короткого имени студента."""
        return f"{self.family} {self.name[0]}.{self.second_name[0]}."

    def __str__(self):
        """Представление экземпляра в виде строки."""
        return f'{self.family} {self.name} {self.second_name}'

    def __repr__(self):
        """Представление в виде строки генерации экземпляра класса."""
        return f'Student({self.family}, {self.name}, {self.second_name})'

    def _load_progress(self):
        """Чтение успеваемости по предметам. Если у студента нет личных данных по успеваемости - создается
        список предметов из общего списка доступных пред.
        """
        file_name = self.short_name + 'csv'
        if Path(file_name).exists():
            with open(file_name, "r", encoding="UTF-8") as file:
                csv_reader = csv.reader(file, dialect="excel", quoting=csv.QUOTE_NONNUMERIC)
                for row in csv_reader:
                    new_discipline = Discipline(row[0], int(row[1]), int(row[2]))
                    self.append_to_progress(new_discipline)

    def save_progress(self):
        """Сохранение информации об успеваемости студента."""
        file_name = self.short_name + 'csv'
        with open(file_name, "w", encoding="UTF-8") as file:
            csv_writer = csv.writer(file, dialect="excel", quoting=csv.QUOTE_NONNUMERIC)
            for discipline in self._progress:
                csv_writer.writerow([discipline.name, discipline.rate_value, discipline.test_value])

    def show_progress(self):
        """Отображение успеваемости."""
        result = "--------------------------------\n" \
                 "     Предмет    | оценка | тест \n" \
                 "--------------------------------\n"
        for discipline in self._progress:
            result += f"{discipline.name:16s}|{discipline.rate_value:8d}|{discipline.test_value:8d}\n"
        result += "--------------------------------"
        return result

    def find_discipline_in_progress(self, discipline: Discipline) -> bool:
        """Поиск дисциплины в списке успеваемости студента."""
        result = False
        for disc in self._progress:
            if discipline == disc:
                result = True
                break

        return result

    def append_to_progress(self, discipline: Discipline):
        """Добавление новой дисциплины в список успеваемости студента. Дисциплина не должна присутствовать в списке."""
        if discipline.name in _DISCIPLINES and not self.find_discipline_in_progress(discipline):
            self._progress.append(discipline)


if __name__ == '__main__':
    student_1 = Student('Иванов', 'Иван', 'Петрович')
    student_2 = Student('Сидоров', 'Николай', 'Петрович')

    print(student_1.short_name)
    print(student_2)
