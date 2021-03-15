import datetime
import requests
from dataclasses import dataclass
from typing import Optional, List
from pathlib import Path

"""
Задача:
У многих сайтов есть специальный файл robots.txt
Задача этого файла донести до "поисковых" роботов (программ, которые шерстят интернет и запоминают его состояние) указать, какие страницы можно запоминать, а какие нет.

Пример:
Disallow: /search
Allow: /search/about
Allow: /search/static
Allow: /search/howsearchworks

В данном случае инструкция Allow указывает на разрешенную для "индексации" страницу, а Disallow - на запрещенную. Остальные инструкции можно игнорировать.

Необходимо написать дописать класс RobotsTxtAnalyzer, задачка которого состоит в следующием.
Запросить файл robots.txt у указанного ресурса (например ресурс - google.com -> файл https://google.com/robots.txt)
Прочитать содержимое файла, и составить статистику - количество разрешающих и запрещающих инсрукций.
Так же стоит получить информацию из заголовков ответа, когда редактировался данный файл (заголовок ответа Last-Modified). Заголовка может не быть. Тогда оставить поле пустым.
При выходе из програмы обновленные данные сохранить в тот же файл.

Полученную информацию записать в JSON-файл, указанный пользователем.
Важно чтобы в одном JSON-файле можно было хранить статистику для нескольких файлов.
Как вариант - для каждого ресурса хранить информацию о его статистике.


Доп задачи:
 - Если указанный ресурс ранее запрашивался, не обновлять статистику, если его актуальное время изменения не изменилось с предыдущего раза
   Для этого запрос все таки придется выполнить (Last-Modified). 
 - Для "предварительного" запроса не скачивать содержимое файла, нас интересуют только заголовки (HEAD или OPTIONS)
 - Реализовать работу класса через контекстный менеджер (загрузка и сохранение данных статистики)
"""


@dataclass
class Stats:
    """
    Класс данных статистики ресурса

     - allow - количество разрешающих инстркций в файле
     - disallow - количество запрещающих инструкций инстркций в файле
     - last_modified - время последней модификации в формате unix-timestamp, может быть пустой (None) если ресурс не предоставляет такой информации
        Для того чтобы конвертировать строчку с датой в этот формат можно воспользоватся следующим кодом
        datetime.datetime.strptime("Mon, 11 Jan 2021 21:00:00 GMT", "%a, %d %b %Y %H:%M:%S %Z").timestamp()


    В класс можно добавить методы, если это необходимо
    """
    allow: int = 0
    disallow: int = 0
    last_modified: Optional[float] = None

    def __repr__(self):
        return f"Allow - {self.allow}\nDisallow - {self.disallow}\nLast-Modified - {self.last_modified}"


class RobotsTxtAnalyser:
    """
    Класс логики анализа robots.txt

    Сигнатуру существующих методов менять не стоит, но можно добавить новые, если это необходимо
    """
    registry: List["Stats"] = []

    def __init__(self, filename: str):
        self.filename = filename

    def fetch(self, resource: str) -> str:
        """
        Получить robots.txt у ресурса, вернуть его содержимое

         - resourse - имя домена, например google.com

        Обработать возможные ошибки:
         - Страница robots.txt не существует
        """

        response = requests.get(f"https://{resource}/robots.txt")

        if response.status_code != 404:
            return response.text

        return response.raise_for_status()

    def collect_stats(self, content: str) -> Stats:
        """
        Обоработать содержимое файла robots.txt, составить статистику

         - content - содержимое robots.txt (пример можно посмотреть https://google.com/robots.txt)
        """
        stats = Stats()

        response = requests.head(f"https://{resource}/robots.txt")
        if response.headers.get("Last-Modified"):
            stats.last_modified = response.headers.get("Last-Modified")
            stats.last_modified = datetime.datetime.strptime(f"{stats.last_modified}",
                                                                  "%a, %d %b %Y %H:%M:%S %Z").timestamp()

        for line in content.split("\n"):
            if line.startswith("Allow"):
                stats.allow += 1
            elif line.startswith("Disallow"):
                stats.disallow += 1

        return stats

    def analyze(self, resource: str):
        """
        Провести анализ ресурса, и обновить информацию по нему, если она уже имелась

         - resourse - имя домена, например google.com

        """

    @staticmethod
    def load(filename):
        """
        Загрузить предыдущие данные анализа ресурсов из файла
        """
        robots_analyze_file = Path(f"{filename}.txt")
        if not robots_analyze_file.exists():
            robots_analyze_file.touch()
        else:
            with robots_analyze_file.open() as f:
                data = []
                for line in f:
                    data.append(line)
        return data

    @staticmethod
    def save(self):
        """
        Сохранить обновленные данные анализа ресурсов в файл
        """
        with open(filename, "w") as f:
            f.write(self.stats)

    def __enter__(self) -> "RobotsTxtAnalyser":
        pass

    def __exit__(self, exc_type, exc_value, tb):
        pass


if __name__ == "__main__":
    filename = input("Enter filename: ")
    resource = input("Enter resource: ")

    analyzer = RobotsTxtAnalyser(filename)

    print(analyzer.collect_stats(analyzer.fetch(resource)))
    print(analyzer.load(filename))

    analyzer.analyze(resource)
    analyzer.save()

    # with RobotsTxtAnalyser(filename) as analyzer:
    #     analyzer.analyze(resource)
