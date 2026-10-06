# Мобильная автоматизация PNW (Appium) — ДЗ OTUS QA-Python

Домашнее задание по модулю `mobile`: автоматизация жестов и поиск элементов
через Appium. Тест открывает главный список приложения **PNW**, пролистывает
его свайпами (W3C Actions) до пункта **«Календарь»** (`Calendar`) и кликает по
нему. Отчёт формируется с помощью **Allure**.

## Соответствие критериям задания

| Требование ДЗ | Реализация |
| --- | --- |
| Python + Appium-Python-Client | `Appium-Python-Client==6.0.7`, `Selenium==4.50.0` |
| Desired Capabilities | `config.py` → `get_capabilities()` |
| Свайпы через Touch Action / W3C Actions | `gestures.py` → `swipe()` (W3C `ActionBuilder` + `PointerInput`) |
| Цикл `while` со свайпами до появления элемента | `pages/app_list_page.py` → `find_by_swiping()` |
| Клик по найденному элементу | там же, `tap_title()` |
| Понятное исключение, если элемент не найден | `ListItemNotFoundError` |
| Отчёт о выполнении | Allure (`allure-pytest`) + логи Appium |

## Структура проекта

```
.
├── config.py                  # Desired Capabilities + настройки (через env)
├── gestures.py                # W3C-свайп (ActionBuilder / PointerInput)
├── conftest.py                # фикстура driver + прикрепление скриншота при падении
├── pytest.ini                 # конфигурация pytest (pythonpath, allure, маркеры)
├── requirements.txt
├── pages/
│   └── app_list_page.py       # Page Object списка + цикл поиска по свайпам
└── tests/
    ├── test_find_calendar.py  # E2E-тест на устройстве (маркер mobile)
    └── test_search_logic.py   # unit-тесты логики поиска (без устройства)
```

## Требования к окружению

- **Python 3.10+** (проверено на 3.14.7).
- **Node.js 18+** и **Appium 2.x** — HTTP-сервер Appium.
- **Android SDK**: `adb`, эмулятор (AVD) или реальное устройство с включённой
  отладкой по USB.
- Установленное приложение **PNW** (`com.csdroid.pkg`).

## Установка окружения

### 1. Python-зависимости

```powershell
# Windows
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
```

```bash
# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Appium-сервер и драйвер

```bash
npm install -g appium
appium driver install uiautomator2
appium            # сервер поднимется на http://127.0.0.1:4723
```

### 3. Устройство и приложение

```bash
adb devices                    # убедитесь, что устройство/эмулятор виден
adb install path\to\pnw.apk    # установите PNW
```

### 4. Allure CLI (для генерации HTML-отчёта)

```bash
npm install -g allure-commandline   # требует установленной Java
```

## Конфигурация

Все параметры читаются из переменных окружения (со значениями по умолчанию),
менять код не нужно:

| Переменная | По умолчанию | Назначение |
| --- | --- | --- |
| `APPIUM_SERVER_URL` | `http://127.0.0.1:4723` | адрес Appium-сервера |
| `PNW_APP_PACKAGE` | `com.csdroid.pkg` | package приложения PNW |
| `PNW_APP_ACTIVITY` | _(пусто)_ | activity запуска; если пусто — Appium сам определит launcher |
| `PNW_TARGET_ITEM` | `Calendar` | текст искомого пункта |
| `PNW_MAX_SWIPES` | `20` | предохранитель от бесконечного цикла |
| `ANDROID_DEVICE_NAME` | `Android Emulator` | имя устройства для capabilities |
| `ANDROID_UDID` | _(пусто)_ | серийный номер конкретного устройства |
| `PNW_NO_RESET` | `true` | не сбрасывать состояние приложения |

## Запуск тестов

```bash
# Всё: нужен запущенный Appium + устройство/эмулятор с PNW
pytest

# Только E2E-тесты, требующие устройства
pytest -m mobile

# Только unit-тесты логики поиска (без Appium и устройства)
pytest -m "not mobile"
```

Пока Appium запущен с `--log`, его консольный вывод служит «стандартным
логом Appium», как и допускает задание.

## Отчёт Allure

Результаты пишутся в `allure-results/` (см. `pytest.ini`). Просмотр:

```bash
allure serve allure-results
# или статический отчёт:
allure generate allure-results -o allure-report --clean
```

## Как работает поиск «Календаря»

`AppListPage.find_by_swiping(text)`:

1. читает заголовки (`com.csdroid.pkg:id/tv_title`), видимые на экране;
2. если искомый текст среди них — кликает по элементу и возвращает `True`;
3. если свайп не открыл ничего нового — список прокручен до конца, цикл
   останавливается и бросается `ListItemNotFoundError` с понятным текстом;
4. иначе выполняется W3C-свайп вверх (`gestures.swipe`) и шаг повторяется;
5. число свайпов ограничено `PNW_MAX_SWIPES`.

## Примечания

- Appium 2 / `uiautomator2` больше не поддерживают legacy `TouchAction`,
  поэтому жесты реализованы через W3C Actions (`ActionBuilder` +
  `PointerInput`) — это официально рекомендуемый способ.
- Если приложение не стартует автоматически, заполните `PNW_APP_ACTIVITY`
  (имя launcher-activity можно узнать в Appium Inspector).
- Unit-тесты `tests/test_search_logic.py` проверяют логику цикла
  (поиск, определение конца списка, исключение) на фейковом драйвере и
  проходят без устройства — удобно для CI.
