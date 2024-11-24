from django.core.management.base import BaseCommand
from django.db import connection


#python manage.py reset_sequence


class Command(BaseCommand):
    help = "Reset the SQLite sequence for the 'teachers_teacher' table"

    def handle(self, *args, **options):
        try:
            with connection.cursor() as cursor:
                cursor.execute("UPDATE sqlite_sequence SET seq = 0 WHERE name = 'teachers_teacher';")
            self.stdout.write(self.style.SUCCESS("Successfully reset the sequence for 'teachers_teacher'."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error resetting the sequence: {e}"))



#Identifying the Sequence Name: If you’re not sure about the sequence name, 
#you can find it

#SELECT pg_get_serial_sequence('teachers_teacher', 'id');

"""
class Command(BaseCommand):
    help = "Reset the PostgreSQL sequence for the 'teachers_teacher' table"

    def handle(self, *args, **options):
        try:
            with connection.cursor() as cursor:
                # Replace 'teachers_teacher_id_seq' with your actual sequence name
                cursor.execute("ALTER SEQUENCE teachers_teacher_id_seq RESTART WITH 1;")
            self.stdout.write(self.style.SUCCESS("Successfully reset the sequence for 'teachers_teacher'."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error resetting the sequence: {e}"))
            
"""            