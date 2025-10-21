#!/bin/bash

# Run all tests in the src directory
echo "Running all tests..."

# Run individual test files
echo "Running TextNode tests..."
python3 test_textnode.py

echo "Running HTMLNode tests..."
python3 test_htmlnode.py

echo "Running Markdown tests..."
python3 test_markdown.py

# Also run tests from the parent directory
echo "Running markdown_to_blocks tests..."
cd ..
PYTHONPATH=src python3 test_markdown_to_blocks.py

echo "Running block_to_block_type tests..."
python3 test_block_to_block_type.py
cd src

echo "All tests completed!"