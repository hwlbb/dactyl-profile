.PHONY: help install run watch clean test test-models

help:
	@echo "可用命令:"
	@echo "make install      - 安装项目依赖"
	@echo "make install-dev  - 安装开发依赖"
	@echo "make run         - 生成键盘模型"
	@echo "make watch       - 监视文件变化并自动重新生成"
	@echo "make clean       - 清理生成的文件"
	@echo "make test        - 运行测试"
	@echo "make test-models - 生成测试模型"

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

run:
	python -m src

watch:
	python -m src --watch

clean:
	python -m src --clean

test:
	pytest

test-models:
	python tests/test_model.py