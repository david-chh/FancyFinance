.PHONY: dev

install:
	@echo "Installing dependencies..."
	cd langgraph-agent
	uv venv
	uv sync

dev:
	@echo "Running dev server..."
	uv run --directory langgraph-agent 



