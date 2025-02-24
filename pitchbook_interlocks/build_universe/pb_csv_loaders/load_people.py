from pitchbook_interlocks.models.data_models import Person
from pitchbook_interlocks.build_universe.models.pb_csv_parser import PBCSVParser
from pitchbook_interlocks.models.universe import Universe


def load_people(file_path: str, universe: Universe) -> None:
    parser = PBCSVParser("People", file_path)

    for row, validator in parser.rows():
        person_id: str | None = parser.parse_string(row["PersonID"])
        person_full_name: str | None = parser.parse_string(row["FullName"])

        with validator as row_validator:
            validations = [
                (person_id is not None, "Missing person_id"),
                (person_full_name is not None, "Missing person_full_name"),
            ]

            for condition, error_message in validations:
                row_validator.validate(condition, error_message)

            if row_validator.is_valid():
                assert person_id is not None
                assert person_full_name is not None

                person = Person(
                    person_id=person_id,
                    person_full_name=person_full_name,
                )
                universe.person_store.insert(person_id, person)

    if universe.verbose_mode:
        print(parser.get_results())
