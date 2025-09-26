#!/usr/bin/env python3
"""
Update python_automation to match python_intro/python_gamedev structure:
1. Add /js/course-enhancements.js
2. Add /js/clipboard.js  
3. Add /styles/enhanced.css
4. Update all HTML files to reference these scripts and styles
"""

import os
import re
import sys
import shutil
import platform
from pathlib import Path

def detect_path_format():
    """Detect if we're running on Windows or WSL/Linux"""
    system = platform.system()
    if system == "Windows":
        return "windows"
    else:
        return "wsl"

def get_project_paths():
    """Get the correct paths for both source and destination projects"""
    system_type = detect_path_format()
    
    if system_type == "windows":
        # Windows path format for WSL files
        paths = {
            'automation': [
                r"\\wsl$\Ubuntu\home\practicalace\projects\python_automation",
                r"\\wsl.localhost\Ubuntu\home\practicalace\projects\python_automation",
            ],
            'intro': [
                r"\\wsl$\Ubuntu\home\practicalace\projects\python_intro",
                r"\\wsl.localhost\Ubuntu\home\practicalace\projects\python_intro",
            ],
            'gamedev': [
                r"\\wsl$\Ubuntu\home\practicalace\projects\python_gamedev",
                r"\\wsl.localhost\Ubuntu\home\practicalace\projects\python_gamedev",
            ]
        }
    else:
        # WSL/Linux path format
        paths = {
            'automation': [
                "/home/practicalace/projects/python_automation",
                os.path.expanduser("~/projects/python_automation"),
            ],
            'intro': [
                "/home/practicalace/projects/python_intro",
                os.path.expanduser("~/projects/python_intro"),
            ],
            'gamedev': [
                "/home/practicalace/projects/python_gamedev",
                os.path.expanduser("~/projects/python_gamedev"),
            ]
        }
    
    # Find which paths exist
    found_paths = {}
    for project, path_list in paths.items():
        for path in path_list:
            if os.path.exists(path):
                found_paths[project] = path
                break
    
    if 'automation' not in found_paths:
        print("❌ Could not find python_automation folder!")
        print("Please enter the full path to python_automation:")
        user_path = input().strip()
        if os.path.exists(user_path):
            found_paths['automation'] = user_path
        else:
            print(f"Error: Path '{user_path}' does not exist!")
            sys.exit(1)
    
    return found_paths

def copy_js_files(paths):
    """Copy JavaScript files from python_intro to python_automation"""
    print("\n📂 Setting up JavaScript files...")
    
    # Create js directory if it doesn't exist
    js_dir = os.path.join(paths['automation'], 'js')
    if not os.path.exists(js_dir):
        os.makedirs(js_dir)
        print(f"  ✅ Created js directory")
    
    # Files to copy
    js_files = ['course-enhancements.js', 'clipboard.js']
    
    # Try to copy from python_intro first, then python_gamedev
    source_project = None
    if 'intro' in paths:
        source_project = 'intro'
    elif 'gamedev' in paths:
        source_project = 'gamedev'
    else:
        print("  ⚠️  No source project found for JS files!")
        print("  Please manually copy course-enhancements.js and clipboard.js to python_automation/js/")
        return False
    
    source_js_dir = os.path.join(paths[source_project], 'js')
    
    for js_file in js_files:
        source_file = os.path.join(source_js_dir, js_file)
        dest_file = os.path.join(js_dir, js_file)
        
        if os.path.exists(source_file):
            if not os.path.exists(dest_file):
                try:
                    shutil.copy2(source_file, dest_file)
                    print(f"  ✅ Copied {js_file}")
                except Exception as e:
                    print(f"  ❌ Failed to copy {js_file}: {e}")
            else:
                print(f"  ✓ {js_file} already exists")
        else:
            print(f"  ⚠️  {js_file} not found in source")
    
    return True

def copy_enhanced_css(paths):
    """Copy enhanced.css from python_intro to python_automation"""
    print("\n📂 Setting up CSS files...")
    
    # Create styles directory if it doesn't exist
    styles_dir = os.path.join(paths['automation'], 'styles')
    if not os.path.exists(styles_dir):
        os.makedirs(styles_dir)
        print(f"  ✅ Created styles directory")
    
    # Try to copy from python_intro first
    source_project = None
    if 'intro' in paths:
        source_project = 'intro'
    elif 'gamedev' in paths:
        source_project = 'gamedev'
    else:
        print("  ⚠️  No source project found for CSS files!")
        return False
    
    source_css = os.path.join(paths[source_project], 'styles', 'enhanced.css')
    dest_css = os.path.join(styles_dir, 'enhanced.css')
    
    if os.path.exists(source_css):
        if not os.path.exists(dest_css):
            try:
                shutil.copy2(source_css, dest_css)
                print(f"  ✅ Copied enhanced.css")
            except Exception as e:
                print(f"  ❌ Failed to copy enhanced.css: {e}")
        else:
            print(f"  ✓ enhanced.css already exists")
    else:
        print(f"  ⚠️  enhanced.css not found in source")
        # Create a minimal enhanced.css if not found
        create_minimal_enhanced_css(dest_css)
    
    return True

def create_minimal_enhanced_css(css_path):
    """Create a minimal enhanced.css file if source not found"""
    minimal_css = """/* Enhanced styles for python_automation */

/* Reading time indicator */
.reading-time {
    font-size: 0.9rem;
    color: #666;
    margin: 1rem 0;
}

/* Skip to main content link */
.skip-to-main {
    position: absolute;
    left: -9999px;
    z-index: 999;
    padding: 1rem;
    background: #000;
    color: #fff;
    text-decoration: none;
}

.skip-to-main:focus {
    left: 50%;
    transform: translateX(-50%);
    top: 0;
}

/* Progress indicator */
.progress-indicator {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 4px;
    background: rgba(0,0,0,0.1);
    z-index: 1000;
}

.progress-bar {
    height: 100%;
    background: linear-gradient(to right, #667eea, #764ba2);
    width: 0;
    transition: width 0.3s ease;
}

/* Responsive SVG */
.responsive-svg {
    max-width: 100%;
    height: auto;
}

/* Code block improvements */
.code-block-wrapper {
    position: relative;
    margin: 1em 0;
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
    .dark-mode-toggle {
        background: #333;
        color: #fff;
    }
}
"""
    
    try:
        with open(css_path, 'w', encoding='utf-8') as f:
            f.write(minimal_css)
        print(f"  ✅ Created minimal enhanced.css")
    except Exception as e:
        print(f"  ❌ Failed to create enhanced.css: {e}")

def update_html_file(filepath):
    """Update a single HTML file to include new scripts and styles"""
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return False, f"Error reading file: {e}"
    
    original_content = content
    changes_made = []
    
    # 1. Add enhanced.css after main.css
    if 'enhanced.css' not in content:
        pattern = r'(<link href="[^"]*styles/main\.css" rel="stylesheet"/>)'
        replacement = r'\1\n    <link href="/styles/enhanced.css" rel="stylesheet"/>'
        new_content = re.sub(pattern, replacement, content, count=1)
        
        if new_content != content:
            content = new_content
            changes_made.append("added enhanced.css")
    
    # 2. Add course-enhancements.js before </head>
    if 'course-enhancements.js' not in content:
        # First, check if there's any </head> tag
        if '</head>' in content:
            # Add before </head>
            pattern = r'(</head>)'
            replacement = r'    <script src="/js/course-enhancements.js" defer></script>\n\1'
            new_content = re.sub(pattern, replacement, content, count=1)
            
            if new_content != content:
                content = new_content
                changes_made.append("added course-enhancements.js")
    
    # 3. Add clipboard.js after course-enhancements.js or before </head>
    if 'clipboard.js' not in content:
        if 'course-enhancements.js' in content:
            # Add after course-enhancements.js
            pattern = r'(    <script src="/js/course-enhancements.js" defer></script>)'
            replacement = r'\1\n    <script src="/js/clipboard.js" defer></script>'
            new_content = re.sub(pattern, replacement, content, count=1)
        else:
            # Add before </head>
            pattern = r'(</head>)'
            replacement = r'    <script src="/js/clipboard.js" defer></script>\n\1'
            new_content = re.sub(pattern, replacement, content, count=1)
        
        if new_content != content:
            content = new_content
            changes_made.append("added clipboard.js")
    
    # 4. Add skip-to-main link if not present
    if 'skip-to-main' not in content and '<body>' in content:
        pattern = r'(<body>)'
        replacement = r'\1\n    <!-- Skip to main content for accessibility -->\n    <a href="#main-content" class="skip-to-main">Skip to main content</a>'
        new_content = re.sub(pattern, replacement, content, count=1)
        
        if new_content != content:
            content = new_content
            changes_made.append("added skip-to-main link")
    
    # 5. Add progress indicator if not present
    if 'progress-indicator' not in content and 'skip-to-main' in content:
        pattern = r'(    <a href="#main-content" class="skip-to-main">Skip to main content</a>)'
        replacement = r'\1\n    \n    <!-- Progress indicator -->\n    <div class="progress-indicator" role="progressbar" aria-label="Page scroll progress">\n        <div class="progress-bar"></div>\n    </div>'
        new_content = re.sub(pattern, replacement, content, count=1)
        
        if new_content != content:
            content = new_content
            changes_made.append("added progress indicator")
    
    # 6. Wrap main content with main tag if not present
    if '<main' not in content and '<h1>' in content:
        # Find the first h1 and wrap everything from there
        pattern = r'(<h1[^>]*>)'
        replacement = r'    \n    <main id="main-content">\n    \1'
        new_content = re.sub(pattern, replacement, content, count=1)
        
        # Close main before </body>
        if new_content != content:
            pattern = r'(</body>)'
            replacement = r'    </main>\n\1'
            content = re.sub(pattern, replacement, new_content, count=1)
            changes_made.append("added main wrapper")
    
    # Write the updated content if changes were made
    if changes_made:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, changes_made
        except Exception as e:
            return False, f"Error writing file: {e}"
    else:
        return False, "no changes needed"

def process_all_html_files(automation_path):
    """Process all HTML files in python_automation"""
    print("\n📝 Updating HTML files...")
    
    # Get all HTML files
    html_files = []
    for filename in os.listdir(automation_path):
        if filename.endswith('.html'):
            html_files.append(filename)
    
    html_files.sort()
    total_files = len(html_files)
    
    print(f"Found {total_files} HTML files to process")
    print("-" * 60)
    
    # Statistics
    updated_count = 0
    skipped_count = 0
    failed_files = []
    
    # Process each file
    for i, filename in enumerate(html_files, 1):
        filepath = os.path.join(automation_path, filename)
        progress = f"[{i}/{total_files}]"
        
        success, result = update_html_file(filepath)
        
        if success:
            changes = ", ".join(result)
            print(f"{progress} ✅ {filename}: {changes}")
            updated_count += 1
        elif "no changes needed" in str(result):
            print(f"{progress} ✓  {filename}: already updated")
            skipped_count += 1
        else:
            print(f"{progress} ⚠  {filename}: {result}")
            failed_files.append((filename, result))
    
    # Print summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total files processed: {total_files}")
    print(f"Files updated: {updated_count}")
    print(f"Files skipped (already updated): {skipped_count}")
    print(f"Files failed: {len(failed_files)}")
    
    if failed_files:
        print("\n⚠ Failed files:")
        for filename, error in failed_files:
            print(f"  - {filename}: {error}")
    
    return updated_count > 0

def verify_setup(automation_path):
    """Verify that all required files are in place"""
    print("\n🔍 Verifying setup...")
    
    checks = {
        'js/course-enhancements.js': False,
        'js/clipboard.js': False,
        'styles/enhanced.css': False
    }
    
    for file_path in checks.keys():
        full_path = os.path.join(automation_path, file_path)
        if os.path.exists(full_path):
            checks[file_path] = True
            print(f"  ✅ {file_path} exists")
        else:
            print(f"  ❌ {file_path} missing")
    
    all_good = all(checks.values())
    
    if all_good:
        print("\n✅ All required files are in place!")
    else:
        print("\n⚠️  Some files are missing. The setup may not work correctly.")
    
    return all_good

def main():
    """Main function"""
    
    print("=" * 60)
    print("PYTHON_AUTOMATION STRUCTURE UPDATER")
    print("=" * 60)
    print("\nThis script will update python_automation to match")
    print("the structure of python_intro and python_gamedev.\n")
    
    # Get project paths
    print("🔍 Detecting project paths...")
    paths = get_project_paths()
    
    print(f"✅ Found python_automation at: {paths['automation']}")
    if 'intro' in paths:
        print(f"✅ Found python_intro at: {paths['intro']}")
    if 'gamedev' in paths:
        print(f"✅ Found python_gamedev at: {paths['gamedev']}")
    
    # Step 1: Copy JS files
    if not copy_js_files(paths):
        print("\n⚠️  Warning: Some JS files could not be copied.")
    
    # Step 2: Copy CSS files
    if not copy_enhanced_css(paths):
        print("\n⚠️  Warning: enhanced.css could not be copied.")
    
    # Step 3: Update HTML files
    if process_all_html_files(paths['automation']):
        print("\n✅ HTML files successfully updated!")
    else:
        print("\n✓ No HTML files needed updating.")
    
    # Step 4: Verify setup
    verify_setup(paths['automation'])
    
    print("\n" + "=" * 60)
    print("✅ PROCESS COMPLETE!")
    print("=" * 60)
    print("\nYour python_automation project now has:")
    print("  • Course enhancement features")
    print("  • Copy-to-clipboard functionality")
    print("  • Enhanced CSS styling")
    print("  • Improved accessibility features")
    print("\nEnjoy your enhanced automation course! 🚀")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Process interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
