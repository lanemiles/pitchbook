from pitchbook_interlocks.build_universe.compute_investor_interlocks import (
    compute_investor_interlocks,
)
from pitchbook_interlocks.build_universe.compute_person_interlocks import (
    compute_person_interlocks,
)
from pitchbook_interlocks.build_universe.pb_csv_loaders.load_company_investors import (
    load_company_investors,
)
from pitchbook_interlocks.models.universe import Universe
from pitchbook_interlocks.build_universe.remove_companies_without_competitors_and_board_members import (
    remove_companies_without_competitors_and_board_members,
)
from pitchbook_interlocks.build_universe.pb_csv_loaders.load_board_members import (
    load_board_members,
)
from pitchbook_interlocks.build_universe.pb_csv_loaders.load_companies import (
    load_companies,
)
from pitchbook_interlocks.build_universe.pb_csv_loaders.load_company_advisors import (
    load_company_advisors,
)
from pitchbook_interlocks.build_universe.pb_csv_loaders.load_competitors import (
    load_competitors,
)
from pitchbook_interlocks.build_universe.pb_csv_loaders.load_employees import (
    load_employees,
)
from pitchbook_interlocks.build_universe.pb_csv_loaders.load_investors import (
    load_investors,
)
from pitchbook_interlocks.build_universe.pb_csv_loaders.load_people import load_people


def build_universe(universe: Universe):
    print("Loading data from CSV files...")
    load_companies(universe.get_pb_csv_path("Company.csv"), universe)
    load_investors(universe.get_pb_csv_path("Investor.csv"), universe)
    load_people(universe.get_pb_csv_path("Person.csv"), universe)

    load_company_investors(
        universe.get_pb_csv_path("CompanyInvestorRelation.csv"), universe
    )
    load_employees(universe.get_pb_csv_path("PersonPositionRelation.csv"), universe)
    load_board_members(
        universe.get_pb_csv_path("PersonBoardSeatRelation.csv"), universe
    )
    load_company_advisors(
        universe.get_pb_csv_path("PersonAdvisoryRelation.csv"), universe
    )
    load_competitors(
        universe.get_pb_csv_path("CompanyCompetitorRelation.csv"), universe
    )

    print("Removing companies without competitors and board members...")
    remove_companies_without_competitors_and_board_members(universe)

    print("Computing interlocks...")
    compute_person_interlocks(universe)
    compute_investor_interlocks(universe)

    print("Calculating results and writing to results.csv...")
