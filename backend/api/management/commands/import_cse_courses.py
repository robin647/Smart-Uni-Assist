import pandas as pd
from django.core.management.base import BaseCommand
from api.models import CSESkillDevelopmentCourse

class Command(BaseCommand):
    help = 'Import skill development courses from Excel'

    def add_arguments(self, parser):
        parser.add_argument('excel_file', type=str, help='Path to the Excel file')

    def handle(self, *args, **options):
        excel_file = options['excel_file']

        try:
            df = pd.read_excel(excel_file)
            print("Excel Columns:", df.columns)  # Debugging
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Could not read file: {e}"))
            return

        for _, row in df.iterrows():
            try:
                course_name = row['Course Name']  # Match exact column name
                CSESkillDevelopmentCourse.objects.create(course_name=course_name)
                self.stdout.write(self.style.SUCCESS(f"✅ Added: {course_name}"))
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"❌ Failed to add: {e}"))
