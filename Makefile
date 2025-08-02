.PHONY: install run test clean

# Install dependencies
install:
	pip install -e .

# Run the ETSM platform
run:
	streamlit run src/dashboard.py

# Run tests
test:
	python -m pytest tests/ -v

# Clean up
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +

# Install development dependencies
install-dev:
	pip install -e .[dev]

# Format code
format:
	black src/ tests/

# Lint code
lint:
	flake8 src/ tests/

# Full development setup
setup: install-dev format lint test 