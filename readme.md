<h1 align="center"> приложение FastAPI </h1>  
<h2> Введение </h2>
Приложение разрабатывается в обучающих целях. Основной целью обучения является изучение работы FastAPI <br>
<b>Предметная область:</b> база данных для чата и API для взаимодействия с базой. <br>
<br>
<i><small>Web сокета не будет. Неа.</small></i>
<h3> Задачи проекта </h3>

<ol>
  <li>Настройка окружения. Зависимости. Первое web-приложение (REST API) ✔</li>
  <li>Создание API для сервера «работа с пользователями» ✔</li>
  <li>Подключение к СУБД PostgreSQL. Роутер.<br>Операции пути, реализующие просмотр, добавление, обновление, удаление данных из таблиц БД ✔</li>
  <li>Развёртывание приложения ✔</li>
  <li>Контеризация с помощью docker ✔</li>
  <li>Контроль версий при помощи git ✔</li>
  <li>Создание docker-compose файла ✔</li>
  <li>Добавление тестов для API</li>
  <li>Добавление миграций alembic</li>
  <li>Фоновые задачи. Безопасность и Middleware</li>
  <li>Работа с HTTP ответами ✔</li>
  <li>Развертывание приложения на удаленном сервере</li>
  <li>Работа с шаблонами, базами данных, прокси-серверами (Создать API для управления пользователями)</li>
</ol>

<h2> Содержание проекта </h2>
Проект состоит из FastAPI приложения и 2-х docker-контейнеров с PostgreSQL.<br>
Проект основывается на языке python. А так же малой доли batch файлов: docker-скриптов и скриптов развертывания.
<ul>
  <br>
  <li>FastAPI приложение</li>
  Приложение включает в себя саму библиотек FastAPI, библиотеку взаимодействия с базой данный SQLAlchemy на основе ORM и библиотеку миграций alembic<br>
  <ul>
    <br>
    <h3>Структура проекта:</h3>
      <li>auth - каталог с кодом для регистрации/авторизации пользователей (в данный момент не используется)</li>
      <li>lib - каталог с пользовательскими функциями и классами</li>
      <li>scripts - каталог batch файлов</li>
      <li>tests - каталог с unit-тестами</li>
      <li>venv - каталог виртуального окружения (генерируется скриптом)</li>
      <li>.gitignore - git файл исключений фиксаций <i>(скрыт)</i></li>
      <li>config.py - файл с приватной информацией <i>(скрыт)</i></li>
      <li>database.env - файл приватных данных для построения sql docker контейнеров <i>(скрыт)</i></li>
      <li>database.py - файл подключения к БД и общих функций взаимодействия с бд</li>
      <li>docker-compose.yaml - файл конструирования контейнеров</li>
      <li>init_database.py - файл построения бд</li>
      <li>main.py - точка входа</li>
      <li>models.py - модели таблиц базы данных</li>
      <li>readme.md - файл описания</li>
      <li>requirements.txt - требуемые библиотеки</li>
      <li>routers.py - роутеры приложения. (модели поведения при fetch запросах)</li>
    </ul>
  <li>idz-database-1 - Docker контейнер с БД</li>
  <li>idz-test_database-1 - Docker контейнер с БД для тестов</li>
</ul>
<h2> Развертывание проекта </h2>
<i>на момент написания readme 28.04.2024 развертывание приложения на linux не протестировано</i><br>
Перейдите в каталог расположения проекта<br>
Linux:<br>
  &nbsp;&nbsp;&nbsp;&nbsp;<code>cd /usr/local/back-fastapi</code><br>
Windows:<br>
  &nbsp;&nbsp;&nbsp;&nbsp;<code>C:</code><br>
  &nbsp;&nbsp;&nbsp;&nbsp;<code>cd C:\back-fastapi</code><br>
  <br>
Клонируйте репозиторий<br>
Linux/Windows:<br>
  &nbsp;&nbsp;&nbsp;&nbsp;<code>git clone https://github.com/Eccllair/Backend_fastapi.git</code><br>
<br>
Добавьте файлы окружения в корень каталога<br>
config.py<br>
<code>  POSTGRES_USER='username'
  POSTGRES_PASSWORD='password'
  POSTGRES_SERVER='localhost'
  POSTGRES_TEST_SERVER='localhost'
  POSTGRES_DB='dbname'
</code>
<br>
database.env<br>
<code>  POSTGRES_USER=username
  POSTGRES_PASSWORD=password
  POSTGRES_DB=dbname
</code>
<br>
Запустите скрипт развертывания <br>
<b>Важно! При развертывании должен быть открыт корневой каталог проекта</b><br>
Windows:<br>
  &nbsp;&nbsp;&nbsp;&nbsp;<code>scripts/build.cmd </code><br>
Linux:<br>
  &nbsp;&nbsp;&nbsp;&nbsp;<code>scripts/build</code><br>

<h2> Запуск проекта </h2>
<h3> Запуск проекта локально </h3>
Перейдите в корневой каталог приложения:<br>
<code> cd ... </code><br>
<br>
Активируйте виртуальное окружение, если оно не было активировано:<br>
Windows:<br>
<code>.\venv\Scripts\activate.bat</code><br>
Linux:<br>
<code>source venv/bin/activate</code><br>
<br>
Запустите приложение:<br>
Windows/Linux:<br>
<code>uvicorn main:app</code><br>
<br>
или<br>
<h3> Запуск проекта на Docker </h3>
Перейдите в корневой каталог приложения:<br>
<code> cd ... </code><br>
Запустите скрипт развертывания:<br>
Windows:<br>
<code>build-on-docker.cmd</code><br>

после запуска swagger будет доступен по аддресу http://127.0.0.1:8000/docs
