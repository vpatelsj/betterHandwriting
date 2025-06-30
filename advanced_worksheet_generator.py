#!/usr/bin/env python3

"""
Advanced Selenium-based worksheet generator for WorksheetWorks.com
Handles complex PDF generation scenarios including redirects and pop-ups.
"""

import time
import os
import sys
import argparse
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def setup_driver(headless=True, download_dir=None):
    """Setup Chrome driver with appropriate options"""
    if download_dir is None:
        download_dir = os.getcwd()
    
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    # Enable download preferences
    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
        "plugins.always_open_pdf_externally": True,
        "plugins.plugins_disabled": ["Chrome PDF Viewer"]
    }
    chrome_options.add_experimental_option("prefs", prefs)
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        return driver
    except Exception as e:
        print(f"Error setting up Chrome driver: {e}")
        print("Make sure ChromeDriver is installed and in your PATH")
        sys.exit(1)

def wait_for_pdf_download(download_dir, initial_files, timeout=30):
    """Wait for a PDF file to be downloaded"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        current_files = set(os.listdir(download_dir))
        new_files = current_files - initial_files
        
        # Check for PDF files
        pdf_files = [f for f in new_files if f.endswith('.pdf')]
        if pdf_files:
            # Wait a bit more to ensure download is complete
            time.sleep(2)
            return pdf_files[0]
        
        # Check for partial downloads
        partial_files = [f for f in new_files if f.endswith('.crdownload')]
        if partial_files:
            print("Download in progress...")
        
        time.sleep(1)
    
    return None

def generate_worksheet_advanced(text="The quick brown fox jumps over the lazy dog", 
                               output_file="handwriting_worksheet.pdf",
                               line_style="dashed",
                               letter_style="dashed",
                               headless=True):
    """Advanced worksheet generation with better PDF handling"""
    
    download_dir = os.path.abspath(os.getcwd())
    driver = setup_driver(headless, download_dir)
    
    try:
        print("Navigating to worksheet generator...")
        driver.get("https://www.worksheetworks.com/english/writing/handwriting/print-practice.html")
        
        # Wait for page to load
        print("Waiting for page to load...")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Give Angular app time to initialize
        time.sleep(8)
        
        print("Looking for form elements...")
        
        # Record initial files for download detection
        initial_files = set(os.listdir(download_dir))
        
        # Find and fill the text input
        text_input = None
        try:
            # Wait for textarea to be present and visible
            text_input = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.TAG_NAME, "textarea"))
            )
            print("Found text input")
        except:
            print("Could not find textarea, trying alternative selectors...")
            alternative_selectors = [
                (By.NAME, "text"),
                (By.ID, "text"),
                (By.CSS_SELECTOR, "input[type='text']"),
                (By.CSS_SELECTOR, ".form-control")
            ]
            
            for by_method, selector in alternative_selectors:
                try:
                    text_input = driver.find_element(by_method, selector)
                    break
                except:
                    continue
        
        if text_input:
            print(f"Entering text: {text}")
            text_input.clear()
            text_input.send_keys(text)
            time.sleep(1)
        else:
            print("WARNING: Could not find text input field")
        
        # Try to set other form options if available
        try:
            # Line height
            line_height_select = driver.find_element(By.NAME, "lineHeight")
            Select(line_height_select).select_by_value("0.5")
            print("Set line height to 0.5 inches")
        except:
            pass
        
        try:
            # Set guide lines based on line_style parameter
            print(f"Setting guide lines to {line_style} style...")
            
            # Different patterns for guide lines based on the website's options
            guide_patterns = {
                "solid": "1111",      # All solid lines
                "dashed": "1010",     # Alternating dashed pattern
                "dotted": "0101",     # Dotted pattern
                "minimal": "1000",    # Only top line
                "none": "0000"        # No guide lines
            }
            
            target_pattern = guide_patterns.get(line_style, "1010")  # Default to dashed
            
            # Try to find and set guide line radio buttons
            guide_found = False
            
            # Look for radio buttons with specific patterns
            try:
                guide_radios = driver.find_elements(By.XPATH, f"//input[@type='radio' and @value='{target_pattern}']")
                if guide_radios:
                    guide_radios[0].click()
                    print(f"✓ Set guide lines to {line_style} style (pattern: {target_pattern})")
                    guide_found = True
            except:
                pass
            
            # If radio buttons not found, try clicking on guide line images
            if not guide_found:
                try:
                    # Look for clickable guide line images/labels
                    guide_images = driver.find_elements(By.XPATH, f"//img[contains(@src, 'guides') and contains(@src, '{target_pattern}')]")
                    if guide_images:
                        # Click the parent element (usually a label or div)
                        parent = guide_images[0].find_element(By.XPATH, "./..")
                        parent.click()
                        print(f"✓ Set guide lines to {line_style} style via image")
                        guide_found = True
                except:
                    pass
            
            # Try alternative selectors for guide options
            if not guide_found:
                alternative_selectors = [
                    (By.NAME, "guides"),
                    (By.ID, "guides"),
                    (By.CSS_SELECTOR, f"input[value='{target_pattern}']"),
                    (By.XPATH, f"//label[contains(text(), '{line_style.capitalize()}')]")
                ]
                
                for by_method, selector in alternative_selectors:
                    try:
                        element = driver.find_element(by_method, selector)
                        if element.tag_name == 'select':
                            Select(element).select_by_value(target_pattern)
                        else:
                            element.click()
                        print(f"✓ Set guide lines to {line_style} style")
                        guide_found = True
                        break
                    except:
                        continue
            
            if not guide_found:
                print(f"⚠️  Could not set {line_style} guide lines - using default")
                
        except Exception as e:
            print(f"Error setting guide lines: {e}")
            print("Using default guide line style")
        
        try:
            # Set letters style based on letter_style parameter
            print(f"Setting letters to {letter_style} style...")
            
            # Look for letters section/menu
            letters_menu_found = False
            
            # Step 1: Find and click the Letters menu/section to open letter options
            print("Looking for Letters menu to open...")
            letters_menu_opened = False
            
            # Try multiple approaches to find the Letters section
            letters_menu_selectors = [
                # Look for "Letters:" label or heading
                (By.XPATH, "//*[contains(text(), 'Letters:') or contains(text(), 'Letter Appearance') or contains(text(), 'Letter Style')]"),
                # Look for letters section divs or containers
                (By.XPATH, "//div[contains(@class, 'letter') or contains(@id, 'letter')]"),
                # Look for clickable elements with letter-related images
                (By.XPATH, "//img[contains(@src, 'appearance') or contains(@src, 'letter') or contains(@alt, 'letter')]"),
                # Look for buttons or links mentioning letters
                (By.XPATH, "//button[contains(text(), 'Letter') or contains(text(), 'Font')] | //a[contains(text(), 'Letter') or contains(text(), 'Font')]"),
                # Look for form sections related to appearance
                (By.XPATH, "//*[contains(@class, 'appearance') or contains(@id, 'appearance')]")
            ]
            
            for by_method, selector in letters_menu_selectors:
                try:
                    elements = driver.find_elements(by_method, selector)
                    for element in elements:
                        if element.is_displayed():
                            print(f"Attempting to click Letters menu element: {element.tag_name}")
                            try:
                                # Scroll into view first
                                driver.execute_script("arguments[0].scrollIntoView(true);", element)
                                time.sleep(1)
                                
                                # Try clicking the element
                                element.click()
                                time.sleep(2)
                                
                                # Check if letter style options became available
                                letter_options_check = driver.find_elements(By.XPATH, 
                                    "//input[@type='radio' and (contains(@value, 'dashed') or contains(@value, 'outline') or contains(@value, 'solid'))] | " +
                                    "//*[contains(text(), 'Dashed') or contains(text(), 'Outline') or contains(text(), 'Solid')]")
                                
                                if letter_options_check:
                                    print("✓ Letters menu opened successfully")
                                    letters_menu_opened = True
                                    break
                                    
                            except Exception as e:
                                print(f"Failed to click element: {e}")
                                continue
                                
                    if letters_menu_opened:
                        break
                        
                except Exception as e:
                    print(f"Error with selector {selector}: {e}")
                    continue
            
            # Step 2: If menu opened, find and select the desired letter style
            if letters_menu_opened:
                print(f"Looking for {letter_style} letter style option...")
                
                # Map letter styles to possible values/text
                style_mappings = {
                    'dashed': ['dashed', 'outline', 'Dashed', 'Outline'],
                    'solid': ['solid', 'filled', 'Solid', 'Filled'],
                    'outline': ['outline', 'dashed', 'Outline', 'Dashed']
                }
                
                possible_values = style_mappings.get(letter_style, [letter_style, letter_style.capitalize()])
                
                for value in possible_values:
                    # Try radio buttons first
                    try:
                        radio_options = driver.find_elements(By.XPATH, f"//input[@type='radio' and contains(@value, '{value}')]")
                        if radio_options:
                            radio_options[0].click()
                            print(f"✓ Selected {letter_style} letters via radio button")
                            letters_menu_found = True
                            break
                    except:
                        pass
                    
                    # Try clickable text/labels
                    try:
                        text_options = driver.find_elements(By.XPATH, f"//*[contains(text(), '{value}') and (self::label or self::span or self::div or self::button)]")
                        if text_options:
                            text_options[0].click()
                            print(f"✓ Selected {letter_style} letters via text option")
                            letters_menu_found = True
                            break
                    except:
                        pass
                        
                    if letters_menu_found:
                        break
            
            # Step 3: Alternative approaches if menu wasn't found or opened
            if not letters_menu_found:
                print("Trying alternative approaches to find letter style options...")
                
                # Try to find the Letters section with image preview (original approach)
                try:
                    # Look for the letters appearance image that shows "solid" vs other options
                    letters_images = driver.find_elements(By.XPATH, "//img[contains(@src, 'appearance') or contains(@src, 'letter')]")
                    
                    for img in letters_images:
                        # Click on the image or its parent to open options
                        try:
                            # First try clicking the image directly
                            img.click()
                            time.sleep(2)
                            
                            # Look for dashed/outline option after clicking
                            letter_options = driver.find_elements(By.XPATH, f"//input[@type='radio' and (contains(@value, '{letter_style}') or contains(@value, 'outline'))]")
                            if letter_options:
                                letter_options[0].click()
                                print(f"✓ Set letters to {letter_style} style")
                                letters_menu_found = True
                                break
                                
                            # Try looking for text options
                            letter_text_options = driver.find_elements(By.XPATH, f"//*[contains(text(), '{letter_style}') or contains(text(), 'outline') or contains(text(), '{letter_style.capitalize()}') or contains(text(), 'Outline')]")
                            if letter_text_options:
                                letter_text_options[0].click()
                                print(f"✓ Set letters to {letter_style} style via text option")
                                letters_menu_found = True
                                break
                                
                        except:
                            continue
                            
                except:
                    pass
            
            # Alternative approach: look for letters configuration area
            if not letters_menu_found:
                try:
                    # Look for letter style radio buttons or selects
                    letter_style_selectors = [
                        (By.NAME, "letterStyle"),
                        (By.NAME, "letters"),
                        (By.ID, "letterStyle"),
                        (By.ID, "letters"),
                        (By.CSS_SELECTOR, f"input[value*='{letter_style}']"),
                        (By.CSS_SELECTOR, "input[value*='outline']"),
                        (By.XPATH, f"//input[@type='radio' and contains(@value, '{letter_style}')]"),
                        (By.XPATH, "//input[@type='radio' and contains(@value, 'outline')]"),
                        (By.XPATH, f"//select//option[contains(text(), '{letter_style}') or contains(text(), 'outline')]")
                    ]
                    
                    for by_method, selector in letter_style_selectors:
                        try:
                            element = driver.find_element(by_method, selector)
                            if element.tag_name == 'select':
                                Select(element).select_by_visible_text(letter_style.capitalize())
                            elif element.tag_name == 'option':
                                element.click()
                            elif element.get_attribute('type') == 'radio':
                                element.click()
                            else:
                                element.click()
                            print(f"✓ Set letters to {letter_style} style via form control")
                            letters_menu_found = True
                            break
                        except:
                            continue
                            
                except:
                    pass
            
            # Try clicking on specific letter appearance sections
            if not letters_menu_found:
                try:
                    # Look for sections labeled "Letters:" or similar
                    letter_sections = driver.find_elements(By.XPATH, "//*[contains(text(), 'Letters:') or contains(text(), 'Letter')]")
                    
                    for section in letter_sections:
                        try:
                            # Click on the section to expand options
                            section.click()
                            time.sleep(1)
                            
                            # Look for dashed/outline options nearby
                            parent = section.find_element(By.XPATH, "../..")
                            letter_options = parent.find_elements(By.XPATH, f".//*[contains(text(), '{letter_style}') or contains(text(), 'outline')]")
                            
                            if letter_options:
                                letter_options[0].click()
                                print(f"✓ Set letters to {letter_style} style via section")
                                letters_menu_found = True
                                break
                                
                        except:
                            continue
                            
                except:
                    pass
            
            # Final attempt: look for any clickable elements related to letter styling
            if not letters_menu_found:
                try:
                    # Find elements that might open letter options
                    clickable_elements = driver.find_elements(By.XPATH, "//*[contains(@class, 'letter') or contains(@id, 'letter') or contains(text(), 'appearance')]")
                    
                    for element in clickable_elements:
                        try:
                            if element.is_displayed() and element.is_enabled():
                                element.click()
                                time.sleep(1)
                                
                                # Check if any letter style options appeared
                                new_letter_options = driver.find_elements(By.XPATH, f"//*[contains(text(), '{letter_style}') or contains(text(), 'outline')]")
                                if new_letter_options:
                                    new_letter_options[0].click()
                                    print(f"✓ Set letters to {letter_style} style via clickable element")
                                    letters_menu_found = True
                                    break
                        except:
                            continue
                            
                except:
                    pass
            
            if not letters_menu_found:
                print(f"⚠️  Could not find letters menu to set {letter_style} style - using default")
            
            # Step 4: Look for and click OK/Apply/Done button after selecting letter style
            print("Looking for OK/Apply/Done button...")
            ok_button_found = False
            
            ok_button_selectors = [
                # Standard OK buttons
                (By.XPATH, "//button[contains(text(), 'OK') or contains(text(), 'ok')]"),
                (By.XPATH, "//input[@type='button' and (contains(@value, 'OK') or contains(@value, 'ok'))]"),
                (By.XPATH, "//input[@type='submit' and (contains(@value, 'OK') or contains(@value, 'ok'))]"),
                # Apply buttons
                (By.XPATH, "//button[contains(text(), 'Apply') or contains(text(), 'apply')]"),
                (By.XPATH, "//input[@type='button' and (contains(@value, 'Apply') or contains(@value, 'apply'))]"),
                # Done buttons
                (By.XPATH, "//button[contains(text(), 'Done') or contains(text(), 'done')]"),
                (By.XPATH, "//input[@type='button' and (contains(@value, 'Done') or contains(@value, 'done'))]"),
                # Close buttons that might apply changes
                (By.XPATH, "//button[contains(text(), 'Close') and not(contains(text(), 'close'))]"),
                # Save buttons
                (By.XPATH, "//button[contains(text(), 'Save') or contains(text(), 'save')]"),
                # Accept/Confirm buttons
                (By.XPATH, "//button[contains(text(), 'Accept') or contains(text(), 'Confirm')]")
            ]
            
            for by_method, selector in ok_button_selectors:
                try:
                    ok_buttons = driver.find_elements(by_method, selector)
                    for btn in ok_buttons:
                        if btn.is_displayed() and btn.is_enabled():
                            print(f"Found OK/Apply button: {btn.text or btn.get_attribute('value')}")
                            try:
                                # Scroll into view
                                driver.execute_script("arguments[0].scrollIntoView(true);", btn)
                                time.sleep(1)
                                
                                # Click the button
                                btn.click()
                                print("✓ Clicked OK/Apply button")
                                ok_button_found = True
                                time.sleep(2)  # Wait for changes to apply
                                break
                                
                            except Exception as e:
                                print(f"Failed to click OK button: {e}")
                                try:
                                    # Try JavaScript click as fallback
                                    driver.execute_script("arguments[0].click();", btn)
                                    print("✓ Clicked OK button via JavaScript")
                                    ok_button_found = True
                                    time.sleep(2)
                                    break
                                except:
                                    continue
                                    
                    if ok_button_found:
                        break
                        
                except Exception as e:
                    print(f"Error with OK button selector {selector}: {e}")
                    continue
            
            if not ok_button_found:
                print("ℹ️  No OK/Apply button found (changes may be applied automatically)")
            
            # Give the page time to process any changes
            time.sleep(2)
                
        except Exception as e:
            print(f"Error setting {letter_style} letters: {e}")
            print("Using default letter style")
        
        try:
            # Paper size
            paper_select = driver.find_element(By.NAME, "paperSize")
            Select(paper_select).select_by_value("letter")
            print("Set paper size to letter")
        except:
            pass
        
        # Find and click the Create Worksheet button
        create_button = None
        button_selectors = [
            (By.XPATH, "//button[contains(text(), 'Create Worksheet')]"),
            (By.XPATH, "//input[@value='Create Worksheet']"),
            (By.CSS_SELECTOR, "button[type='submit']"),
            (By.CSS_SELECTOR, ".btn-primary"),
            (By.XPATH, "//button[contains(@class, 'btn') and contains(text(), 'Create')]")
        ]
        
        for by_method, selector in button_selectors:
            try:
                create_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((by_method, selector))
                )
                print(f"Found create button: {selector}")
                break
            except:
                continue
        
        if create_button:
            print("Clicking Create Worksheet button...")
            
            # Scroll button into view
            driver.execute_script("arguments[0].scrollIntoView(true);", create_button)
            time.sleep(1)
            
            # Click the button
            try:
                create_button.click()
            except:
                # Try JavaScript click if regular click fails
                driver.execute_script("arguments[0].click();", create_button)
            
            print("Waiting for worksheet generation...")
            
            # Method 1: Wait for direct PDF download
            pdf_file = wait_for_pdf_download(download_dir, initial_files, timeout=15)
            
            if pdf_file:
                final_path = os.path.join(download_dir, output_file)
                os.rename(os.path.join(download_dir, pdf_file), final_path)
                print(f"✓ PDF downloaded and saved as: {output_file}")
                return True
            
            # Method 2: Check for redirects or new tabs
            print("Checking for redirects or new windows...")
            time.sleep(5)
            
            # Check if URL changed
            current_url = driver.current_url
            print(f"Current URL: {current_url}")
            
            # Check for new windows/tabs
            if len(driver.window_handles) > 1:
                print("New window/tab detected, switching...")
                driver.switch_to.window(driver.window_handles[-1])
                time.sleep(3)
                
                new_url = driver.current_url
                print(f"New window URL: {new_url}")
                
                if new_url.endswith('.pdf'):
                    print("Direct PDF URL found, downloading...")
                    response = requests.get(new_url)
                    with open(output_file, 'wb') as f:
                        f.write(response.content)
                    print(f"✓ PDF downloaded: {output_file}")
                    return True
            
            # Method 3: Look for download links on the page
            print("Looking for download links...")
            download_links = driver.find_elements(By.XPATH, "//a[contains(@href, '.pdf')]")
            
            if download_links:
                print(f"Found {len(download_links)} PDF download links")
                link = download_links[0]
                href = link.get_attribute('href')
                print(f"Downloading from: {href}")
                
                try:
                    response = requests.get(href)
                    with open(output_file, 'wb') as f:
                        f.write(response.content)
                    print(f"✓ PDF downloaded: {output_file}")
                    return True
                except Exception as e:
                    print(f"Error downloading PDF: {e}")
            
            # Method 4: Check if we need to wait longer or click additional buttons
            print("Looking for additional buttons or messages...")
            
            # Look for "Download" or "Save" buttons
            download_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Download')] | //a[contains(text(), 'Download')] | //button[contains(text(), 'Save')] | //a[contains(text(), 'Save')]")
            
            if download_buttons:
                print(f"Found {len(download_buttons)} download buttons")
                for button in download_buttons:
                    try:
                        button.click()
                        print("Clicked download button, waiting for PDF...")
                        pdf_file = wait_for_pdf_download(download_dir, initial_files, timeout=10)
                        if pdf_file:
                            final_path = os.path.join(download_dir, output_file)
                            os.rename(os.path.join(download_dir, pdf_file), final_path)
                            print(f"✓ PDF downloaded: {output_file}")
                            return True
                    except Exception as e:
                        print(f"Error clicking download button: {e}")
            
            print("No PDF was generated or downloaded")
            return False
            
        else:
            print("ERROR: Could not find Create Worksheet button")
            return False
            
    except Exception as e:
        print(f"Error generating worksheet: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        # Take a screenshot for debugging
        try:
            driver.save_screenshot("debug_screenshot_advanced.png")
            print("Debug screenshot saved: debug_screenshot_advanced.png")
            
            # Save page source for analysis
            with open("debug_page_source.html", "w") as f:
                f.write(driver.page_source)
            print("Page source saved: debug_page_source.html")
            
        except:
            pass
        
        driver.quit()

def main():
    parser = argparse.ArgumentParser(description='Advanced handwriting practice worksheet generator')
    parser.add_argument('--text', default="The quick brown fox jumps over the lazy dog",
                       help='Text for handwriting practice')
    parser.add_argument('--output', default="handwriting_worksheet.pdf",
                       help='Output PDF filename')
    parser.add_argument('--line-style', default="dashed", 
                       choices=['solid', 'dashed', 'dotted', 'minimal', 'none'],
                       help='Guide line style (default: dashed)')
    parser.add_argument('--letter-style', default="dashed",
                       choices=['solid', 'dashed', 'outline'],
                       help='Letter style (default: dashed)')
    parser.add_argument('--visible', action='store_true',
                       help='Run browser in visible mode (not headless)')
    
    args = parser.parse_args()
    
    print("Advanced Handwriting Worksheet Generator")
    print("=" * 45)
    print(f"Text: {args.text}")
    print(f"Output: {args.output}")
    print(f"Line Style: {args.line_style}")
    print(f"Letter Style: {args.letter_style}")
    print(f"Mode: {'Visible' if args.visible else 'Headless'}")
    print()
    
    success = generate_worksheet_advanced(
        text=args.text,
        output_file=args.output,
        line_style=args.line_style,
        letter_style=args.letter_style,
        headless=not args.visible
    )
    
    if success:
        print("\n✓ Worksheet generated successfully!")
        print(f"Check your file: {args.output}")
    else:
        print("\n✗ Failed to generate worksheet")
        print("\nDebugging information:")
        print("- debug_screenshot_advanced.png: Visual state of the page")
        print("- debug_page_source.html: HTML source for analysis")
        print("\nTroubleshooting tips:")
        print("1. Try running with --visible to watch the process")
        print("2. The website might be using CAPTCHA or other anti-bot measures")
        print("3. Try using the manual browser method from CURL_GUIDE.md")
        sys.exit(1)

if __name__ == "__main__":
    main()
