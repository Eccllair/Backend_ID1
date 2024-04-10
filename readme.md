<h1 align="center"> приложение FastAPI </h1>  
<h2> Введение </h2>
Приложение разрабатывается в обучающих целях. Основной целью обучения является изучение работы FastAPI
<h3> Задачи проекта </h3>

<ol>
  <li>Настройка окружения. Зависимости. Первое web-приложение (REST API) ✔</li>
  <li>Создание API для сервера «работа с пользователями»</li>
  <li>Подключение к СУБД PostgreSQL. Роутер.<br>Операции пути, реализующие просмотр, добавление, обновление, удаление данных из таблиц БД</li>
  <li>Развёртывание приложения</li>
</ol>

<h2> Содержание проекта </h2>
Проект состоит из FastAPI приложения и 2-х docker-контейнеров с PostgreSQL
<ul>
  <br>
  <li>FastAPI приложение</li>
  Приложение включает в себя файлы кода на python, модели, чистые SQL-запросы, docker-скрипты и скрипты развертывания.<br>
  Модели и чистые SQL-запосы используются вместе для изучения взаимодействия с базой данных при помощи обоих подходов.<br>
  Модели - быстрый и удобный инструмент.<br>
  SQL-запросы могут использоваться для сложных и оптимизированных запросов к базе данных.
  <ul>
    <br>
    <h3>Структура проекта:</h3>
      <li>auth - каталог с кодом для регистрации/авторизации пользователей (в данный момент не используется)</li>
      <li>lib - каталог с пользовательскими функциями и классами</li>
      <li>models - каталог с моделями таблиц базы данных и взаимодействием с ними</li>
      <li>routers - каталог с ссылками приложения</li>
      <li>tests - каталог с unit-тестами </li>
      <li>venv - каталог виртуального окружения (генерируется скриптом)</li>
      <li>.gitignore - git файл исключений фиксаций (скрыт)</li>
      <li>config.py - файл с приватной информацией (скрыт)</li>
      <li>database.env - файл приватных данных для построения sql docker контейнеров (скрыт)</li>
      <li>database.py - файл подключения к БД</li>
      <li>docker-compose.yaml - файл конструирования контейнеров</li>
      <li>main.py - точка входа</li>
      <li>readme.md - файл описания</li>
      <li>requirements.txt - требуемые библиотеки</li>
    </ul>
  <li>idz-database-1 - Контейнер с БД</li>
  <li>idz-test_database-1 - Контейнер с БД для тестов</li>
</ul>
<h2> Развертывание проекта </h2>
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
