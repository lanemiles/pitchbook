from pitchbook_interlocks.models.universe import Universe
from pitchbook_interlocks.print_results.models.interlock_with_context import (
    InterlockWithContext,
)
from pitchbook_interlocks.print_results.models.results_utils import ResultsUtils


def print_paper_tables(universe: Universe) -> None:
    ResultsUtils.print_csv_str(["SECTION 1: PAPER TABLES"])
    table_functions = [
        print_table_1,
        print_table_2,
        print_table_3,
        print_table_4,
        print_table_5,
        print_table_6,
        print_table_7,
        print_table_8,
        print_table_9,
        print_table_10,
    ]
    for table_func in table_functions:
        table_func(universe)
        print()


def has_overlap(company) -> bool:
    return bool(company.person_interlocks or company.investor_interlocks)


def count_overlap(companies: list) -> int:
    return sum(1 for c in companies if has_overlap(c))


def print_grouped_overlap(universe: Universe, companies: list, group_func) -> None:
    grouped = ResultsUtils.group_companies_by_property(
        companies, group_func, universe.company_store.values()
    )
    for group_label, cos in grouped.items():
        cos_with_overlap = count_overlap(cos)
        pct_cos = ResultsUtils.pct_str(cos_with_overlap, len(cos))
        ResultsUtils.print_csv_str([group_label, len(cos), cos_with_overlap, pct_cos])
    total = len(companies)
    total_overlap = count_overlap(companies)
    ResultsUtils.print_csv_str(
        ["Total", total, total_overlap, ResultsUtils.pct_str(total_overlap, total)]
    )


def group_small_counts(counts: dict, total: int, threshold: float = 0.01) -> dict:
    grouped = {}
    for key, count in counts.items():
        if count / total < threshold:
            grouped["Other"] = grouped.get("Other", 0) + count
        else:
            grouped[key] = count
    return grouped


def print_table_1(universe: Universe) -> None:
    print("Table 1")
    count_maps = {
        "Companies": len(universe.company_store.values()),
        "Investors": len(universe.investor_store.values()),
        "People": len(universe.person_store.values()),
    }
    ResultsUtils.print_csv_str(["Object Type", "# in Dataset"])
    for object_type, count in count_maps.items():
        ResultsUtils.print_csv_str([object_type, count])


def print_table_2(universe: Universe) -> None:
    print("Table 2")
    ResultsUtils.print_csv_str(
        [
            "Overlap Type",
            "# of Companies Involved In 1+ Overlap",
            "% of Companies Involved In 1+ Overlap",
        ]
    )
    overlap_types_map = {
        "Person Overlaps": lambda c: c.person_interlocks,
        "Investor Overlaps": lambda c: c.investor_interlocks,
        "All Overlaps": lambda c: c.person_interlocks | c.investor_interlocks,
    }
    total_companies = len(universe.company_store.values())
    for overlap_type, filter_func in overlap_types_map.items():
        cos_with_overlap = len(
            list(filter(filter_func, universe.company_store.values()))
        )
        pct_cos = ResultsUtils.pct_str(cos_with_overlap, total_companies)
        ResultsUtils.print_csv_str([overlap_type, cos_with_overlap, pct_cos])


def print_table_3(universe: Universe) -> None:
    print("Table 3")
    ResultsUtils.print_csv_str(
        [
            "Known Board Size",
            "# of Companies",
            "# of Companies Involved In 1+ Overlap",
            "% of Companies Involved In 1+ Overlap",
        ]
    )
    for min_board_size in ResultsUtils.MIN_BOARD_MEMBER_THRESHOLDS:
        companies = ResultsUtils.filter_to_companies_with_at_least_n_board_members(
            universe.company_store.values(), min_board_size
        )
        cos_with_overlap = count_overlap(companies)
        pct_cos = ResultsUtils.pct_str(cos_with_overlap, len(companies))
        ResultsUtils.print_csv_str(
            [
                f"{min_board_size}+ Board Members",
                len(companies),
                cos_with_overlap,
                pct_cos,
            ]
        )


def print_table_4(universe: Universe) -> None:
    print("Table 4")
    ResultsUtils.print_csv_str(
        [
            "Last Reported Revenue (in Millions)",
            "# of Companies",
            "# of Companies Involved In 1+ Overlap",
            "% of Companies Involved In 1+ Overlap",
        ]
    )
    companies = ResultsUtils.filter_to_companies_with_at_least_n_board_members(
        universe.company_store.values(), 5
    )
    print_grouped_overlap(universe, companies, lambda c: c.grouped_revenue)


def print_table_5(universe: Universe) -> None:
    print("Table 5")
    ResultsUtils.print_csv_str(
        [
            "Ownership Status",
            "# of Companies",
            "# of Companies Involved In 1+ Overlap",
            "% of Companies Involved In 1+ Overlap",
        ]
    )
    companies = ResultsUtils.filter_to_companies_with_at_least_n_board_members(
        universe.company_store.values(), 5
    )
    print_grouped_overlap(universe, companies, lambda c: c.grouped_ownership_status)


def print_table_6(universe: Universe) -> None:
    print("Table 6")
    ResultsUtils.print_csv_str(
        [
            "Pitchbook Industry Sector",
            "# of Companies",
            "# of Companies Involved In 1+ Overlap",
            "% of Companies Involved In 1+ Overlap",
        ]
    )
    companies = ResultsUtils.filter_to_companies_with_at_least_n_board_members(
        universe.company_store.values(), 5
    )
    print_grouped_overlap(universe, companies, lambda c: c.grouped_industry_sector)


def print_table_7(universe: Universe) -> None:
    print("Table 7")
    ResultsUtils.print_csv_str(
        [
            "Individual's Investor Employment Status",
            "Employer's Investments",
            "# of Individual Overlaps",
            "% of All Individual Overlaps",
        ]
    )
    interlocks = [
        InterlockWithContext(interlock, universe)
        for person in universe.person_store.values()
        for interlock in person.interlocks
    ]
    total = len(interlocks)
    rows = [
        ("Not Employed", "n/a", lambda i: not i.assigned_investor),
        (
            "Employed",
            "Both Companies",
            lambda i: i.assigned_investor and i.investor_invest_in_count == 2,
        ),
        (
            "Employed",
            "One Company",
            lambda i: i.assigned_investor and i.investor_invest_in_count == 1,
        ),
        (
            "Employed",
            "Neither Company",
            lambda i: i.assigned_investor and i.investor_invest_in_count == 0,
        ),
    ]
    for status, investments, condition in rows:
        count_val = len(list(filter(condition, interlocks)))
        pct = ResultsUtils.pct_str(count_val, total)
        ResultsUtils.print_csv_str([status, investments, count_val, pct])
    ResultsUtils.print_csv_str(["Total", "", total, ResultsUtils.pct_str(total, total)])


def print_table_8(universe: Universe) -> None:
    print("Table 8")
    ResultsUtils.print_csv_str(
        [
            "Position Level",
            "# of Occurences in Investor Overlaps",
            "% of Occurences in Investor Overlaps",
        ]
    )
    interlocks = [
        InterlockWithContext(interlock, universe)
        for investor in universe.investor_store.values()
        for interlock in investor.interlocks
    ]
    total_positions = 0
    position_counts = {}
    for interlock in interlocks:
        total_positions += 2
        for level in interlock.position_levels:
            position_counts[level] = position_counts.get(level, 0) + 1
    grouped_counts = group_small_counts(
        position_counts, total_positions, threshold=0.01
    )
    for level, count in sorted(
        grouped_counts.items(), key=lambda x: x[1], reverse=True
    ):
        pct = ResultsUtils.pct_str(count, total_positions)
        ResultsUtils.print_csv_str([level, count, pct])
    ResultsUtils.print_csv_str(
        [
            "Total",
            total_positions,
            ResultsUtils.pct_str(total_positions, total_positions),
        ]
    )


def print_table_9(universe: Universe) -> None:
    print("Table 9")
    ResultsUtils.print_csv_str(
        [
            "Invested Invested In...",
            "# of Investor Overlaps",
            "% of Investor Overlaps",
        ]
    )
    interlocks = [
        InterlockWithContext(interlock, universe)
        for investor in universe.investor_store.values()
        for interlock in investor.interlocks
    ]
    invested_in_map = {
        "Both Companies": lambda i: i.investor_invest_in_count == 2,
        "One Company": lambda i: i.investor_invest_in_count == 1,
        "Neither Company": lambda i: i.investor_invest_in_count == 0,
    }
    for label, condition in invested_in_map.items():
        count_val = len(list(filter(condition, interlocks)))
        pct = ResultsUtils.pct_str(count_val, len(interlocks))
        ResultsUtils.print_csv_str([label, count_val, pct])
    ResultsUtils.print_csv_str(
        [
            "Total",
            len(interlocks),
            ResultsUtils.pct_str(len(interlocks), len(interlocks)),
        ]
    )


def print_table_10(universe: Universe) -> None:
    print("Table 10")
    ResultsUtils.print_csv_str(
        [
            "Company Business Status",
            "# of Companies",
            "% of Companies Involved In Any Overlap",
            "% of Companies Involved In Individual Overlap",
            "% of Companies Involved In Investor Overlap",
        ]
    )
    all_companies = ResultsUtils.filter_to_companies_with_at_least_n_board_members(
        universe.company_store.values(), 5
    )
    grouped_status = ResultsUtils.group_companies_by_property(
        all_companies,
        lambda c: c.grouped_business_status,
        universe.company_store.values(),
    )
    for status, companies in grouped_status.items():
        num_cos = len(companies)
        pct_any = ResultsUtils.pct_str(
            len(
                list(
                    filter(
                        lambda c: c.person_interlocks or c.investor_interlocks,
                        companies,
                    )
                )
            ),
            num_cos,
        )
        pct_indiv = ResultsUtils.pct_str(
            len(list(filter(lambda c: c.person_interlocks, companies))), num_cos
        )
        pct_investor = ResultsUtils.pct_str(
            len(list(filter(lambda c: c.investor_interlocks, companies))), num_cos
        )
        ResultsUtils.print_csv_str([status, num_cos, pct_any, pct_indiv, pct_investor])
    total = len(all_companies)
    ResultsUtils.print_csv_str(
        [
            "Total",
            total,
            ResultsUtils.pct_str(
                len(
                    list(
                        filter(
                            lambda c: c.person_interlocks or c.investor_interlocks,
                            all_companies,
                        )
                    )
                ),
                total,
            ),
            ResultsUtils.pct_str(
                len(list(filter(lambda c: c.person_interlocks, all_companies))), total
            ),
            ResultsUtils.pct_str(
                len(list(filter(lambda c: c.investor_interlocks, all_companies))), total
            ),
        ]
    )
