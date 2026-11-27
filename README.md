<div align="center">

# 🐋 BlueWhale

**Трекер краснокнижных морских млекопитающих**

Интерактивная карта миграционных маршрутов редких и исчезающих видов

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Google Maps](https://img.shields.io/badge/Google%20Maps-JavaScript%20API-4285F4?logo=googlemaps&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?logo=sqlite&logoColor=white)

</div>

---

## О проекте

BlueWhale — интерактивный проект, посвящённый изучению миграционных маршрутов краснокнижных морских млекопитающих. Цель — исследовать перемещения морских животных, визуализировать их пути и привлечь внимание к сохранению редких и исчезающих видов.

В основе проекта данные двух международных ресурсов:

| Ресурс | Что даёт проекту |
|---|---|
| [IUCN Red List](https://www.iucnredlist.org/) | Природоохранный статус видов и угрозы их существованию |
| [Movebank](https://www.movebank.org/cms/movebank-main) | Данные о перемещениях животных, полученные с помощью систем отслеживания |

## Как это устроено

```
База данных (виды, таксономия, описания)
              │  научное название вида
              ▼
     Запрос в Movebank API
              │  GPS-точки животных
              ▼
   Метки и маршруты на карте Google Maps
              │  клик по метке
              ▼
 Картинка, описание, ссылки на IUCN и Википедию
```

В базе данных хранится 41 вид морских млекопитающих со статусом CR, EN или VU. По научному названию вида сайт запрашивает точки из Movebank и рисует их на карте. Клик по метке открывает карточку животного.

## Как запустить сайт

### Что понадобится

- Python 3.10 или новее
- Git
- Ключ Google Maps JavaScript API ([как получить](https://developers.google.com/maps/documentation/javascript/get-api-key))
- Аккаунт на [Movebank](https://www.movebank.org/) (для запросов к данным)

### 1. Скачать проект

```bash
git clone https://github.com/ВАШ_НИК/BlueWhale.git
cd BlueWhale
```

### 2. Создать виртуальное окружение

```bash
python -m venv .venv
```

Активировать его:

```powershell
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

```bash
# Linux и macOS
source .venv/bin/activate
```

Если PowerShell ругается на запрет запуска скриптов, выполните один раз:
`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

### 3. Установить зависимости

```bash
pip install -r requirements.txt
```

### 4. Настроить секреты

Скопируйте шаблон и впишите свои данные:

```bash
# Windows (PowerShell)
Copy-Item .env.example .env

# Linux и macOS
cp .env.example .env
```

Откройте `.env` и заполните:

```
MOVEBANK_USER=ваш_логин
MOVEBANK_PASSWORD=ваш_пароль
```

Файл `.env` в Git не попадает, он добавлен в `.gitignore`.

### 5. Указать ключ Google Maps

В файле `static/index.html` найдите строку с подключением карты и замените `ТВОЙ_КЛЮЧ` на свой ключ:

```html
src="https://maps.googleapis.com/maps/api/js?key=ТВОЙ_КЛЮЧ&loading=async&callback=initMap"
```

### 6. Запустить сервер

```bash
python main.py
```

Откройте в браузере [http://localhost:8000](http://localhost:8000).

Чтобы остановить сервер, нажмите `Ctrl + C` в терминале.

## Источники данных

- [IUCN Red List](https://www.iucnredlist.org/) — статус видов
- [Movebank](https://www.movebank.org/) — данные о перемещениях животных
- [Википедия](https://www.wikipedia.org/) — описания и изображения видов