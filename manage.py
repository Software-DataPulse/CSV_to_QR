# manage.py
import os
import sys
sys.path.append('/path/to/your_project_directory')

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qr_generator_project.settings')  # <-- Update 'qr_generator' with your project name
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
