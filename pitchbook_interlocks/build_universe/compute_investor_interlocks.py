from pitchbook_interlocks.models.data_models import (
    Interlock,
    Investor,
    Company,
)
from pitchbook_interlocks.models.universe import Universe
import itertools


def compute_investor_board_seat_interlock_combinations(
    investor: Investor,
) -> list[tuple[tuple[str, str], tuple[str, str]]]:
    seats = [(seat.person_id, seat.company_id) for seat in investor.board_seats]
    return list(itertools.combinations(seats, 2))


def compute_investor_interlocks(universe: Universe) -> None:
    for investor in universe.investor_store.values():
        combos = compute_investor_board_seat_interlock_combinations(investor)
        for (person1, company1), (person2, company2) in combos:
            if person1 != person2 and company1 != company2:
                comp1: Company | None = universe.company_store.get(company1)
                comp2: Company | None = universe.company_store.get(company2)
                if comp1 and comp2 and company2 in comp1.competitors:
                    interlock = Interlock(
                        entity_id=investor.investor_id,
                        entity_type=Interlock.INVESTOR_INTERLOCK,
                        person_1_id=person1,
                        company_1_id=comp1.company_id,
                        person_2_id=person2,
                        company_2_id=comp2.company_id,
                    )
                    investor.interlocks.add(interlock)
                    comp1.investor_interlocks.add(interlock)
                    comp2.investor_interlocks.add(interlock)
