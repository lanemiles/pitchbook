from pitchbook_interlocks.models.universe import Universe
from pitchbook_interlocks.print_results.models.results_utils import ResultsUtils
from pitchbook_interlocks.print_results.models.interlock_breakdown_result import (
    InterlockBreakdownResult,
)

LIST_OF_ATTRIBUTE_TABLES = [
    {"name": "Industry Sector", "mapper": lambda c: c.grouped_industry_sector},
    {"name": "Revenue", "mapper": lambda c: c.grouped_revenue},
    {"name": "Ownership Status", "mapper": lambda c: c.grouped_ownership_status},
    {"name": "Business Status", "mapper": lambda c: c.grouped_business_status},
]


def print_company_attribute_tables(universe: Universe) -> None:
    ResultsUtils.print_csv_str(["SECTION 3: COMPANY ATTRIBUTE TABLES"])
    ResultsUtils.print_csv_str([""])

    companies_list = list(universe.company_store.values())

    for table in LIST_OF_ATTRIBUTE_TABLES:
        table_name = table["name"]
        mapper = table["mapper"]
        ResultsUtils.print_csv_str([f"COMPANY ATTRIBUTES TABLE: {table_name}"])
        ResultsUtils.print_csv_str(
            [
                "Min Board Size",
                {table_name},
                "# Companies",
                "",
                "# Companies ANY Interlock",
                "% Companies ANY Interlock",
                "",
                "# Companies INDIVIDUAL Interlock",
                "% Companies INDIVIDUAL Interlock",
                "",
                "# Companies INVESTOR Interlock",
                "% Companies INVESTOR Interlock",
            ]
        )
        for min_board_members in ResultsUtils.MIN_BOARD_MEMBER_THRESHOLDS:
            filtered_companies = (
                ResultsUtils.filter_to_companies_with_at_least_n_board_members(
                    companies_list, min_board_members
                )
            )
            attribute_map = ResultsUtils.group_companies_by_property(
                filtered_companies, mapper, universe.company_store.values()
            )
            for attribute, group_companies in attribute_map.items():
                breakdown = InterlockBreakdownResult(group_companies)
                ResultsUtils.print_csv_str(
                    [
                        min_board_members,
                        attribute,
                        breakdown.num_companies,
                        "",
                        breakdown.num_companies_any_interlock,
                        breakdown.pct_companies_any_interlock,
                        "",
                        breakdown.num_companies_person_interlock,
                        breakdown.pct_companies_person_interlock,
                        "",
                        breakdown.num_companies_investor_interlock,
                        breakdown.pct_companies_investor_interlock,
                    ]
                )
            ResultsUtils.print_csv_str([""])
        ResultsUtils.print_csv_str([""])
    ResultsUtils.print_csv_str([""])
