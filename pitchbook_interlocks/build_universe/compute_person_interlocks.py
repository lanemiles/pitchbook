from pitchbook_interlocks.models.data_models import (
    Company,
    Person,
    Interlock,
)
from pitchbook_interlocks.models.universe import Universe
import itertools
from typing import Iterator, Tuple


def compute_person_board_seat_interlock_combinations(
    person: Person,
) -> Iterator[Tuple[str, str]]:
    return itertools.combinations((seat.company_id for seat in person.board_seats), 2)


def compute_person_interlocks(universe: Universe) -> None:
    for person in universe.person_store.values():
        for (
            company_1_id,
            company_2_id,
        ) in compute_person_board_seat_interlock_combinations(person):
            company_1: Company | None = universe.company_store.get(company_1_id)
            company_2: Company | None = universe.company_store.get(company_2_id)
            if (
                company_1
                and company_2
                and company_2.company_id in company_1.competitors
            ):

                interlock = Interlock(
                    entity_id=person.person_id,
                    entity_type=Interlock.PERSON_INTERLOCK,
                    person_1_id=person.person_id,
                    company_1_id=company_1.company_id,
                    person_2_id=person.person_id,
                    company_2_id=company_2.company_id,
                )

                person.interlocks.add(interlock)
                company_1.person_interlocks.add(interlock)
                company_2.person_interlocks.add(interlock)
