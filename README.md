# Тестовое по nlp в Сириус

## Описание решения

В файле sirius_test.ipynb приложен весь процесс обучения модели, за основу взята тинькофская. Данные брал с телеграмм-чата "Data Science Chat" (@datasciencechat).

Файл main.py содержит код телеграмм бота.

Файлы model_handler.py и database_handler.py содержат обработчики модели и базы данных соответственно. База данных нужна для сохранения контекста пользователя (Она создастся если ее нет)

Доступ к модели осуществляется через Hugging Face API, после первого запроса нужно подождать, пока модель загрузится.

## Установка 
### Через гит-репозиторий
1) Клонируйте репозиторий себе, устанавливаете нужные библиотеки c помощью команды

```
python -m pip install -r requirements.txt
```
2) Создаете файл ".env", в нем прописываете HG_TOKEN = <ВАШ ТОКЕН С HUGGING FACE> (https://huggingface.co/settings/tokens) и TG_TOKEN = <ВАШ ТОКЕН С @BotFather>
3) Запускаете main.py
### Через docker-compose
Нужен скачанный docker
1) Скачиваете docker-compose.yml
2) Прописываете в нем свой HF_TOKEN и TG_TOKEN и запускаете с помощью команды:
```
docker-compose run bot
```
3) Либо же сразу запускаете docker-compose.yml с помощью команды
```
docker-compose run -e HF_TOKEN=<ВАШ ТОКЕН> -e TG_TOKEN=<ВАШ ТОКЕН> bot
```
