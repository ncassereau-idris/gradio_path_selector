.PHONY: lint
lint:
	black .
	isort .

.PHONY: build
build:
	gradio cc install
	gradio cc build

.PHONY: clean
clean:
	rm -rf dist/

.PHONY: test
test:
	echo "test"
