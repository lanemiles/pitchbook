from pitchbook_interlocks.models.universe import Universe
from pitchbook_interlocks.print_results.models.interlock_with_context import (
    InterlockWithContext,
)
from pitchbook_interlocks.print_results.models.results_utils import ResultsUtils


def print_investor_interlock_tables(universe: Universe) -> None:
    ResultsUtils.print_csv_str(["SECTION 5: INVESTOR INTERLOCK TABLES"])
    ResultsUtils.print_csv_str([""])

    interlocks_with_context: list[InterlockWithContext] = []
    for investor in universe.investor_store.values():
        for interlock in investor.interlocks:
            interlocks_with_context.append(InterlockWithContext(interlock, universe))

    print_investor_interlocks_investment_table(interlocks_with_context)
    print_investor_interlocks_position_levels_table(interlocks_with_context)
    print_investor_interlocks_ordering_table(interlocks_with_context)


def print_investor_interlocks_investment_table(
    interlocks_with_context: list[InterlockWithContext],
) -> None:
    ResultsUtils.print_csv_str(["INVESTOR INTERLOCK DATA TABLE: Investment"])

    num_investor_interlocks: int = len(interlocks_with_context)
    num_investor_interlocks_invest_both: int = 0
    num_investor_interlocks_invest_one: int = 0
    num_investor_interlocks_invest_neither: int = 0
    num_investor_interlocks_invest_neither_but_invest_shared_competitor: int = 0

    for interlock in interlocks_with_context:
        invest_sum = interlock.investor_invest_in_count
        if invest_sum == 2:
            num_investor_interlocks_invest_both += 1
        elif invest_sum == 1:
            num_investor_interlocks_invest_one += 1
        else:
            num_investor_interlocks_invest_neither += 1
            if interlock.investor_invest_in_shared_competitor:
                num_investor_interlocks_invest_neither_but_invest_shared_competitor += 1

    ResultsUtils.print_csv_str(
        [
            "Invested In:",
            "# Interlocks",
            "% of Investor Interlocks",
        ]
    )
    ResultsUtils.print_csv_str(
        [
            "TOTAL",
            num_investor_interlocks,
            ResultsUtils.pct_str(num_investor_interlocks, num_investor_interlocks),
        ]
    )
    ResultsUtils.print_csv_str(
        [
            "Both",
            num_investor_interlocks_invest_both,
            ResultsUtils.pct_str(
                num_investor_interlocks_invest_both, num_investor_interlocks
            ),
        ]
    )
    ResultsUtils.print_csv_str(
        [
            "One",
            num_investor_interlocks_invest_one,
            ResultsUtils.pct_str(
                num_investor_interlocks_invest_one, num_investor_interlocks
            ),
        ]
    )
    ResultsUtils.print_csv_str(
        [
            "Neither",
            num_investor_interlocks_invest_neither,
            ResultsUtils.pct_str(
                num_investor_interlocks_invest_neither, num_investor_interlocks
            ),
        ]
    )
    ResultsUtils.print_csv_str([""])

    ResultsUtils.print_csv_str(
        [
            "Invested In:",
            "Invest in Shared Competitor",
            "# of Interlocks",
            "% of Invest Neither Interlocks",
        ]
    )
    ResultsUtils.print_csv_str(
        [
            "Neither",
            "Yes",
            num_investor_interlocks_invest_neither_but_invest_shared_competitor,
            ResultsUtils.pct_str(
                num_investor_interlocks_invest_neither_but_invest_shared_competitor,
                num_investor_interlocks_invest_neither,
            ),
        ]
    )
    ResultsUtils.print_csv_str(
        [
            "Neither",
            "No",
            (
                num_investor_interlocks_invest_neither
                - num_investor_interlocks_invest_neither_but_invest_shared_competitor
            ),
            ResultsUtils.pct_str(
                (
                    num_investor_interlocks_invest_neither
                    - num_investor_interlocks_invest_neither_but_invest_shared_competitor
                ),
                num_investor_interlocks_invest_neither,
            ),
        ]
    )
    ResultsUtils.print_csv_str([""])


def print_investor_interlocks_position_levels_table(
    interlocks_with_context: list[InterlockWithContext],
) -> None:
    ResultsUtils.print_csv_str(["INVESTOR INTERLOCK DATA TABLE: Position Levels"])
    ResultsUtils.print_csv_str(["Position Level", "# Occurences", "% Occurences"])

    position_level_map: dict[str, int] = {}
    total_position_levels: int = 0

    for interlock in interlocks_with_context:
        for position_level in interlock.position_levels:
            position_level_map[position_level] = (
                position_level_map.get(position_level, 0) + 1
            )
            total_position_levels += 1

    for position_level, count in sorted(
        position_level_map.items(), key=lambda x: x[1], reverse=True
    ):
        percentage = ResultsUtils.pct_str(count, total_position_levels)
        ResultsUtils.print_csv_str([position_level, count, percentage])
    ResultsUtils.print_csv_str([""])


def print_investor_interlocks_ordering_table(
    interlocks_with_context: list[InterlockWithContext],
) -> None:
    ResultsUtils.print_csv_str(["INVESTOR INTERLOCK DATA TABLE: Orderings"])

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
