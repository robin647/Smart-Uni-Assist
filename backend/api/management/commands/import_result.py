import pandas as pd
from django.core.management.base import BaseCommand
from api.models import Result, Course, User

class Command(BaseCommand):
    help = 'Import result data from Excel file'

    def add_arguments(self, parser):
        parser.add_argument('excel_file', type=str, help='Path to the Excel file')
        parser.add_argument('--user-id', type=int, help='User ID to assign to all results')

    def handle(self, *args, **options):
        excel_file = options['excel_file']
        user_id = options.get('user_id')

        try:
            df = pd.read_excel(excel_file)
            df = pd.read_excel(excel_file)
            print(df.columns)  

        except Exception as e:
            self.stderr.write(self.style.ERROR(f" Failed to read Excel file: {e}"))
            return

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            self.stderr.write(self.style.ERROR(f" User with ID {user_id} does not exist"))
            return

        for index, row in df.iterrows():
            try:
                course = Course.objects.get(name=row['course_name'], user=user)
                Result.objects.create(
                    user=user,
                    course=course,
                    grade=row['grade'],
                    comment=row['comment']
                )
                self.stdout.write(self.style.SUCCESS(f" Added result: {course.name} - {row['grade']}"))
            except Course.DoesNotExist:
                self.stderr.write(self.style.ERROR(f" Course '{row['course_name']}' not found for user {user.username}"))
            except Exception as e:
                self.stderr.write(self.style.ERROR(f" Failed to add result: {e}"))
