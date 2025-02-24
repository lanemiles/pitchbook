from pitchbook_interlocks.models.universe import Universe
from pitchbook_interlocks.print_results.company_attribute_tables import (
    print_company_attribute_tables,
)

from pitchbook_interlocks.print_results.individual_interlock_tables import (
    print_individual_interlock_tables,
)
from pitchbook_interlocks.print_results.investor_interlock_tables import (
    print_investor_interlock_tables,
)
from pitchbook_interlocks.print_results.overview_tables import print_overview_tables
from pitchbook_interlocks.print_results.appendix_tables import print_appendix_tables
from pitchbook_interlocks.print_results.interlock_dump_tables import (
    print_interlock_dump_tables,
)
from pitchbook_interlocks.print_results.paper_tables import print_paper_tables


def print_results(universe: Universe) -> None:
    print_paper_tables(universe)
    print()
    print()
    print_overview_tables(universe)
    print()
    print()
    print_company_attribute_tables(universe)
    print()
    print()
    print_individual_interlock_tables(universe)
    print()
    print()
    print_investor_interlock_tables(universe)
    print()
    print()
    print_appendix_tables(universe)
    print()
    print()
    print_interlock_dump_tables(universe)
