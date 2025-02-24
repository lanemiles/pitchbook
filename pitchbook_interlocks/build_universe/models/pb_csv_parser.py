import csv
import time
from collections import Counter
from datetime import datetime


class PBCSVParser:
    def __init__(self, name: str, file_path: str):
        self.name: str = name
        self.file_path: str = file_path
        self.successes: int = 0
        self.failures: int = 0
        self.failure_reasons: list[str] = []
        self.start_time = time.time()

    def rows(
        self,
    ) -> list[tuple[dict[str, str], "PBCSVParser.RowValidator"]]:
        with open(self.file_path, newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            return [(row, self.RowValidator(self)) for row in reader]

    def parse_string(self, value: str) -> str | None:
        s = value.strip()
        return s if s else None

    def parse_float(self, value: str) -> float | None:
        try:
            return float(value.strip())
        except ValueError:
            return None

    def parse_boolean(self, s: str) -> bool | None:
        s = s.strip()
        if s == "Yes":
            return True
        elif s == "No":
            return False
        return None

    def parse_int(self, value: str) -> int | None:
        try:
            return int(value.strip())
        except ValueError:
            return None

    def parse_date_obj(self, date_string: str) -> datetime | None:
        try:
            return datetime.strptime(date_string.strip(), "%m/%d/%Y")
        except ValueError:
            return None

    def get_results(self) -> str:
        end_time = time.time()
        total = self.successes + self.failures
        sorted_failures = sorted(
            Counter(self.failure_reasons).items(), key=lambda x: x[1], reverse=True
        )
        return (
            f"{self.name} | Total: {total} | Successes: {self.successes} | "
            f"Failures: {self.failures} | Failure Reasons: {sorted_failures} | "
            f"Time: {(end_time - self.start_time):.2f} seconds"
        )

    class RowValidator:
        def __init__(self, parent: "PBCSVParser"):
            self.parent = parent
            self.errors: list[str] = []

        def validate(self, condition: bool, error_msg: str) -> bool:
            if not condition:
                self.errors.append(error_msg)
            return condition

        def is_valid(self) -> bool:
            return len(self.errors) == 0

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback) -> None:
            if self.errors:
                self.parent.failures += 1
                self.parent.failure_reasons.extend(self.errors)
            else:
                self.parent.successes += 1
