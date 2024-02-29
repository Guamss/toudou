import csv
import dataclasses
import io

from datetime import datetime

import toudou.models as models


def export_to_csv() -> io.StringIO:
    output = io.StringIO()
    csv_writer = csv.DictWriter(
        output,
        fieldnames=[f.name for f in dataclasses.fields(models.Todo)]
    )
    for todo in models.Todo.getToudous():
        csv_writer.writerow(dataclasses.asdict(todo))
    return output


def import_from_csv(csv_file: io.StringIO) -> None:
    csv_reader = csv.DictReader(
        csv_file,
        fieldnames=[f.name for f in dataclasses.fields(models.Todo)]
    )
    for row in csv_reader:
        models.Todo(
                task=row["task"], 
                date=datetime.fromisoformat(row["due"]) if row["due"] else None, 
                completed=row["complete"] == "True"
                )