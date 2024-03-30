import csv
import dataclasses
import io
from datetime import datetime
import toudou.models as models

DOWNLOAD_DIR = 'src/toudou'

def export_to_csv() -> io.StringIO:
    """
    Export the to-do tasks to a CSV file.

    Returns:
        io.StringIO: A StringIO object containing the CSV data.
    """
    output = io.StringIO()
    csv_writer = csv.DictWriter(
        output,
        fieldnames=[f.name for f in dataclasses.fields(models.Todo) if f.name != 'id']
    )
    csv_writer.writeheader()
    for todo in models.getToudous():
        todo_dict = {f.name: getattr(todo, f.name) for f in dataclasses.fields(models.Todo) if f.name != 'id'}
        csv_writer.writerow(todo_dict)
    return output


def import_from_csv(csv_file: io.TextIOWrapper) -> None:
    csv_file.seek(0)
    csv_reader = csv.DictReader(
        csv_file,
        fieldnames=["task", "date", "completed"]
    )
    for row in csv_reader:
        if not (row['task'] == 'task' or row['date'] == 'date' or row['completed'] == 'completed'):
            models.create_todo(
                task=row["task"],
                due=datetime.fromisoformat(row["date"]) if row["date"] else None,
                completed=row["completed"] == "True"
            )


    