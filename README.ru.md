# Мои скиллы для Claude Code

Коллекция кастомных скиллов, хуков и гайдов по настройке [Claude Code](https://docs.anthropic.com/en/docs/claude-code).

## Кастомные скиллы

### [screenshot](./screenshot/)

Монитор буфера обмена — автоматически сохраняет скриншоты и делает их доступными через команду `/screenshot`.

**Как работает:**
- Фоновый демон следит за буфером обмена (каждую секунду)
- Когда появляется новое изображение — сохраняет в `~/Screenshots` как PNG
- Claude Code читает и описывает скриншоты по запросу

**Быстрая установка:**
```bash
brew install pngpaste
cd screenshot && bash scripts/install.sh
```

Подробнее в [screenshot/README.md](./screenshot/README.md).

### [analyze-patterns](./analyze-patterns/)

Анализ транскриптов сессий Claude Code — находит повторяющиеся паттерны поведения: коррекции, частые инструменты, брошенные задачи и случаи, когда Claude сопротивляется инструкциям.

**Как работает:**
- Python-скрипт извлекает сообщения пользователя из `~/.claude/projects/*.jsonl`
- Claude анализирует их на 4 типа паттернов
- Показывает цитаты-доказательства и предлагает конкретные действия
- Опционально создаёт GitHub Issues для каждого найденного паттерна

**Быстрая установка:**
```bash
mkdir -p ~/.claude/skills/analyze-patterns/scripts
cp analyze-patterns/SKILL.md ~/.claude/skills/analyze-patterns/SKILL.md
cp analyze-patterns/scripts/pattern-detector.py ~/.claude/skills/analyze-patterns/scripts/
```

Подробнее в [analyze-patterns/README.md](./analyze-patterns/README.md).

### [remote-control](./remote-control/)

Подключайся к терминальной сессии Claude Code с телефона или любого устройства. Запусти задачу на ноутбуке — продолжи с дивана.

- Запусти `claude rc` в отдельном терминале → получишь ссылку + QR-код
- Открой ссылку на телефоне (веб или Claude iOS app)
- Нужна подписка **Max** (Pro — скоро)

Подробнее в [remote-control/README.md](./remote-control/README.md).

## Хуки и автоматизация

### [github-issues-memory](./github-issues-memory/)

GitHub Issues + Projects как постоянная память агента. Агент сам создаёт, обновляет и закрывает issues — контекст не теряется между сессиями.

- **SessionStart hook** — загружает открытые issues при старте сессии
- **PostToolUse hook** — напоминает обновить issues после `git push`
- **Rule-файл** — объясняет агенту воркфлоу

По мотивам статей [Sereja Ris](https://sereja.tech/blog/github-projects-ai-agent-memory/).

## Гайды по настройке

### [multi-account-sync](./multi-account-sync/)

Синхронизация конфига Claude Code (скиллы, правила, настройки) между несколькими учётками macOS на одной машине через `/Users/Shared/` и symlinks. Git не нужен для синхронизации на одном компьютере.

По мотивам [статьи о синхронизации](https://sereja.tech/blog/sync-claude-code-four-machines/) Sereja Ris.

### Подход "Правка → Правило"

Вместо того чтобы чинить одну и ту же ошибку дважды — записываем правило в `~/.claude/rules/`, чтобы агент больше её не повторял. Правила загружаются автоматически каждую сессию, можно фильтровать по путям файлов.

По мотивам [статьи](https://sereja.tech/blog/fix-once-rule-forever/) Sereja Ris.

## Советы

### `lfg` — запуск Claude Code в автономном режиме

Shell-алиас для запуска Claude Code с `--dangerously-skip-permissions` (без подтверждений). Идея от [Sereja Ris](https://github.com/serejaris/ris-claude-code).

Добавь в `~/.zshrc`:

```bash
alias lfg="claude --dangerously-skip-permissions"
```

> **Внимание:** Пропускает все запросы на подтверждение. Используй только в доверенном окружении.

## Сторонние скиллы

| Скилл | Автор | Описание |
|-------|-------|---------|
| [superpowers](https://github.com/obra/superpowers) | Jesse Vincent | TDD, отладка, брейнсторминг, код-ревью, планирование |
| [data](https://github.com/anthropics/claude-code/tree/main/plugins) | Anthropic | SQL, визуализация данных, дашборды, статистика |
| [skill-creator](https://github.com/anthropics/skills) | Anthropic | Мета-скилл для создания, валидации и упаковки новых скиллов |
| [frontend-design](https://github.com/anthropics/claude-code/tree/main/plugins/frontend-design) | Anthropic | Продакшн-качество фронтенд UI с авторским дизайном |
| [developing-with-streamlit](https://github.com/streamlit/agent-skills) | Streamlit | Streamlit-приложения — дизайн, производительность, лейауты, данные |
| [frontend-slides](https://github.com/zarazhangrui/frontend-slides) | zarazhangrui | HTML-презентации с анимациями, конвертация из PPT |
| [macos-fixer](https://github.com/serejaris/ris-claude-code) | Sereja Ris | Диагностика памяти macOS, траблшутинг производительности |
| [git-workflow-manager](https://github.com/serejaris/ris-claude-code) | Sereja Ris | Conventional commits, семантическое версионирование, changelogs |

## Полезное чтение

Статьи, которые повлияли на этот сетап:

- [GitHub Projects как память для AI-агента](https://sereja.tech/blog/github-projects-ai-agent-memory/) — Sereja Ris
- [Хуки Claude Code: агент сам ведёт задачи](https://sereja.tech/blog/claude-code-hooks-github-issues/) — Sereja Ris
- [Как я синхронизирую Claude Code на четырёх компах](https://sereja.tech/blog/sync-claude-code-four-machines/) — Sereja Ris
- [Правка → Правило: как научить агента не повторять ошибки](https://sereja.tech/blog/fix-once-rule-forever/) — Sereja Ris
- [Модульные правила: как не утонуть в CLAUDE.md](https://sereja.tech/blog/modular-rules-claude-md/) — Sereja Ris
- [Claude Code получил память между сессиями](https://sereja.tech/blog/claude-code-auto-memory/) — Sereja Ris

## Лицензия

MIT
