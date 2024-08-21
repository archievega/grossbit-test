## How to run

Run db:
```bash
docker compose up
```
Set DB_URL:
```bash
export APP__DB__URL=postgresql+asyncpg://postgres:postgres@localhost:5432/postgres
```

```bash
cd cash_machine
```
Install dependencies:
```bash
poetry install
```
Apply migrations:
```bash
alembic upgrade head
```
Run app:
```bash
python cash_machine/main.py
```
