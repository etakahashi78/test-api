.PHONY: up  down db-migrate db-conn run mock-run test test-debug format lint help

up: ## Dockerコンテナ（MySQL）起動
	docker compose up -d

down: ## Dockerコンテナ（MySQL）停止
	docker compose down

db-migrate: ## DBマイグレーションを実行
	poetry run python -m test_api.migrate_db

db-conn: ## CLIでDB接続
	mysql -h127.0.0.1 -uroot invox_test_db -P3306

run: ## FastAPI起動
	poetry run uvicorn test_api.main:app --host 127.0.0.1 --reload

mock-run: ## モックサーバ起動
	poetry run python -m mock_server

test: ## pytest実行
	poetry run pytest .

test-debug: ## pytestデバッグ実行
	poetry run pytest --capture=no .

format: ## コードフォーマット
	poetry run ruff format .

lint: ## コードリント
	poetry run ruff check . --fix

help: ## ヘルプを表示
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
