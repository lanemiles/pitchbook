from datetime import datetime
from pitchbook_interlocks.models.data_models import Company
from pitchbook_interlocks.build_universe.models.pb_csv_parser import (
    PBCSVParser,
)
from pitchbook_interlocks.models.universe import Universe


def load_companies(file_path: str, universe: Universe) -> None:
    parser = PBCSVParser("Companies", file_path)

    for row, validator in parser.rows():
        company_id: str | None = parser.parse_string(row["CompanyID"])
        company_name: str | None = parser.parse_string(row["CompanyName"])
        business_status: str | None = parser.parse_string(row["BusinessStatus"])
        ownership_status: str | None = parser.parse_string(row["OwnershipStatus"])
        primary_pb_industry_sector: str | None = parser.parse_string(
            row["PrimaryIndustrySector"]
        )
        primary_pb_industry_group: str | None = parser.parse_string(
            row["PrimaryIndustryGroup"]
        )
        primary_pb_industry_code: str | None = parser.parse_string(
            row["PrimaryIndustryCode"]
        )
        revenue: float | None = parser.parse_float(row["Revenue"])
        revenue_period_end_date: datetime | None = parser.parse_date_obj(
            row["PeriodEndDate"]
        )

        with validator as row_validator:
            validations = [
                (company_id is not None, "Invalid company_id: is None"),
                (company_name is not None, "Invalid company_name: is None"),
            ]

            for condition, error_message in validations:
                row_validator.validate(condition, error_message)

            if row_validator.is_valid():
                assert company_id is not None
                assert company_name is not None
                company = Company(
                    company_id=company_id,
                    company_name=company_name,
                    revenue=revenue,
                    revenue_period_end_date=revenue_period_end_date,
                    business_status=business_status,
                    ownership_status=ownership_status,
                    primary_pb_industry_sector=primary_pb_industry_sector,
                    primary_pb_industry_group=primary_pb_industry_group,
                    primary_pb_industry_code=primary_pb_industry_code,
                )
                universe.company_store.insert(company_id, company)

    if universe.verbose_mode:
        print(parser.get_results())
