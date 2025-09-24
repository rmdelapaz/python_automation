#!/usr/bin/env python3
"""
Script to check and fix navigation breadcrumbs and footer links in all course HTML files.
Works with Windows WSL paths and native paths.
"""

import os
import re
import sys
import platform
from pathlib import Path
from typing import List, Tuple, Optional, Dict
from dataclasses import dataclass
from bs4 import BeautifulSoup
import html

@dataclass
class Lesson:
    """Represents a lesson in the course."""
    module_num: int
    lesson_num: int
    filename: str
    title: str
    module_name: str

class CourseNavigationFixer:
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.lessons = self._define_course_structure()
        self.verify_structure()
        
    def verify_structure(self):
        """Verify that all HTML files are mapped in the structure."""
        # Get all HTML files in directory
        all_html_files = set(
            f.name for f in self.base_path.glob("*.html") 
            if f.name != "index.html" and not f.name.startswith("_")
        )
        
        # Get mapped files
        mapped_files = set(lesson.filename for lesson in self.lessons)
        
        # Find unmapped files
        unmapped = all_html_files - mapped_files
        
        if unmapped:
            print("⚠️  WARNING: The following files are not mapped in the course structure:")
            for file in sorted(unmapped):
                print(f"   - {file}")
            print("\nThese files will be skipped and won't have navigation.")
            response = input("\nContinue anyway? (y/n): ").strip().lower()
            if response != 'y':
                sys.exit(1)
        else:
            print(f"✅ All {len(all_html_files)} HTML files are mapped in the course structure.")
            print("   Navigation will be consistent across all files.\n")
        
    def _define_course_structure(self) -> List[Lesson]:
        """Define the complete course structure with all lessons based on actual files."""
        lessons = [
            # Module 1: File and System Automation (filesystem_*)
            Lesson(1, 1, "filesystem_advanced_file_operations.html", 
                   "Advanced File Operations", "File and System Automation"),
            Lesson(1, 2, "filesystem_batch_renaming.html", 
                   "Batch Renaming", "File and System Automation"),
            Lesson(1, 3, "filesystem_directory_watching.html", 
                   "Directory Watching", "File and System Automation"),
            Lesson(1, 4, "filesystem_file_organization_scripts.html", 
                   "File Organization Scripts", "File and System Automation"),
            Lesson(1, 5, "filesystem_backup_automation.html", 
                   "Backup Automation", "File and System Automation"),
            
            # Module 2: Web Scraping (webscraping_*)
            Lesson(2, 1, "webscraping_html_css_selectors.html", 
                   "HTML & CSS Selectors", "Web Scraping"),
            Lesson(2, 2, "webscraping_beautifulsoup_mastery.html", 
                   "BeautifulSoup Mastery", "Web Scraping"),
            Lesson(2, 3, "webscraping_forms_cookies.html", 
                   "Forms and Cookies", "Web Scraping"),
            Lesson(2, 4, "webscraping_session_management.html", 
                   "Session Management", "Web Scraping"),
            Lesson(2, 5, "webscraping_ethics_robots.html", 
                   "Ethics and Robots.txt", "Web Scraping"),
            
            # Module 3: Browser Automation (browser_automation_*)
            Lesson(3, 1, "browser_automation_webdriver_setup.html", 
                   "WebDriver Setup", "Browser Automation"),
            Lesson(3, 2, "browser_automation_element_interaction.html", 
                   "Element Interaction", "Browser Automation"),
            Lesson(3, 3, "browser_automation_waiting_strategies.html", 
                   "Waiting Strategies", "Browser Automation"),
            Lesson(3, 4, "browser_automation_page_object_model.html", 
                   "Page Object Model", "Browser Automation"),
            Lesson(3, 5, "browser_automation_headless_browsing.html", 
                   "Headless Browsing", "Browser Automation"),
            
            # Module 4: Data Processing (workingwithdata_*)
            Lesson(4, 1, "workingwithdata_csv_processing.html", 
                   "CSV Processing", "Data Processing"),
            Lesson(4, 2, "workingwithdata_excel_automation.html", 
                   "Excel Automation", "Data Processing"),
            Lesson(4, 3, "workingwithdata_json_xml_parsing.html", 
                   "JSON & XML Parsing", "Data Processing"),
            Lesson(4, 4, "workingwithdata_pdf_manipulation.html", 
                   "PDF Manipulation", "Data Processing"),
            Lesson(4, 5, "workingwithdata_database_automation.html", 
                   "Database Automation", "Data Processing"),
            
            # Module 5: Email Automation (email_automation_*)
            Lesson(5, 1, "email_automation_sending_emails.html", 
                   "Sending Emails", "Email Automation"),
            Lesson(5, 2, "email_automation_reading_emails.html", 
                   "Reading Emails", "Email Automation"),
            Lesson(5, 3, "email_automation_attachments.html", 
                   "Email Attachments", "Email Automation"),
            Lesson(5, 4, "email_automation_html_emails.html", 
                   "HTML Emails", "Email Automation"),
            Lesson(5, 5, "email_automation_filtering_rules.html", 
                   "Email Filtering Rules", "Email Automation"),
            
            # Module 6: API Automation (api_automation_*)
            Lesson(6, 1, "api_automation_restful_consumption.html", 
                   "RESTful API Consumption", "API Automation"),
            Lesson(6, 2, "api_automation_authentication_methods.html", 
                   "Authentication Methods", "API Automation"),
            Lesson(6, 3, "api_automation_rate_limiting.html", 
                   "Rate Limiting", "API Automation"),
            Lesson(6, 4, "api_automation_webhook_implementation.html", 
                   "Webhook Implementation", "API Automation"),
            Lesson(6, 5, "api_automation_api_testing.html", 
                   "API Testing", "API Automation"),
            
            # Module 7: Cloud Automation (cloud_automation_*)
            Lesson(7, 1, "cloud_automation_aws_boto3.html", 
                   "AWS with Boto3", "Cloud Automation"),
            Lesson(7, 2, "cloud_automation_google_cloud.html", 
                   "Google Cloud Platform", "Cloud Automation"),
            Lesson(7, 3, "cloud_automation_storage.html", 
                   "Cloud Storage", "Cloud Automation"),
            Lesson(7, 4, "cloud_automation_serverless.html", 
                   "Serverless Functions", "Cloud Automation"),
            Lesson(7, 5, "cloud_automation_deploying.html", 
                   "Deployment Automation", "Cloud Automation"),
            
            # Module 8: Task Orchestration (task_orchestration_*)
            Lesson(8, 1, "task_orchestration_airflow_basics.html", 
                   "Apache Airflow Basics", "Task Orchestration"),
            Lesson(8, 2, "task_orchestration_creating_dags.html", 
                   "Creating DAGs", "Task Orchestration"),
            Lesson(8, 3, "task_orchestration_dependencies.html", 
                   "Task Dependencies", "Task Orchestration"),
            Lesson(8, 4, "task_orchestration_error_handling.html", 
                   "Error Handling", "Task Orchestration"),
            Lesson(8, 5, "task_orchestration_monitoring.html", 
                   "Monitoring and Alerts", "Task Orchestration"),
            
            # Module 9: Testing Automation (testing_automation_*)
            Lesson(9, 1, "testing_automation_unit.html", 
                   "Unit Test Automation", "Testing Automation"),
            Lesson(9, 2, "testing_automation_integration.html", 
                   "Integration Testing", "Testing Automation"),
            Lesson(9, 3, "testing_automation_ui_selenium.html", 
                   "UI Testing with Selenium", "Testing Automation"),
            Lesson(9, 4, "testing_automation_api.html", 
                   "API Testing", "Testing Automation"),
            Lesson(9, 5, "testing_automation_ci.html", 
                   "Continuous Integration", "Testing Automation"),
            
            # Module 10: System Administration (systemadmin_*)
            Lesson(10, 1, "systemadmin_scheduled_tasks.html", 
                   "Scheduled Tasks", "System Administration"),
            Lesson(10, 2, "systemadmin_process_management.html", 
                   "Process Management", "System Administration"),
            Lesson(10, 3, "systemadmin_log_analysis.html", 
                   "Log Analysis", "System Administration"),
            Lesson(10, 4, "systemadmin_system_monitoring.html", 
                   "System Monitoring", "System Administration"),
            Lesson(10, 5, "systemadmin_environment_management.html", 
                   "Environment Management", "System Administration"),
            
            # Module 11: GUI Automation (gui_automation_*)
            Lesson(11, 1, "gui_automation_pyautogui.html", 
                   "PyAutoGUI Basics", "GUI Automation"),
            Lesson(11, 2, "gui_automation_mouse_keyboard.html", 
                   "Mouse and Keyboard Control", "GUI Automation"),
            Lesson(11, 3, "gui_automation_screen_capture.html", 
                   "Screen Capture", "GUI Automation"),
            Lesson(11, 4, "gui_automation_window_management.html", 
                   "Window Management", "GUI Automation"),
            Lesson(11, 5, "gui_automation_cross_platform.html", 
                   "Cross-Platform GUI", "GUI Automation"),
            
            # Module 12: Chatbot Development (chatbot_*)
            Lesson(12, 1, "chatbot_telegram_bots.html", 
                   "Telegram Bots", "Chatbot Development"),
            Lesson(12, 2, "chatbot_discord_bots.html", 
                   "Discord Bots", "Chatbot Development"),
            Lesson(12, 3, "chatbot_slack_integration.html", 
                   "Slack Integration", "Chatbot Development"),
            Lesson(12, 4, "chatbot_command_handling.html", 
                   "Command Handling", "Chatbot Development"),
            Lesson(12, 5, "chatbot_nlp.html", 
                   "Natural Language Processing", "Chatbot Development"),
            
            # Module 13: Advanced Scraping (advanced_scraping_*)
            Lesson(13, 1, "advanced_scraping_selenium.html", 
                   "Advanced Selenium", "Advanced Web Scraping"),
            Lesson(13, 2, "advanced_scraping_scrapy.html", 
                   "Scrapy Framework", "Advanced Web Scraping"),
            Lesson(13, 3, "advanced_scraping_captcha.html", 
                   "CAPTCHA Handling", "Advanced Web Scraping"),
            Lesson(13, 4, "advanced_scraping_proxy_rotation.html", 
                   "Proxy Rotation", "Advanced Web Scraping"),
            Lesson(13, 5, "advanced_scraping_data_pipelines.html", 
                   "Data Pipelines", "Advanced Web Scraping"),
            
            # Module 14: RPA and Enterprise (rpa_enterprise_*)
            Lesson(14, 1, "rpa_enterprise_concepts.html", 
                   "RPA Concepts", "RPA and Enterprise Automation"),
            Lesson(14, 2, "rpa_enterprise_uipath_integration.html", 
                   "UiPath/Python Integration", "RPA and Enterprise Automation"),
            Lesson(14, 3, "rpa_enterprise_business_process.html", 
                   "Business Process Automation", "RPA and Enterprise Automation"),
            Lesson(14, 4, "rpa_enterprise_document_processing.html", 
                   "Document Processing", "RPA and Enterprise Automation"),
            Lesson(14, 5, "rpa_enterprise_reporting.html", 
                   "Reporting Automation", "RPA and Enterprise Automation"),
        ]
        return lessons
    
    def get_lesson_by_filename(self, filename: str) -> Optional[Lesson]:
        """Get lesson object by filename."""
        for lesson in self.lessons:
            if lesson.filename == filename:
                return lesson
        return None
    
    def get_previous_lesson(self, current: Lesson) -> Optional[Lesson]:
        """Get the previous lesson in sequence."""
        try:
            current_index = self.lessons.index(current)
            if current_index > 0:
                return self.lessons[current_index - 1]
        except ValueError:
            pass
        return None
    
    def get_next_lesson(self, current: Lesson) -> Optional[Lesson]:
        """Get the next lesson in sequence."""
        try:
            current_index = self.lessons.index(current)
            if current_index < len(self.lessons) - 1:
                return self.lessons[current_index + 1]
        except ValueError:
            pass
        return None
    
    def create_breadcrumb_html(self, lesson: Lesson) -> str:
        """Create breadcrumb HTML for a lesson."""
        breadcrumb = f"""
    <nav class="breadcrumb">
        <a href="index.html">Home</a> &gt; 
        <a href="index.html#module{lesson.module_num}">{lesson.module_name}</a> &gt; 
        <span>{lesson.title}</span>
    </nav>"""
        return breadcrumb
    
    def create_footer_navigation(self, lesson: Lesson) -> str:
        """Create footer navigation HTML."""
        prev_lesson = self.get_previous_lesson(lesson)
        next_lesson = self.get_next_lesson(lesson)
        
        footer_parts = ['<footer>', '<div class="navigation-links">']
        
        # Previous lesson link
        if prev_lesson:
            footer_parts.append(
                f'<a href="{prev_lesson.filename}" class="nav-prev">&larr; Previous: {prev_lesson.title}</a>'
            )
        else:
            footer_parts.append('<span class="nav-prev"></span>')
        
        # Home link
        footer_parts.append('<a href="index.html" class="nav-home">🏠 Course Home</a>')
        
        # Next lesson link
        if next_lesson:
            footer_parts.append(
                f'<a href="{next_lesson.filename}" class="nav-next">Next: {next_lesson.title} &rarr;</a>'
            )
        else:
            footer_parts.append('<span class="nav-next"></span>')
        
        footer_parts.extend(['</div>', '</footer>'])
        
        return '\n    '.join(footer_parts)
    
    def update_html_file(self, filepath: Path) -> bool:
        """Update a single HTML file with proper navigation."""
        try:
            filename = filepath.name
            lesson = self.get_lesson_by_filename(filename)
            
            if not lesson:
                print(f"  ⚠️  {filename} not in course structure, skipping...")
                return False
            
            # Read the file
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            soup = BeautifulSoup(content, 'html.parser')
            
            # Check if breadcrumb exists and update/add it
            existing_breadcrumb = soup.find('nav', class_='breadcrumb')
            new_breadcrumb = BeautifulSoup(self.create_breadcrumb_html(lesson), 'html.parser')
            
            if existing_breadcrumb:
                existing_breadcrumb.replace_with(new_breadcrumb.nav)
                print(f"  ✓ Updated breadcrumb in {filename}")
            else:
                # Add breadcrumb after body tag
                body = soup.find('body')
                if body:
                    # Insert at the beginning of body
                    body.insert(0, new_breadcrumb.nav)
                    print(f"  ✓ Added breadcrumb to {filename}")
            
            # Update footer
            existing_footer = soup.find('footer')
            new_footer = BeautifulSoup(self.create_footer_navigation(lesson), 'html.parser')
            
            if existing_footer:
                existing_footer.replace_with(new_footer.footer)
                print(f"  ✓ Updated footer navigation in {filename}")
            else:
                # Add footer at the end of body
                body = soup.find('body')
                if body:
                    body.append(new_footer.footer)
                    print(f"  ✓ Added footer navigation to {filename}")
            
            # Add CSS for navigation if not present
            if not soup.find('style', string=re.compile('breadcrumb|navigation-links')):
                style_tag = soup.new_tag('style')
                style_tag.string = """
        .breadcrumb {
            background: #f8f9fa;
            padding: 1rem;
            border-radius: 5px;
            margin-bottom: 2rem;
            font-size: 0.9rem;
        }
        
        .breadcrumb a {
            color: #667eea;
            text-decoration: none;
        }
        
        .breadcrumb a:hover {
            text-decoration: underline;
        }
        
        .navigation-links {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 2rem 0;
            margin-top: 3rem;
            border-top: 2px solid #e0e0e0;
        }
        
        .navigation-links a {
            color: #667eea;
            text-decoration: none;
            font-weight: 500;
            padding: 0.5rem 1rem;
            border-radius: 5px;
            transition: all 0.3s ease;
        }
        
        .navigation-links a:hover {
            background: #f0f0f0;
        }
        
        .nav-prev, .nav-next {
            flex: 1;
        }
        
        .nav-next {
            text-align: right;
        }
        
        .nav-home {
            text-align: center;
        }
        """
                head = soup.find('head')
                if head:
                    head.append(style_tag)
                    print(f"  ✓ Added navigation CSS to {filename}")
            
            # Write the updated content
            with open(filepath, 'w', encoding='utf-8') as f:
                # Use prettify with proper formatting
                f.write(str(soup))
            
            return True
            
        except Exception as e:
            print(f"  ❌ Error processing {filepath}: {e}")
            return False
    
    def process_all_files(self):
        """Process all HTML files in the directory."""
        print("\n🚀 Starting navigation fix for all course files...\n")
        
        # Get all HTML files except index.html
        html_files = [f for f in self.base_path.glob("*.html") 
                     if f.name != "index.html" and not f.name.startswith("_")]
        
        print(f"Found {len(html_files)} HTML files to process")
        print(f"Mapped {len(self.lessons)} files in course structure\n")
        
        success_count = 0
        skipped_count = 0
        
        for filepath in sorted(html_files):
            print(f"Processing: {filepath.name}")
            if self.update_html_file(filepath):
                success_count += 1
            else:
                skipped_count += 1
            print()
        
        print(f"✅ Completed!")
        print(f"   Successfully updated: {success_count} files")
        print(f"   Skipped/Failed: {skipped_count} files")
        
        # Create a summary report
        self.create_summary_report(html_files, success_count)
    
    def create_summary_report(self, files_processed: List[Path], success_count: int):
        """Create a summary report of the changes."""
        report_path = self.base_path / "navigation_update_report.txt"
        
        with open(report_path, 'w') as f:
            f.write("Course Navigation Update Report\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Total files found: {len(files_processed)}\n")
            f.write(f"Files in structure: {len(self.lessons)}\n")
            f.write(f"Successfully updated: {success_count}\n")
            f.write(f"Skipped/Failed: {len(files_processed) - success_count}\n\n")
            
            f.write("Course Structure:\n")
            f.write("-" * 30 + "\n")
            
            current_module = 0
            for lesson in self.lessons:
                if lesson.module_num != current_module:
                    current_module = lesson.module_num
                    f.write(f"\nModule {current_module}: {lesson.module_name}\n")
                
                f.write(f"  {lesson.module_num}.{lesson.lesson_num} - {lesson.title}\n")
                f.write(f"       File: {lesson.filename}\n")
            
            # List unmapped files
            mapped_files = set(lesson.filename for lesson in self.lessons)
            unmapped = [f for f in files_processed if f.name not in mapped_files]
            
            if unmapped:
                f.write("\n\nFiles not in structure (skipped):\n")
                f.write("-" * 30 + "\n")
                for filepath in sorted(unmapped):
                    f.write(f"  - {filepath.name}\n")
        
        print(f"\n📄 Report saved to: {report_path}")

def detect_path():
    """Detect the correct path based on the environment."""
    possible_paths = [
        # Running from within the project directory
        Path("."),
        Path("./python_automation"),
        
        # WSL paths from Windows
        Path("//wsl.localhost/Ubuntu/home/practicalace/projects/python_automation"),
        Path("//wsl$/Ubuntu/home/practicalace/projects/python_automation"),
        Path("\\\\wsl.localhost\\Ubuntu\\home\\practicalace\\projects\\python_automation"),
        Path("\\\\wsl$\\Ubuntu\\home\\practicalace\\projects\\python_automation"),
        
        # Native WSL/Linux paths
        Path("/home/practicalace/projects/python_automation"),
        Path("~/projects/python_automation").expanduser(),
        
        # Windows paths
        Path("C:/Users/practicalace/projects/python_automation"),
        Path("D:/projects/python_automation"),
    ]
    
    # Check current directory first
    current_dir = Path.cwd()
    print(f"Current directory: {current_dir}")
    
    # Check if we're already in the right directory
    test_file = "index.html"
    if (current_dir / test_file).exists():
        print(f"✅ Found course files in current directory: {current_dir}")
        return str(current_dir)
    
    # Check all possible paths
    for path in possible_paths:
        try:
            if path.exists() and (path / test_file).exists():
                print(f"✅ Found course files at: {path}")
                return str(path)
        except Exception as e:
            continue
    
    return None

def main():
    """Main function to run the navigation fixer."""
    print("=" * 60)
    print("   Course Navigation Fixer")
    print("=" * 60)
    print("\n🔍 Detecting course directory...\n")
    
    # Try to auto-detect the path
    base_path = detect_path()
    
    if not base_path:
        print("❌ Could not auto-detect the course directory.")
        print("\n📁 Please enter the full path to your python_automation folder:")
        print("   Examples:")
        print("   - Windows WSL: //wsl$/Ubuntu/home/practicalace/projects/python_automation")
        print("   - Linux/WSL: /home/practicalace/projects/python_automation")
        print("   - Windows: C:\\Users\\YourName\\projects\\python_automation")
        print("   - Or just '.' if you're running from within the folder\n")
        
        base_path = input("Path: ").strip()
        
        # Remove quotes if present
        base_path = base_path.strip('"').strip("'")
        
        # Check if the provided path exists
        if not Path(base_path).exists():
            print(f"\n❌ Path not found: {base_path}")
            print("Please check the path and try again.")
            return
        
        # Check if it contains course files
        if not (Path(base_path) / "index.html").exists():
            print(f"\n⚠️  Warning: index.html not found in {base_path}")
            proceed = input("Continue anyway? (y/n): ").strip().lower()
            if proceed != 'y':
                return
    
    print(f"\n✅ Using path: {base_path}\n")
    print("-" * 60)
    
    try:
        fixer = CourseNavigationFixer(base_path)
        fixer.process_all_files()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        print("Please check the path and try again.")

if __name__ == "__main__":
    main()
