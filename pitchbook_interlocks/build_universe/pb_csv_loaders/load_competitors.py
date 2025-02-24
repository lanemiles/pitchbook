from pitchbook_interlocks.build_universe.models.pb_csv_parser import PBCSVParser
from pitchbook_interlocks.models.universe import Universe


def load_competitors(file_path: str, universe: Universe) -> None:
    parser = PBCSVParser("Company Competitors", file_path)

    for row, validator in parser.rows():
        company_id: str | None = parser.parse_string(row["CompanyID"])
        competitor_id: str | None = parser.parse_string(row["CompetitorID"])

        with validator as row_validator:
            validations = [
                (
                    company_id is not None
                    and universe.company_store.exists(company_id),
                    "Invalid company_id: either missing or not found in universe.",
                ),
                (
                    competitor_id is not None
                    and universe.company_store.exists(competitor_id),
                    "Invalid competitor_id: either missing or not found in universe.",
                ),
            ]

            for condition, error_message in validations:
                row_validator.validate(condition, error_message)

            if row_validator.is_valid():
                assert company_id is not None
                assert competitor_id is not None
                company = universe.company_store.get(company_id)
                company.competitors.add(competitor_id)

                competitor = universe.company_store.get(competitor_id)
                competitor.competitors.add(company_id)

    if universe.verbose_mode:
        print(parser.get_results())
