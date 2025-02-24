from pitchbook_interlocks.models.data_models import Employee
from pitchbook_interlocks.build_universe.models.pb_csv_parser import PBCSVParser
from pitchbook_interlocks.models.universe import Universe
from datetime import datetime


def load_employees(file_path: str, universe: Universe) -> None:
    parser = PBCSVParser("Investor Employees", file_path)

    for row, validator in parser.rows():
        person_id: str | None = parser.parse_string(row["PersonID"])
        entity_id: str | None = parser.parse_string(row["EntityID"])
        full_title: str | None = parser.parse_string(row["FullTitle"])
        position_level: str | None = parser.parse_string(row["PositionLevel"])
        is_current: bool | None = parser.parse_boolean(row["IsCurrent"])
        start_date: datetime | None = parser.parse_date_obj(row["StartDate"])
        end_date: datetime | None = parser.parse_date_obj(row["EndDate"])

        with validator as row_validator:
            validations = [
                (
                    person_id is not None and universe.person_store.exists(person_id),
                    "Invalid person_id: either missing or person with id not found.",
                ),
                (
                    entity_id is not None and universe.investor_store.exists(entity_id),
                    "Invalid entity_id: either missing or investor with id not found.",
                ),
                (
                    is_current is not None and is_current,
                    "Invalid is_current: either missing or not True.",
                ),
                (full_title is not None, "Invalid full_title: is None."),
                (position_level is not None, "Invalid position_level: is None."),
            ]

            for condition, error_message in validations:
                row_validator.validate(condition, error_message)

            if row_validator.is_valid():
                assert person_id is not None
                assert entity_id is not None
                assert full_title is not None
                assert position_level is not None
                assert is_current is not None

                employee = Employee(
                    person_id=person_id,
                    investor_id=entity_id,
                    full_title=full_title,
                    position_level=position_level,
                    is_current=is_current,
                    start_date=start_date,
                    end_date=end_date,
                )

                investor = universe.investor_store.get(entity_id)
                investor.employees.add(employee)

                person = universe.person_store.get(person_id)
                person.investor_jobs.add(employee)

    if universe.verbose_mode:
        print(parser.get_results())
