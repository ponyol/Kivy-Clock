# Quick Start для macOS

Быстрое руководство по запуску Kivy Clock на macOS.

## Проблема: "Unable to find Window provider"

Если вы видите эту ошибку при запуске:
```
[CRITICAL] [Window] Unable to find any valuable Window provider
ModuleNotFoundError: No module named 'pygame'
```

### Решение (выберите один из вариантов)

#### Вариант 1: Переустановка Kivy с зависимостями (Быстрый)

```bash
# Активируйте ваше виртуальное окружение (если используете)
source .venv/bin/activate

# Переустановите Kivy с полными зависимостями
pip uninstall kivy
pip install 'kivy[base]>=2.3.0'

# Запустите приложение
python3 main.py
```

#### Вариант 2: Использование Python 3.11 (Рекомендуется для Python 3.14+)

```bash
# Установите Python 3.11 через Homebrew
brew install python@3.11

# Создайте новое виртуальное окружение
python3.11 -m venv .venv

# Активируйте окружение
source .venv/bin/activate

# Установите зависимости
pip install -r requirements.txt

# Запустите приложение
python3 main.py
```

#### Вариант 3: Использование существующего requirements.txt

```bash
# Активируйте ваше виртуальное окружение
source .venv/bin/activate

# Переустановите все зависимости
pip install --upgrade --force-reinstall -r requirements.txt

# Запустите приложение
python3 main.py
```

## Проверка установки

После установки проверьте, что Kivy установлен правильно:

```bash
python3 -c "import kivy; print(f'Kivy {kivy.__version__} установлен')"
```

Вы должны увидеть:
```
Kivy 2.3.1 установлен
```

## Частые проблемы

### Python 3.14
- **Проблема:** Python 3.14 слишком новый, некоторые зависимости Kivy еще не совместимы
- **Решение:** Используйте Python 3.11-3.13

### Виртуальное окружение
- **Всегда активируйте** виртуальное окружение перед установкой пакетов
- Проверка: `which python3` должен показывать путь с `.venv`

### Homebrew Python
- Если используете Python из Homebrew, используйте `python3.11` вместо `python3`
- Пример: `python3.11 main.py`

## Полная последовательность действий

```bash
# 1. Клонировать репозиторий
git clone <url>
cd Kivy-Clock

# 2. Установить Python 3.11 (если нужно)
brew install python@3.11

# 3. Создать виртуальное окружение
python3.11 -m venv .venv

# 4. Активировать окружение
source .venv/bin/activate

# 5. Установить зависимости
pip install -r requirements.txt

# 6. (Опционально) Скачать шрифты, если их нет
python3 download_fonts.py

# 7. Запустить приложение
python3 main.py
```

## Управление приложением

- **F1** - Открыть настройки
- **ESC** - Выход из приложения

## Дополнительная помощь

- Полная документация: [README.md](README.md)
- Упаковка для macOS: [MACOS_PACKAGING.md](MACOS_PACKAGING.md)
