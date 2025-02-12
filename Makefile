.PHONY: watch
watch: run
	watchmedo shell-command --patterns="*.py" --recursive --command="python src/main.py" src

.PHONY: run
run:
	python -c "import os; os.makedirs('things', exist_ok=True)"
	python src/main.py
