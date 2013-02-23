Russian Mchs open data

Website: http://www.opengovdata.ru

Создано в НП "Информационная культура"

##DESCRIPTION
Скрипты по извлечению и преобразованию данных МЧС России в открытые данные

Скрипт cbsextphone.py - извлекает всю информацию о телефонах экстренных служб по регионам и возвращает 4 CSV файла:
- phones.csv - все телефоны
- ops.csv - операторы связи
- regions.csv - список регионов
- services.csv - список сервисов

Скрипт process.py - извлекает ссылки на ежедневные сводки МЧС и загружает их MongoDB
В итоге создает CSV файл - alllinks.csv со ссылками на ежедневные отчеты

Скрипт firebranches.py - извлекает список пожарных частей из fire.mchs.gov.ru/fire_map/ и сохраняет в файл
В итоге создает CSV файл - data/branches/branches.csv со списоком и координатами частей


##REQUIREMENTS

- python 2.5+
- mechanize
- pymongo


##LIMITATIONS
Сайт МЧС регулярно меняется, требуется перепроверка работоспособности скриптов после изменений

