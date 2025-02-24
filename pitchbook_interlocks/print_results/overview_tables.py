from pitchbook_interlocks.models.data_models import Person
from pitchbook_interlocks.print_results.models.results_utils import ResultsUtils
from pitchbook_interlocks.print_results.models.interlock_breakdown_result import (
    InterlockBreakdownResult,
)
from pitchbook_interlocks.models.universe import Universe


def print_overview_tables(universe: Universe) -> None:
    companies_list = list(universe.company_store.values())
    investors_list = list(universe.investor_store.values())
    people_list = list(universe.person_store.values())

    ResultsUtils.print_csv_str(["SECTION 2: OVERVIEW TABLES"])
    ResultsUtils.print_csv_str([""])
    ResultsUtils.print_csv_str(["OVERVIEW: Overview Table"])
    ResultsUtils.print_csv_str(["# Companies Total", len(companies_list)])
    ResultsUtils.print_csv_str(["# Investors Total", len(investors_list)])
    ResultsUtils.print_csv_str(["# People Total", len(people_list)])
    ResultsUtils.print_csv_str([""])

    ResultsUtils.print_csv_str(["OVERVIEW TABLE: Company Interlock"])
    ResultsUtils.print_csv_str(
        [
            "Min Board Size",
            "# Companies",
            "",
            "# Companies ANY Interlock",
            "% Companies ANY Interlock",
            "",
            " Companies INDIVIDUAL Interlock",
            "% Companies INDIVIDUAL Interlock",
            "",
            "# Companies INVESTOR Interlock",
            "% Companies INVESTOR Interlock",
        ]
    )
    for min_board_members in [1, 3, 5]:
        filtered_companies = (
            ResultsUtils.filter_to_companies_with_at_least_n_board_members(
                companies_list, min_board_members
            )
        )
        interlock_breakdown = InterlockBreakdownResult(filtered_companies)
        ResultsUtils.print_csv_str(
            [
                min_board_members,
                interlock_breakdown.num_companies,
                "",
                interlock_breakdown.num_companies_any_interlock,
                interlock_breakdown.pct_companies_any_interlock,
                "",
                interlock_breakdown.num_companies_person_interlock,
                interlock_breakdown.pct_companies_person_interlock,
                "",
                interlock_breakdown.num_companies_investor_interlock,
                interlock_breakdown.pct_companies_investor_interlock,
            ]
        )
    ResultsUtils.print_csv_str([""])

    ResultsUtils.print_csv_str(["OVERVIEW: Individual Employment Table"])
    ResultsUtils.print_csv_str(
        [
            "# People",
            "# People With 1+ Investor Job",
            "% of Individuals With Interlock With 1+ Investor Job",
        ]
    )
    people_with_interlock: list[Person] = (
        ResultsUtils.filter_to_people_with_individual_interlock(people_list)
    )
    num_people_with_interlock: int = len(people_with_interlock)
    num_people_with_investor_job: int = len(
        ResultsUtils.filter_to_people_with_investor_job(people_with_interlock)
    )
    pct_people_with_investor_job: str = ResultsUtils.pct_str(
        num_people_with_investor_job, num_people_with_interlock
    )
    ResultsUtils.print_csv_str(
        [
            num_people_with_interlock,
            num_people_with_investor_job,
            pct_people_with_investor_job,
        ]
    )
    ResultsUtils.print_csv_str([""])
