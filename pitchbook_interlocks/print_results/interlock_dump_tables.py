from pitchbook_interlocks.models.universe import Universe
from pitchbook_interlocks.print_results.models.interlock_with_context import (
    InterlockWithContext,
)
from pitchbook_interlocks.print_results.models.results_utils import ResultsUtils


def clean_row(row: list) -> list:
    return ["" if v is None else v for v in row]


def print_interlock_dump_tables(universe: Universe) -> None:
    ResultsUtils.print_csv_str(["SECTION 7: INTERLOCK DUMP TABLES"])
    print_individual_interlock_dump_table(universe)
    ResultsUtils.print_csv_str(["", ""])
    print_investor_interlock_dump_table(universe)


def build_contexts(universe: Universe, role: str) -> list[InterlockWithContext]:
    contexts = []
    if role == "person":
        for person in universe.person_store.values():
            contexts.extend(
                InterlockWithContext(interlock, universe)
                for interlock in person.interlocks
            )
    elif role == "investor":
        for investor in universe.investor_store.values():
            contexts.extend(
                InterlockWithContext(interlock, universe)
                for interlock in investor.interlocks
            )
    return contexts


def get_investment_date(universe: Universe, investor, company_id) -> str:
    if investor and investor.invested_in_company(company_id):
        return universe.investor_store.get(
            investor.investor_id
        ).earliest_investment_date(company_id)
    return ""


def print_individual_interlock_dump_table(universe: Universe) -> None:
    ResultsUtils.print_csv_str(["INTERLOCK DUMP TABLE: Individual Interlocks", ""])

    contexts = build_contexts(universe, "person")
    header = [
        "Person ID",
        "Person Name",
        "Company 1 ID",
        "Company 1 Name",
        "Start Date on Company 1 Board",
        "Company 2 ID",
        "Company 2 Name",
        "Start Date on Company 2 Board",
        "Employed By Investor?",
        "Investor ID",
        "Investor Name",
        "Position Level @ Investor",
        "Start Date @ Investor",
        "Investment Date in Company 1",
        "Investment Date in Company 2",
        "Date Ordering Job/Invest/Board Person/Company 1",
        "Date Ordering Job/Invest/Board Person/Company 2",
    ]
    ResultsUtils.print_csv_str(header)

    for ctx in contexts:
        interlock = ctx.interlock
        person = universe.person_store.get(interlock.entity_id)
        comp1 = universe.company_store.get(interlock.company_1_id)
        comp2 = universe.company_store.get(interlock.company_2_id)
        investor = ctx.assigned_investor

        row = [
            interlock.entity_id,
            person.person_full_name,
            interlock.company_1_id,
            comp1.company_name,
            person.start_date_on_board(interlock.company_1_id),
            interlock.company_2_id,
            comp2.company_name,
            person.start_date_on_board(interlock.company_2_id),
            investor is not None,
            investor.investor_id if investor else "",
            investor.investor_name if investor else "",
            person.position_level_at_investor(investor.investor_id) if investor else "",
            person.start_date_at_investor(investor.investor_id) if investor else "",
            get_investment_date(universe, investor, interlock.company_1_id),
            get_investment_date(universe, investor, interlock.company_2_id),
            (
                ctx.investor_board_seat_orderings[0]["ordering_type"]
                if ctx.investor_board_seat_orderings
                else ""
            ),
            (
                ctx.investor_board_seat_orderings[1]["ordering_type"]
                if ctx.investor_board_seat_orderings
                else ""
            ),
        ]
        ResultsUtils.print_csv_str(clean_row(row))


def print_investor_interlock_dump_table(universe: Universe) -> None:
    ResultsUtils.print_csv_str(["INTERLOCK DUMP TABLE: Investor Interlocks", ""])

    contexts = build_contexts(universe, "investor")
    header = [
        "Investor ID",
        "Investor Name",
        "Person 1 ID",
        "Person 1 Name",
        "Person 1 Position Level @ Investor",
        "Person 1 Start Date @ Investor",
        "Company 1 ID",
        "Company 1 Name",
        "Person 1 Start Date on Company 1 Board",
        "Person 2 ID",
        "Person 2 Name",
        "Person 2 Position Level @ Investor",
        "Person 2 Start Date @ Investor",
        "Company 2 ID",
        "Company 2 Name",
        "Person 2 Start Date on Company 2 Board",
        "Investment Date in Company 1",
        "Investment Date in Company 2",
        "Date Ordering Job/Invest/Board Person/Company 1",
        "Date Ordering Job/Invest/Board Person/Company 2",
    ]
    ResultsUtils.print_csv_str(header)

    for ctx in contexts:
        investor = ctx.assigned_investor
        assert investor is not None
        p1 = universe.person_store.get(ctx.interlock.person_1_id)
        p2 = universe.person_store.get(ctx.interlock.person_2_id)
        comp1 = universe.company_store.get(ctx.interlock.company_1_id)
        comp2 = universe.company_store.get(ctx.interlock.company_2_id)

        row = [
            investor.investor_id,
            investor.investor_name,
            ctx.interlock.person_1_id,
            p1.person_full_name,
            p1.position_level_at_investor(investor.investor_id),
            p1.start_date_at_investor(investor.investor_id),
            ctx.interlock.company_1_id,
            comp1.company_name,
            p1.start_date_on_board(ctx.interlock.company_1_id),
            ctx.interlock.person_2_id,
            p2.person_full_name,
            p2.position_level_at_investor(investor.investor_id),
            p2.start_date_at_investor(investor.investor_id),
            ctx.interlock.company_2_id,
            comp2.company_name,
            p2.start_date_on_board(ctx.interlock.company_2_id),
            get_investment_date(universe, investor, ctx.interlock.company_1_id),
            get_investment_date(universe, investor, ctx.interlock.company_2_id),
            (
                ctx.investor_board_seat_orderings[0]["ordering_type"]
                if ctx.investor_board_seat_orderings
                else ""
            ),
            (
                ctx.investor_board_seat_orderings[1]["ordering_type"]
                if ctx.investor_board_seat_orderings
                else ""
            ),
        ]
        ResultsUtils.print_csv_str(clean_row(row))
