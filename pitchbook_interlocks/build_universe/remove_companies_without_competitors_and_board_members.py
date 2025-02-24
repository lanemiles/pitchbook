from pitchbook_interlocks.models.universe import Universe


def remove_companies_without_competitors_and_board_members(universe: Universe) -> None:
    to_remove: set[str] = set()
    for company in universe.company_store.values():
        if len(company.competitors) == 0 or len(company.board_members) == 0:
            to_remove.add(company.company_id)

    if universe.verbose_mode:
        print(
            f"Removing {len(to_remove)} companies without competitors or board members"
        )

    delete_companies(universe, to_remove)


def delete_companies(universe: Universe, company_ids_to_delete: set[str]) -> None:

    # 1. Remove companies from the company store.
    for cid in company_ids_to_delete:
        universe.company_store.remove(cid)

    # 2. Clean up references in investors.
    for investor in universe.investor_store.values():
        # Remove board seats whose company_id is in delete_ids.
        investor.board_seats = {
            bm
            for bm in investor.board_seats
            if bm.company_id not in company_ids_to_delete
        }
        # Remove investments referring to a deleted company.
        investor.investments = {
            inv
            for inv in investor.investments
            if inv.company_id not in company_ids_to_delete
        }

    # 3. Clean up references in persons.
    for person in universe.person_store.values():
        # Remove board seats that refer to deleted companies.
        person.board_seats = {
            bm
            for bm in person.board_seats
            if bm.company_id not in company_ids_to_delete
        }

    # 4. Clean up competitor references in remaining companies.
    for comp in universe.company_store.values():
        # Remove the deleted company ids from the competitors set.
        comp.competitors.difference_update(company_ids_to_delete)
