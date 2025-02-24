from pitchbook_interlocks.models.universe import Universe
from pitchbook_interlocks.print_results.models.interlock_with_context import (
    InterlockWithContext,
)
from pitchbook_interlocks.print_results.models.results_utils import ResultsUtils


def print_individual_interlock_tables(universe: Universe) -> None:
    ResultsUtils.print_csv_str(["SECTION 4: INDIVIDUAL INTERLOCK TABLES"])
    ResultsUtils.print_csv_str([""])

    interlocks_with_context: list[InterlockWithContext] = []
    for person in universe.person_store.values():
        for interlock in person.interlocks:
            interlocks_with_context.append(InterlockWithContext(interlock, universe))

    print_individual_interlocks_investment_table(interlocks_with_context)
    print_individual_interlocks_ordering_table(interlocks_with_context)


def print_individual_interlocks_investment_table(
    interlocks_with_context: list[InterlockWithContext],
) -> None:
    ResultsUtils.print_csv_str(["INDIVIDUAL INTERLOCK DATA TABLE: Investment"])

    num_individual_interlocks: int = len(interlocks_with_context)
    num_employed_at_investor: int = sum(
        1 for x in interlocks_with_context if x.assigned_investor is not None
    )
    num_invest_both: int = sum(
        1
        for x in interlocks_with_context
        if x.assigned_investor is not None and x.investor_invest_in_count == 2
    )
    num_invest_one: int = sum(
        1
        for x in interlocks_with_context
        if x.assigned_investor is not None and x.investor_invest_in_count == 1
    )
    num_invest_neither: int = sum(
        1
        for x in interlocks_with_context
        if x.assigned_investor is not None and x.investor_invest_in_count == 0
    )

    ResultsUtils.print_csv_str(
        [
            "Employment Status",
            "Invested In:",
            "# Interlocks",
            "% of Individual Interlocks",
        ]
    )
    ResultsUtils.print_csv_str(
        [
            "TOTAL",
            "TOTAL",
            num_individual_interlocks,
            ResultsUtils.pct_str(num_individual_interlocks, num_individual_interlocks),
        ]
    )
    ResultsUtils.print_csv_str(
        [
            "Not Employed",
            "n/a",
            num_individual_interlocks - num_employed_at_investor,
            ResultsUtils.pct_str(
                (num_individual_interlocks - num_employed_at_investor),
                num_individual_interlocks,
            ),
        ]
    )
    ResultsUtils.print_csv_str(
        [
            "Employed",
            "Both",
            num_invest_both,
            ResultsUtils.pct_str(num_invest_both, num_individual_interlocks),
        ]
    )
    ResultsUtils.print_csv_str(
        [
            "Employed",
            "One",
            num_invest_one,
            ResultsUtils.pct_str(num_invest_one, num_individual_interlocks),
        ]
    )
    ResultsUtils.print_csv_str(
        [
            "Employed",
            "Neither",
            num_invest_neither,
            ResultsUtils.pct_str(num_invest_neither, num_individual_interlocks),
        ]
    )
    ResultsUtils.print_csv_str([""])


def print_individual_interlocks_ordering_table(
    interlocks_with_context: list[InterlockWithContext],
) -> None:
    ResultsUtils.print_csv_str(
        [
            "INDIVIDUAL INTERLOCK DATA TABLE: Orderings (For Individual Interlocks Where Person Is Employed)"
        ]
    )

    total_board_seats = 0
    missing_count = 0
    ordering_counts: dict[str, int] = {}
    ordering_gap_day_lists: dict[str, list[float]] = {}

    for interlock in interlocks_with_context:
        for ordering in interlock.investor_board_seat_orderings:
            total_board_seats += 1
            ordering_type = ordering["ordering_type"]
            if ordering_type == InterlockWithContext.MISSING_DATA:
                missing_count += 1
            else:
                ordering_counts[ordering_type] = (
                    ordering_counts.get(ordering_type, 0) + 1
                )
                if ordering["gap_two"] is not None:
                    ordering_gap_day_lists.setdefault(ordering_type, []).append(
                        ordering["gap_two"]
                    )

    ResultsUtils.print_csv_str(["Total Board Seats", total_board_seats])
    ResultsUtils.print_csv_str(["Missing Data", missing_count])
    ResultsUtils.print_csv_str([""])

    full_count = total_board_seats - missing_count
    ResultsUtils.print_csv_str(["Ordering", "# Board Seats", "% of Full Board Seats"])
    for ordering_type, count in sorted(
        ordering_counts.items(), key=lambda x: x[1], reverse=True
    ):
        percentage = ResultsUtils.pct_str(count, full_count)
        ResultsUtils.print_csv_str([ordering_type, count, percentage])
    ResultsUtils.print_csv_str([""])

    for ordering_type, gap_list in ordering_gap_day_lists.items():
        if gap_list:
            median_days = ResultsUtils.compute_stats(gap_list)["Median (Days)"]
            ResultsUtils.print_csv_str(
                [f"Median Gap (gap_two) for {ordering_type}", median_days]
            )
    ResultsUtils.print_csv_str([""])
