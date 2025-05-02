# api/management/commands/import_courses.py

import pandas as pd
from django.core.management.base import BaseCommand
from api.models import Course, User

class Command(BaseCommand):
    help = 'Import courses from Excel file'

    def add_arguments(self, parser):
        parser.add_argument('excel_file', type=str, help='Path to the Excel file')
        parser.add_argument('--user-id', type=int, help='User ID to assign to all courses')

    def handle(self, *args, **kwargs):
        excel_file = kwargs['excel_file']
        user_id = kwargs.get('user_id')

        try:
            # Read the Excel file
            df = pd.read_excel(excel_file)
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Failed to read Excel file: {e}'))
            return

        # Iterate through the rows of the Excel file and add to the database
        for _, row in df.iterrows():
            try:
                # Check if the user ID is provided and retrieve the user, or set to None if not
                user = User.objects.get(id=user_id) if user_id else None
                
                # Create the Course object and save it to the database
                course = Course.objects.create(
                    user=user,
                    name=row['name'],  # Name of the course
                    code=row['code'],  # Course code
                    teacher=row['teacher']  # Teacher's name
                )
                
                self.stdout.write(self.style.SUCCESS(f"Added course: {course.name}"))
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Failed to add course: {e}"))
