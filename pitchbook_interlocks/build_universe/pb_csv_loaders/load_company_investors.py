from datetime import datetime
from pitchbook_interlocks.models.data_models import Company, Investment
from pitchbook_interlocks.build_universe.models.pb_csv_parser import PBCSVParser
from pitchbook_interlocks.models.universe import Universe


def load_company_investors(file_path: str, universe: Universe) -> None:
    parser = PBCSVParser("Company Investors", file_path)
    for row, validator in parser.rows():
        company_id: str | None = parser.parse_string(row["CompanyID"])
        investor_id: str | None = parser.parse_string(row["InvestorID"])
        investment_date: datetime | None = parser.parse_date_obj(row["InvestorSince"])

        with validator as row_validator:
            validations = [
                (
                    company_id is not None
                    and universe.company_store.exists(company_id),
                    "Invalid company_id: is None or does not exist",
                ),
                (
                    investor_id is not None
                    and universe.investor_store.exists(investor_id),
                    "Invalid investor_id: is None or does not exist",
                ),
                (
                    investment_date is not None,
                    "Invalid investment_date: is None",
                ),
            ]

            for condition, error_message in validations:
                row_validator.validate(condition, error_message)

            if row_validator.is_valid():
                assert company_id is not None
                assert investor_id is not None
                assert investment_date is not None

                investment = Investment(company_id, investor_id, investment_date)

                investor = universe.investor_store.get(investor_id)
                investor.investments.add(investment)

                company: Company = universe.company_store.get(company_id)
                company.investor_investments.add(investment)

    if universe.verbose_mode:
        print(parser.get_results())
