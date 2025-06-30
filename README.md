# Handwriting Practice Worksheet Generator

This project provides a working solution to generate handwriting practice worksheets from WorksheetWorks.com using automated browser interaction.

## 📋 Files Overview

| File | Description |
|------|-------------|
| `generate_worksheet.sh` | **Main script** - Easy-to-use wrapper |
| `advanced_worksheet_generator.py` | Core generator using Selenium |
| `handwriting_worksheet.pdf` | Sample generated worksheet |
| `prompt.md` | AI agent instructions for story generation |
| `README.md` | This documentation file |

## 🚀 Quick Start

### 1. Install Dependencies
```bash
# Install Python packages
pip install selenium requests

# Install ChromeDriver (macOS with Homebrew)
brew install chromedriver

# Or install ChromeDriver manually from:
# https://chromedriver.chromium.org/
```

## � Requirements

- **Python 3.6+** with `selenium` and `requests` packages
- **Google Chrome** browser installed
- **ChromeDriver** installed and in PATH
- Internet connection


## � Story Generation for Kids

For creating engaging handwriting practice with custom stories:

### Using AI to Generate Stories
```bash
# 1. Ask an AI agent to follow the instructions in prompt.md
# 2. The AI will generate a 300-word story for a 7-year-old
# 3. The AI will create a worksheet PDF with the story

# Example workflow:
# - AI generates: "Tommy found a lost puppy in the park..."
# - AI runs: ./generate_worksheet.sh --text "STORY_HERE" --output "story_practice.pdf"
# - Result: Custom handwriting practice with an engaging story
```

### Benefits of Story-Based Practice
- ✅ **More engaging** than repetitive phrases
- ✅ **Age-appropriate content** (7-year-old level)
- ✅ **300 words** = perfect length for handwriting practice
- ✅ **Custom stories** keep practice sessions fresh and interesting

See `prompt.md` for detailed instructions on story generation.

## �🔧 Advanced Usage

### Use the Python script directly:
```bash
python advanced_worksheet_generator.py --text "Custom text" --output worksheet.pdf
python advanced_worksheet_generator.py --line-style dashed --visible  # Watch browser
python advanced_worksheet_generator.py --line-style solid --text "Solid lines"
```

### Command line options:
```bash
./generate_worksheet.sh --help
```

## 📝 What the Generated PDFs Contain

The worksheets include:
- ✅ Handwriting practice lines with proper spacing
- ✅ Your custom text in print handwriting format
- ✅ **Configurable guide line styles**: solid, dashed, dotted, minimal, or none
- ✅ Professional formatting suitable for practice

### Available Line Styles:
- **`dashed`** (default): Dashed guide lines for better letter formation
- **`solid`**: Traditional solid guide lines
- **`dotted`**: Dotted guide lines for lighter guidance  
- **`minimal`**: Only top line for basic guidance
- **`none`**: No guide lines (just practice text)

## 🛠️ Technical Details

### Why This Solution Works:
1. **Real Browser**: Uses Chrome to properly execute JavaScript
2. **Form Interaction**: Fills out forms exactly like a human would
3. **PDF Detection**: Monitors for actual PDF downloads
4. **Error Handling**: Multiple fallback methods for PDF capture

### Browser Automation Flow:
1. Open WorksheetWorks.com handwriting practice page
2. Wait for Angular app to load
3. Find and fill the text input field
4. Click the "Create Worksheet" button
5. Monitor for PDF download/generation
6. Save the PDF with the specified filename

## 🔍 Comparison: curl vs Automated Browser

| Method | Result | Why |
|--------|--------|-----|
| `curl` | ❌ Returns HTML | JavaScript required |
| **Selenium** | ✅ **Valid PDF** | **Full browser interaction** |

## 🚨 Troubleshooting

### If generation fails:
1. **Run with `--visible`** to see what's happening:
   ```bash
   ./generate_worksheet.sh --visible
   ```

2. **Check dependencies**:
   ```bash
   # Verify Python packages
   python3 -c "import selenium, requests; print('✓ Python packages OK')"
   
   # Verify ChromeDriver
   chromedriver --version
   
   # Verify Chrome browser
   /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version
   ```

3. **Common issues**:
   - Chrome not installed → Install Google Chrome
   - ChromeDriver outdated → Run `brew upgrade chromedriver`
   - Network issues → Check internet connection

### Debug files created:
- `debug_screenshot_advanced.png` - Visual state of the page
- `debug_page_source.html` - HTML source for analysis

## 📊 Success Rate

✅ **Working solution tested with:**
- Default text: "The quick brown fox jumps over the lazy dog"
- Custom text: "ABC abc 123"
- Various lengths and content types

## 🎉 Example Output

Successfully generated worksheets:
- `handwriting_worksheet.pdf` (15.9 KB) ✅
- `test_abc.pdf` (14 KB) ✅

## 💡 Why curl Commands Don't Work

The original analysis showed that WorksheetWorks.com:
- Uses Angular/JavaScript for form processing
- Requires client-side interaction
- Returns HTML pages instead of PDFs for direct HTTP requests
- Needs proper session management

**Bottom line**: You need a real browser to interact with this site properly, which is exactly what our Selenium solution provides.

---

## 🏆 Final Result

**Problem**: "Create a curl command to perform click on the createworksheet button"

**Solution**: While curl alone cannot work with this JavaScript-heavy site, we've created a fully automated browser solution that successfully generates valid handwriting practice PDF worksheets.

**Usage**: Simply run `./generate_worksheet.sh --text "Your text here"` and get a professional handwriting practice worksheet!
