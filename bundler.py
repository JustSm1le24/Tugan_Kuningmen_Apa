
import os
import base64
import re

# Configuration
PROJECT_DIR = r"c:\Users\Дулат\.gemini\antigravity\scratch\grandmother_birthday"
INDEX_FILE = os.path.join(PROJECT_DIR, "index.html")
CSS_FILE = os.path.join(PROJECT_DIR, "style.css")
JS_FILE = os.path.join(PROJECT_DIR, "script.js")
OUTPUT_FILE = os.path.join(PROJECT_DIR, "grandma_birthday_card.html")

def get_base64_mime(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    if ext == '.png':
        return 'image/png'
    elif ext in ['.jpg', '.jpeg']:
        return 'image/jpeg'
    elif ext == '.svg':
        return 'image/svg+xml'
    else:
        return 'application/octet-stream'

def file_to_base64(filepath):
    try:
        with open(filepath, "rb") as f:
            encoded = base64.b64encode(f.read()).decode('utf-8')
            mime = get_base64_mime(filepath)
            return f"data:{mime};base64,{encoded}"
    except Exception as e:
        print(f"Error encoding {filepath}: {e}")
        return None

def process_css(css_content, base_dir):
    # dedicated regex for url('...')
    def replace_url(match):
        url = match.group(1).strip("'\"")
        file_path = os.path.join(base_dir, url)
        if os.path.exists(file_path):
            b64_data = file_to_base64(file_path)
            if b64_data:
                return f"url('{b64_data}')"
        return match.group(0) # Return original if not found

    return re.sub(r"url\(([^)]+)\)", replace_url, css_content)

def main():
    print("Starting bundling process...")
    
    # 1. Read HTML
    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        html_content = f.read()

    # 2. Process and Inline CSS
    if os.path.exists(CSS_FILE):
        with open(CSS_FILE, "r", encoding="utf-8") as f:
            css_content = f.read()
            css_content = process_css(css_content, PROJECT_DIR)
            # Remove existing link to style.css
            html_content = re.sub(r'<link[^>]*rel="stylesheet"[^>]*href="style.css"[^>]*>', '', html_content)
            # Add inline style
            html_content = html_content.replace("</head>", f"<style>\n{css_content}\n</style>\n</head>")
            print("CSS inlined.")

    # 3. Inline JS
    if os.path.exists(JS_FILE):
        with open(JS_FILE, "r", encoding="utf-8") as f:
            js_content = f.read()
            # Remove existing script tag
            html_content = re.sub(r'<script[^>]*src="script.js"[^>]*></script>', '', html_content)
            # Add inline script
            html_content = html_content.replace("</body>", f"<script>\n{js_content}\n</script>\n</body>")
            print("JS inlined.")

    # 4. Inline HTML Images
    def replace_img_src(match):
        src = match.group(1)
        file_path = os.path.join(PROJECT_DIR, src)
        if os.path.exists(file_path):
            b64_data = file_to_base64(file_path)
            if b64_data:
                return f'src="{b64_data}"'
        print(f"Warning: Image not found or failed to encode: {src}")
        return match.group(0)

    html_content = re.sub(r'src="([^"]+)"', replace_img_src, html_content)
    print("Images inlined.")

    # 5. Write Output
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Successfully created {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
