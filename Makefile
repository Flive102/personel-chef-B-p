# Makefile — shortcut commands cho dự án
# Chạy bằng: make <command>
.PHONY: install playground run test generate-traces grade weekly-report

# Cài tất cả dependencies và tạo lockfile
install:
	uv sync --all-extras
	uv lock

# Chạy agent trong playground (ADK interactive mode)
playground:
	agents-cli playground

# Chạy agent trực tiếp qua CLI (không qua playground)
run:
	uv run python -m mood_agent.agent

# Chạy tất cả unit tests
test:
	uv run pytest tests/unit/ -v

# Sinh eval traces (Antigravity checklist)
generate-traces:
	agents-cli eval generate \
	  --dataset tests/eval/datasets/basic-dataset.json \
	  --output artifacts/traces/

# Chấm điểm traces (Antigravity checklist)
grade:
	agents-cli eval grade \
	  --traces artifacts/traces/ \
	  --config tests/eval/eval_config.yaml

# Sinh báo cáo tuần từ SQLite (chạy sau ít nhất 1 session)
weekly-report:
	uv run python -m mood_agent.weekly_report
