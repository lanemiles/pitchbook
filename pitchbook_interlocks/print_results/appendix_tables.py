from pitchbook_interlocks.models.universe import Universe
from pitchbook_interlocks.print_results.models.results_utils import ResultsUtils
from pitchbook_interlocks.print_results.models.interlock_breakdown_result import (
    InterlockBreakdownResult,
)


def print_appendix_tables(universe: Universe) -> None:
    ResultsUtils.print_csv_str(["SECTION 6: APPENDIX TABLES"])
    ResultsUtils.print_csv_str([""])

    companies_list = list(universe.company_store.values())

    ResultsUtils.print_csv_str(["APPENDIX TABLE: Industry Subsector"])
    ResultsUtils.print_csv_str(
        [
            "Min Board Size",
            "Industry Sector",
            "Industry Subsector",
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
        sector_subsector_map = ResultsUtils.group_companies_by_two_properties(
            filtered_companies,
            lambda c: c.grouped_industry_sector,
            lambda c: c.grouped_industry_subsector,
            universe.company_store.values(),
        )
        for sector, subsector_dict in sector_subsector_map.items():
            for subsector, group_companies in subsector_dict.items():
                breakdown = InterlockBreakdownResult(group_companies)
                ResultsUtils.print_csv_str(
                    [
                        min_board_members,
                        sector,
                        subsector,
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
