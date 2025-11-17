# Упаковка приложения для macOS

Это руководство описывает процесс создания standalone .app пакета для macOS из Kivy Clock приложения.

## Содержание

1. [Требования](#требования)
2. [Метод 1: PyInstaller (Рекомендуется)](#метод-1-pyinstaller-рекомендуется)
3. [Метод 2: py2app](#метод-2-py2app)
4. [Создание DMG для распространения](#создание-dmg-для-распространения)
5. [Подписание приложения (опционально)](#подписание-приложения-опционально)
6. [Устранение неполадок](#устранение-неполадок)

---

## Требования

- macOS 10.13 (High Sierra) или новее
- Python 3.9+ установленный через официальный installer или Homebrew
- Установленные зависимости проекта

```bash
pip install -r requirements.txt
```

---

## Метод 1: PyInstaller (Рекомендуется)

PyInstaller - самый простой и надежный способ создания .app пакетов для Kivy приложений.

### Шаг 1: Установка PyInstaller

```bash
pip install pyinstaller
```

### Шаг 2: Создание spec-файла

Создайте файл `kivy-clock.spec` в корне проекта:

```python
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('clock.kv', '.'),
        ('settings.json', '.'),
        ('fonts/*.ttf', 'fonts'),
    ],
    hiddenimports=[
        'kivy.core.window.window_sdl2',
        'kivy.core.image.img_imageio',
        'kivy.core.audio.audio_sdl2',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Kivy Clock',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Kivy Clock',
)

app = BUNDLE(
    coll,
    name='Kivy Clock.app',
    icon=None,  # Добавьте путь к .icns файлу если есть: icon='icon.icns'
    bundle_identifier='com.yourname.kivy-clock',
    info_plist={
        'NSHighResolutionCapable': 'True',
        'NSPrincipalClass': 'NSApplication',
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleVersion': '1.0.0',
        'LSMinimumSystemVersion': '10.13.0',
        'NSHumanReadableCopyright': 'Copyright © 2025',
    },
)
```

### Шаг 3: Сборка приложения

```bash
pyinstaller kivy-clock.spec
```

После успешной сборки .app файл будет находиться в `dist/Kivy Clock.app`

### Шаг 4: Тестирование

```bash
open "dist/Kivy Clock.app"
```

---

## Метод 2: py2app

py2app - официальный инструмент для создания macOS приложений.

### Шаг 1: Установка py2app

```bash
pip install py2app
```

### Шаг 2: Создание setup.py

Создайте файл `setup.py` в корне проекта:

```python
"""
Setup script for creating macOS .app bundle using py2app
"""

from setuptools import setup

APP = ['main.py']
DATA_FILES = [
    ('', ['clock.kv', 'settings.json']),
    ('fonts', [
        'fonts/Roboto-Thin.ttf',
        'fonts/DSEG7Classic-Regular.ttf',
        'fonts/UbuntuMono-Regular.ttf',
        'fonts/DejaVuSansMono.ttf',
        'fonts/SourceCodePro-Regular.ttf',
        'fonts/FiraMono-Regular.ttf',
    ]),
]

OPTIONS = {
    'argv_emulation': False,
    'iconfile': None,  # Укажите путь к .icns если есть: 'icon.icns'
    'plist': {
        'CFBundleName': 'Kivy Clock',
        'CFBundleDisplayName': 'Kivy Clock',
        'CFBundleIdentifier': 'com.yourname.kivy-clock',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSHumanReadableCopyright': 'Copyright © 2025',
        'NSHighResolutionCapable': True,
        'LSMinimumSystemVersion': '10.13.0',
    },
    'packages': ['kivy'],
    'frameworks': [],
    'includes': [
        'kivy.core.window.window_sdl2',
        'kivy.core.image.img_imageio',
    ],
}

setup(
    name='Kivy Clock',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
```

### Шаг 3: Сборка

```bash
# Режим разработки (быстрая сборка для тестирования)
python setup.py py2app -A

# Продакшн режим (полная сборка)
python setup.py py2app
```

Приложение будет находиться в `dist/Kivy Clock.app`

---

## Создание DMG для распространения

DMG - стандартный формат для распространения macOS приложений.

### Вариант 1: Использование create-dmg (рекомендуется)

```bash
# Установка
brew install create-dmg

# Создание DMG
create-dmg \
  --volname "Kivy Clock" \
  --volicon "icon.icns" \
  --window-pos 200 120 \
  --window-size 800 400 \
  --icon-size 100 \
  --icon "Kivy Clock.app" 200 190 \
  --hide-extension "Kivy Clock.app" \
  --app-drop-link 600 185 \
  "Kivy-Clock-1.0.0.dmg" \
  "dist/Kivy Clock.app"
```

### Вариант 2: Ручное создание через Disk Utility

1. Откройте **Disk Utility** (Дисковая утилита)
2. **File → New Image → Blank Image**
3. Параметры:
   - Name: `Kivy-Clock-1.0.0`
   - Size: 100 MB
   - Format: Mac OS Extended (Journaled)
   - Encryption: none
   - Partitions: Single partition - GUID Partition Map
   - Image Format: read/write disk image
4. Нажмите **Create**
5. Скопируйте `Kivy Clock.app` в смонтированный образ
6. (Опционально) Создайте символическую ссылку на `/Applications`
7. Размонтируйте образ
8. Конвертируйте в compressed image:
   ```bash
   hdiutil convert "Kivy-Clock-1.0.0.dmg" \
     -format UDZO \
     -o "Kivy-Clock-1.0.0-compressed.dmg"
   ```

### Вариант 3: Простой скрипт

Создайте файл `create_dmg.sh`:

```bash
#!/bin/bash

APP_NAME="Kivy Clock"
DMG_NAME="Kivy-Clock-1.0.0"
APP_PATH="dist/${APP_NAME}.app"
DMG_DIR="dmg_temp"

# Создаем временную директорию
mkdir -p "${DMG_DIR}"

# Копируем приложение
cp -r "${APP_PATH}" "${DMG_DIR}/"

# Создаем символическую ссылку на Applications
ln -s /Applications "${DMG_DIR}/Applications"

# Создаем DMG
hdiutil create -volname "${APP_NAME}" \
  -srcfolder "${DMG_DIR}" \
  -ov -format UDZO \
  "${DMG_NAME}.dmg"

# Очистка
rm -rf "${DMG_DIR}"

echo "DMG created: ${DMG_NAME}.dmg"
```

Запуск:
```bash
chmod +x create_dmg.sh
./create_dmg.sh
```

---

## Подписание приложения (опционально)

Для распространения через интернет рекомендуется подписать приложение.

### Требования

- Apple Developer Account
- Developer ID Application certificate

### Подписание

```bash
# Подписание .app
codesign --force --deep --sign "Developer ID Application: Your Name (TEAM_ID)" \
  "dist/Kivy Clock.app"

# Проверка подписи
codesign --verify --verbose "dist/Kivy Clock.app"
spctl --assess --verbose "dist/Kivy Clock.app"

# Подписание DMG
codesign --force --sign "Developer ID Application: Your Name (TEAM_ID)" \
  "Kivy-Clock-1.0.0.dmg"
```

### Нотаризация (для macOS 10.15+)

```bash
# Загрузка на нотаризацию
xcrun notarytool submit "Kivy-Clock-1.0.0.dmg" \
  --apple-id "your-email@example.com" \
  --password "app-specific-password" \
  --team-id "TEAM_ID" \
  --wait

# Прикрепление ticket
xcrun stapler staple "Kivy-Clock-1.0.0.dmg"
```

---

## Создание иконки (.icns)

### Из PNG файла

1. Создайте PNG файл 1024x1024px (назовите `icon.png`)
2. Используйте скрипт:

```bash
#!/bin/bash

mkdir icon.iconset
sips -z 16 16     icon.png --out icon.iconset/icon_16x16.png
sips -z 32 32     icon.png --out icon.iconset/icon_16x16@2x.png
sips -z 32 32     icon.png --out icon.iconset/icon_32x32.png
sips -z 64 64     icon.png --out icon.iconset/icon_32x32@2x.png
sips -z 128 128   icon.png --out icon.iconset/icon_128x128.png
sips -z 256 256   icon.png --out icon.iconset/icon_128x128@2x.png
sips -z 256 256   icon.png --out icon.iconset/icon_256x256.png
sips -z 512 512   icon.png --out icon.iconset/icon_256x256@2x.png
sips -z 512 512   icon.png --out icon.iconset/icon_512x512.png
sips -z 1024 1024 icon.png --out icon.iconset/icon_512x512@2x.png

iconutil -c icns icon.iconset
rm -rf icon.iconset
```

После этого используйте `icon.icns` в spec-файле или setup.py

---

## Устранение неполадок

### Проблема: "App is damaged and can't be opened"

**Решение:**
```bash
# Удалите quarantine атрибут
xattr -cr "dist/Kivy Clock.app"
```

### Проблема: Шрифты не загружаются

**Решение:**
Убедитесь, что шрифты правильно включены в DATA_FILES и находятся в правильной директории внутри .app

```bash
# Проверьте содержимое .app
ls -la "dist/Kivy Clock.app/Contents/Resources/"
```

### Проблема: Приложение не запускается

**Решение:**
Запустите из терминала для просмотра ошибок:
```bash
"dist/Kivy Clock.app/Contents/MacOS/Kivy Clock"
```

### Проблема: "LSOpenURLsWithRole() failed"

**Решение:**
Это предупреждение Kivy, которое можно игнорировать. Или добавьте в Info.plist:
```xml
<key>LSUIElement</key>
<true/>
```

### Проблема: Большой размер приложения

**Решение:**
Используйте UPX для сжатия:
```bash
brew install upx
```

И убедитесь, что в spec-файле установлено `upx=True`

---

## Полный пример workflow

```bash
# 1. Установка зависимостей
pip install -r requirements.txt
pip install pyinstaller

# 2. Создание spec-файла (или используйте готовый)
# Создайте kivy-clock.spec как описано выше

# 3. Сборка приложения
pyinstaller kivy-clock.spec

# 4. Тестирование
open "dist/Kivy Clock.app"

# 5. Удаление quarantine (если нужно)
xattr -cr "dist/Kivy Clock.app"

# 6. Создание DMG
./create_dmg.sh

# 7. (Опционально) Подписание
codesign --force --deep --sign "Developer ID" "dist/Kivy Clock.app"
codesign --force --sign "Developer ID" "Kivy-Clock-1.0.0.dmg"
```

---

## Дополнительные ресурсы

- [PyInstaller Documentation](https://pyinstaller.org/)
- [py2app Documentation](https://py2app.readthedocs.io/)
- [Kivy Packaging Guide](https://kivy.org/doc/stable/guide/packaging-osx.html)
- [Apple Code Signing Guide](https://developer.apple.com/support/code-signing/)
- [create-dmg on GitHub](https://github.com/create-dmg/create-dmg)

---

## Примечания

1. **Первый запуск может быть медленным** - это нормально для PyInstaller приложений
2. **Размер приложения** - обычно 40-80 MB из-за включенного Python runtime
3. **Обновления** - для автообновлений рассмотрите использование Sparkle framework
4. **Тестирование** - всегда тестируйте на чистой системе перед распространением

---

## Лицензирование

При распространении убедитесь, что:
- Включена информация о лицензии Kivy (MIT)
- Включены лицензии на шрифты (OFL для большинства используемых шрифтов)
- Указана ваша собственная лицензия
