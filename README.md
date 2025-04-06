# Тестовое задание Python. Возобновляемая энергия  
Проект состоит из пяти файлов Python:  
parse.py - получает данные с FlightRadar24  
db_manager.py - подключается к базе данных PostgreSQL и совершает запросы к таблицам  
flight_report.py - собирает данные в единый csv-файл для отчёта о рейсах по времени  
dashboard.py - моделирует дашборд географической карты с отмеченными рейсами.  

Дополнительные файлы - Dockerfile, docker-compose.yml и requirements.txt; при запуске кода создаётся файл отчёта flight.csv.  

Для запуска приложения:  
Клонировать репозиторий командой `git clone https://github.com/KarinaKhachatrian/GreenAtom.git`  
Перейти в папку `GreenAtom` командой `cd GreenAtom`
Ввести в терминале команду `docker-compose up --build`  
Перейти по ссылке [http://localhost:8501](http://localhost:8501) для просмотра дашборда.  
Для загрузки может потребоваться некоторое время.  
