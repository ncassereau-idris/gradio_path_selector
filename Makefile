.PHONY: lint
lint:
	black .
	isort .

.PHONY: build
build:
	gradio cc install
	gradio cc build --no-generate-docs

.PHONY: clean
clean:
	rm -rf dist/

.PHONY: test
test:
	echo "test"

.PHONY: install
install: build
	pip install dist/*.whl
