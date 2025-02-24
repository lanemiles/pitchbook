from pitchbook_interlocks.models.data_models import BoardMember
from pitchbook_interlocks.models.universe import Universe
from pitchbook_interlocks.build_universe.models.pb_csv_parser import (
    PBCSVParser,
)
from datetime import datetime


def load_board_members(file_path: str, universe: Universe) -> None:
    parser = PBCSVParser("Board Members", file_path)

    for row, validator in parser.rows():
        person_id: str | None = parser.parse_string(row["PersonID"])
        company_id: str | None = parser.parse_string(row["CompanyID"])
        role_on_board: str | None = parser.parse_string(row["RoleOnBoard"])
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
                (role_on_board is not None, "Role on board is missing."),
                (
                    is_current is not None and is_current,
                    "Invalid is_current: either missing or board member is not current.",
                ),
            ]

            for condition, error_message in validations:
                row_validator.validate(condition, error_message)

            if validator.is_valid():
                assert person_id is not None
                assert company_id is not None
                assert role_on_board is not None
                assert is_current is not None

                add_board_member_to_universe(
                    person_id,
                    company_id,
                    role_on_board,
                    is_current,
                    start_date,
                    end_date,
                    universe,
                )

    if universe.verbose_mode:
        print(parser.get_results())


def add_board_member_to_universe(
    person_id: str,
    company_id: str,
    role_on_board: str,
    is_current: bool,
    start_date: datetime | None,
    end_date: datetime | None,
    universe: Universe,
) -> None:
    board_member = BoardMember(
        person_id=person_id,
        company_id=company_id,
        role_on_board=role_on_board,
        is_current=is_current,
        start_date=start_date,
        end_date=end_date,
    )

    company = universe.company_store.get(company_id)
    company.board_members.add(board_member)

    person = universe.person_store.get(person_id)
    person.board_seats.add(board_member)

    for job in person.investor_jobs:
        investor = universe.investor_store.get(job.investor_id)
        if investor:
            investor.board_seats.add(board_member)
