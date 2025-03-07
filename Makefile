.PHONY: help install install-dev run run-legacy watch watch-legacy clean setup-new compare demo-keycap

help:
	@echo "可用命令:"
	@echo "make install      - 安装项目依赖"
	@echo "make install-dev  - 安装开发依赖"
	@echo "make setup-new    - 创建新架构的基本目录结构"
	@echo "make run          - 使用新架构生成键盘模型"
	@echo "make run-legacy   - 使用旧架构生成键盘模型"
	@echo "make watch        - 监视新架构文件变化并自动重新生成"
	@echo "make watch-legacy - 监视旧架构文件变化并自动重新生成"
	@echo "make compare      - 比较新旧架构生成的模型"
	@echo "make demo-keycap  - 生成SA键帽演示模型"
	@echo "make clean        - 清理生成的文件"

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

run:
	python -m src

run-legacy:
	python -m src_legacy

watch:
	python -m src --watch

watch-legacy:
	python -m src_legacy --watch

clean:
	python -m src_legacy --clean
	rm -rf output/new
	rm -rf output/legacy
