Этот проект включает в себя создание и управление различными компонентами с использованием Makefile.
<br>
Использвание:
<li>Запуск `make build_all`</li>
<li>Остановка `make destoroy_all`</li>
<br>
Даг `etl` отвечает за репликацию данных из Postgres в MySQL.
<br>
Создана аналитическая витрина в MySQL: db.data_mart, с помощью которой в разрезе пользователей считаются средние значения: количество, цена, сумма.