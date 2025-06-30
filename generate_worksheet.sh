#!/bin/bash

# Simple wrapper script for generating handwriting worksheets

# Default values
TEXT="The quick brown fox jumps over the lazy dog"
OUTPUT="handwriting_worksheet.pdf"
LINE_STYLE="dashed"
LETTER_STYLE="dashed"
VISIBLE=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --text)
            TEXT="$2"
            shift 2
            ;;
        --output)
            OUTPUT="$2"
            shift 2
            ;;
        --line-style)
            LINE_STYLE="$2"
            shift 2
            ;;
        --letter-style)
            LETTER_STYLE="$2"
            shift 2
            ;;
        --visible)
            VISIBLE=true
            shift
            ;;
        --help|-h)
            echo "Handwriting Worksheet Generator"
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --text 'TEXT'        Text to practice (default: 'The quick brown fox...')"
            echo "  --output FILE        Output filename (default: handwriting_worksheet.pdf)"
            echo "  --line-style STYLE   Guide line style: solid, dashed, dotted, minimal, none (default: dashed)"
            echo "  --letter-style STYLE Letter style: solid, dashed, outline (default: dashed)"
            echo "  --visible            Show browser window during generation"
            echo "  --help, -h           Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0 --text 'Hello World'"
            echo "  $0 --text 'Practice writing' --output my_worksheet.pdf"
            echo "  $0 --line-style solid --letter-style dashed --text 'ABC 123'"
            echo "  $0 --visible  # Watch the browser work"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

echo "🖊️  Handwriting Worksheet Generator"
echo "=================================="
echo "Text: $TEXT"
echo "Output: $OUTPUT"
echo "Line Style: $LINE_STYLE"
echo "Letter Style: $LETTER_STYLE"
echo "Mode: $([ "$VISIBLE" = true ] && echo "Visible browser" || echo "Headless")"
echo ""

# Check if Python environment is set up
if [ ! -d ".venv" ]; then
    echo "❌ Python environment not found. Please run setup first."
    exit 1
fi

# Build the Python command
PYTHON_CMD=".venv/bin/python advanced_worksheet_generator.py --text '$TEXT' --output '$OUTPUT' --line-style '$LINE_STYLE'"
if [ "$VISIBLE" = true ]; then
    PYTHON_CMD="$PYTHON_CMD --visible"
fi

echo "🚀 Starting worksheet generation..."
eval $PYTHON_CMD

if [ $? -eq 0 ] && [ -f "$OUTPUT" ]; then
    echo ""
    echo "✅ Success! Worksheet generated:"
    echo "   📄 File: $OUTPUT"
    echo "   📊 Size: $(ls -lh "$OUTPUT" | awk '{print $5}')"
    echo ""
    echo "🎯 To generate another worksheet:"
    echo "   $0 --text 'Your custom text here' --line-style dashed"
else
    echo ""
    echo "❌ Generation failed. Check the error messages above."
    echo ""
    echo "💡 Troubleshooting:"
    echo "   - Try running with --visible to see what's happening"
    echo "   - Make sure you have a stable internet connection"
    echo "   - Check that Chrome and ChromeDriver are properly installed"
fi
