from datetime import datetime
from pitchbook_interlocks.models.universe import Universe
from pitchbook_interlocks.build_universe.models.pb_csv_parser import PBCSVParser
from pitchbook_interlocks.build_universe.pb_csv_loaders.load_board_members import (
    add_board_member_to_universe,
)


def load_company_advisors(file_path: str, universe: Universe) -> None:
    parser = PBCSVParser("Company Advisors", file_path)

    for row, validator in parser.rows():
        person_id: str | None = parser.parse_string(row["PersonID"])
        company_id: str | None = parser.parse_string(row["EntityID"])
        advisory_title: str | None = parser.parse_string(row["AdvisoryTitle"])
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
                    company_id is not None
                    and universe.company_store.exists(company_id),
                    "Invalid company_id: either missing or company with id not found.",
                ),
                (
                    is_current is not None and is_current,
                    "Invalid is_current: either missing or advisor is not current.",
                ),
                (
                    advisory_title is not None
                    and advisory_title in ["Advisory Board Member", "Board Advisor"],
                    "Invalid advisory_title: is not recognized.",
                ),
            ]

            for condition, error_message in validations:
                row_validator.validate(condition, error_message)

            if row_validator.is_valid():
                assert person_id is not None
                assert company_id is not None
                assert is_current is not None

                add_board_member_to_universe(
                    person_id,
                    company_id,
                    "BOARD_ADVISOR",
                    is_current,
                    start_date,
                    end_date,
                    universe,
                )

    if universe.verbose_mode:
        print(parser.get_results())
