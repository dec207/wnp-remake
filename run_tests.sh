#!/bin/bash
echo "🧪 Running WNP Unit Tests..."
python3 -m unittest tests/test_engine.py
if [ $? -eq 0 ]; then
    echo "✅ All tests passed!"
else
    echo "❌ Tests failed!"
    exit 1
fi
