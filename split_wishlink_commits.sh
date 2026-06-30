#!/usr/bin/env bash
set -e

echo "=== Wishlink: разбиение проекта на смысловые Git-коммиты ==="

if [ ! -f "manage.py" ]; then
  echo "Ошибка: запусти скрипт из корня проекта, где лежит manage.py"
  exit 1
fi

echo
echo "ВНИМАНИЕ: скрипт пересоздаст Git-историю в этой папке."
echo "Код проекта не удаляется, удаляется только папка .git."
read -p "Продолжить? [y/N]: " answer

if [ "$answer" != "y" ] && [ "$answer" != "Y" ]; then
  echo "Отменено."
  exit 0
fi

rm -rf .git
git init
git branch -M main

git config user.name "Грызунов Артем"
git config user.email "artem.gryzunow@gmail.com"

cat > .gitignore <<'EOF'
.venv/
.idea/
__pycache__/
*.pyc
*.pyo
*.pyd
.env
db.sqlite3
media/
*.log
.DS_Store
.vscode/
EOF

cat > .env.example <<'EOF'
SECRET_KEY=dev-secret-key
DEBUG=True

POSTGRES_DB=wishlink
POSTGRES_USER=wishlink_user
POSTGRES_PASSWORD=wishlink_password
POSTGRES_HOST=db
POSTGRES_PORT=5432
EOF

commit_group() {
  message="$1"
  shift

  git add --ignore-errors "$@" 2>/dev/null || true

  if git diff --cached --quiet; then
    echo "Пропуск: $message"
  else
    git commit -m "$message"
  fi
}

echo
echo "=== 1. Базовые файлы проекта ==="
commit_group "Добавлены базовые файлы проекта" \
  .gitignore .env.example manage.py requirements.txt

echo
echo "=== 2. Настройки Django-проекта ==="
commit_group "Создана базовая конфигурация Django-проекта" \
  wishlist/__init__.py \
  wishlist/asgi.py \
  wishlist/wsgi.py \
  wishlist/settings.py \
  wishlist/urls.py

echo
echo "=== 3. Создание приложений проекта ==="
commit_group "Созданы приложения users social wishlists" \
  users/__init__.py users/apps.py users/views.py users/admin.py \
  social/__init__.py social/apps.py social/views.py social/admin.py \
  wishlists/__init__.py wishlists/apps.py wishlists/views.py wishlists/admin.py

echo
echo "=== 4. Пользователь и профиль ==="
commit_group "Добавлена кастомная модель пользователя и профиль" \
  users/models.py \
  users/signals.py \
  users/apps.py \
  users/admin.py

echo
echo "=== 5. Социальные связи ==="
commit_group "Добавлены модели заявок в друзья и отношений" \
  social/models.py \
  social/admin.py

echo
echo "=== 6. Вишлисты и предметы ==="
commit_group "Добавлены модели вишлистов, предметов и ручного доступа" \
  wishlists/models.py \
  wishlists/admin.py

echo
echo "=== 7. Миграции моделей ==="
commit_group "Добавлены миграции базы данных" \
  users/migrations \
  social/migrations \
  wishlists/migrations

echo
echo "=== 8. Формы пользователей ==="
commit_group "Добавлена форма регистрации пользователя" \
  users/forms.py \
  users/views.py

echo
echo "=== 9. Формы вишлистов ==="
commit_group "Добавлены формы для вишлистов и предметов" \
  wishlists/forms.py

echo
echo "=== 10. Логика приватности ==="
commit_group "Реализована проверка доступа к вишлистам" \
  wishlists/services.py

echo
echo "=== 11. Представления вишлистов ==="
commit_group "Добавлены представления для списка, создания и просмотра вишлистов" \
  wishlists/views.py

echo
echo "=== 12. URL-маршруты ==="
commit_group "Настроены маршруты авторизации и вишлистов" \
  wishlist/urls.py

echo
echo "=== 13. Базовый шаблон ==="
commit_group "Добавлен базовый HTML-шаблон проекта" \
  templates/base.html

echo
echo "=== 14. Шаблоны авторизации и профиля ==="
commit_group "Добавлены шаблоны регистрации, входа и профиля" \
  templates/users

echo
echo "=== 15. Шаблоны вишлистов ==="
commit_group "Добавлены шаблоны страниц вишлистов и предметов" \
  templates/wishlists

echo
echo "=== 16. Стили интерфейса ==="
commit_group "Добавлены CSS-стили пользовательского интерфейса" \
  static/css

echo
echo "=== 17. Dockerfile ==="
commit_group "Добавлен Dockerfile для запуска Django-приложения" \
  Dockerfile

echo
echo "=== 18. Docker Compose ==="
commit_group "Добавлена конфигурация Docker Compose с PostgreSQL" \
  docker-compose.yml

echo
echo "=== 19. Настройка PostgreSQL ==="
commit_group "Настроено подключение Django к PostgreSQL" \
  wishlist/settings.py \
  requirements.txt \
  .env.example

echo
echo "=== 20. Документация проекта ==="
commit_group "Добавлена документация проекта" \
  README.md

echo
echo "=== 21. Остальные файлы проекта ==="
git add .
if git diff --cached --quiet; then
  echo "Остальных файлов для коммита нет."
else
  git commit -m "Добавлены дополнительные файлы проекта"
fi

echo
echo "=== Готовая история коммитов ==="
git log --oneline --decorate --graph

echo
echo "Теперь создай пустой репозиторий на GitHub с названием wishlink."
echo "Потом выполни:"
echo
echo "git remote add origin https://github.com/USERNAME/wishlink.git"
echo "git push -u origin main"
echo
echo "Вместо USERNAME подставь свой GitHub-логин."
