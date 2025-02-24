from pitchbook_interlocks.models.data_models import Investor
from pitchbook_interlocks.build_universe.models.pb_csv_parser import PBCSVParser
from pitchbook_interlocks.models.universe import Universe


def load_investors(file_path: str, universe: Universe) -> None:
    parser = PBCSVParser("Investors", file_path)

    for row, validator in parser.rows():
        investor_id: str | None = parser.parse_string(row["InvestorID"])
        investor_name: str | None = parser.parse_string(row["InvestorName"])

        with validator as row_validator:
            validations = [
                (investor_id is not None, "Missing investor_id"),
                (investor_name is not None, "Missing investor_name"),
            ]

            for condition, error_message in validations:
                row_validator.validate(condition, error_message)

            if row_validator.is_valid():
                assert investor_id is not None
                assert investor_name is not None
                investor = Investor(
                    investor_id=investor_id,
                    investor_name=investor_name,
                )
                universe.investor_store.insert(investor_id, investor)

    if universe.verbose_mode:
        print(parser.get_results())
