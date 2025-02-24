from pitchbook_interlocks.models.data_models import Company, Interlock, Investor
from pitchbook_interlocks.models.universe import Universe


class InterlockWithContext:
    # We retain a constant for missing data.
    MISSING_DATA = "MISSING DATA"

    def __init__(self, interlock: Interlock, universe: Universe) -> None:
        self.interlock: Interlock = interlock
        self.universe: Universe = universe
        self.company_1: Company = universe.company_store.get(interlock.company_1_id)
        self.company_2: Company = universe.company_store.get(interlock.company_2_id)
        self.assigned_investor: Investor | None = self._assign_investor()
        self.investor_board_seat_orderings: list[dict] = (
            self._calculate_investor_board_seat_orderings()
        )
        self.position_levels: list[str] = self._calculate_position_levels()
        self.investor_invest_in_count: int = self._calculate_investor_invest_in_count()
        self.investor_invest_in_shared_competitor: bool = (
            self._calculate_investor_invest_in_shared_competitor()
        )

    def _assign_investor(self) -> Investor | None:
        if self.interlock.entity_type == Interlock.INVESTOR_INTERLOCK:
            return self.universe.investor_store.get(self.interlock.entity_id)

        person = self.universe.person_store.get(self.interlock.person_1_id)
        if not person.investor_jobs:
            return None

        best_investor: Investor | None = None
        best_count = -1
        for investor_job in person.investor_jobs:
            investor = self.universe.investor_store.get(investor_job.investor_id)
            invest_count = sum(
                investor.invested_in_company(company_id)
                for company_id in [self.company_1.company_id, self.company_2.company_id]
            )
            if invest_count > best_count:
                best_count = invest_count
                best_investor = investor
        return best_investor

    def _calculate_investor_invest_in_count(self) -> int:
        if self.assigned_investor is None:
            return 0
        return sum(
            self.assigned_investor.invested_in_company(company_id)
            for company_id in [self.company_1.company_id, self.company_2.company_id]
        )

    def _calculate_investor_invest_in_shared_competitor(self) -> bool:
        if self.assigned_investor is None:
            return False
        shared_competitors = self.company_1.competitors & self.company_2.competitors
        return any(
            self.assigned_investor.invested_in_company(comp)
            for comp in shared_competitors
        )

    def _calculate_position_levels(self) -> list[str]:
        if self.assigned_investor is None:
            return []
        return [
            self.universe.person_store.get(pid).position_level_at_investor(
                self.assigned_investor.investor_id
            )
            for pid in [self.interlock.person_1_id, self.interlock.person_2_id]
        ]

    def _calculate_investor_board_seat_orderings(self) -> list[dict]:
        """
        For each board seat (pairing of person and company), calculate the ordering
        of the following dates:
            - Job start date at the investor (J)
            - Earliest investment date in the company (I)
            - Board seat start date at the company (B)

        Instead of grouping unknown orderings into "OTHER ORDERING", we dynamically
        sort the available dates and produce one of the six possible orderings.
        If any of the dates is missing, we return MISSING_DATA.
        """
        if self.assigned_investor is None:
            return []

        orderings = []
        pairs = [
            (self.interlock.person_1_id, self.interlock.company_1_id),
            (self.interlock.person_2_id, self.interlock.company_2_id),
        ]

        for person_id, company_id in pairs:
            person = self.universe.person_store.get(person_id)
            job_start = person.start_date_at_investor(
                self.assigned_investor.investor_id
            )
            board_start = person.start_date_on_board(company_id)
            investment_date = (
                self.assigned_investor.earliest_investment_date(company_id)
                if self.assigned_investor.invested_in_company(company_id)
                else None
            )

            if job_start is None or investment_date is None or board_start is None:
                ordering = {
                    "ordering_type": self.MISSING_DATA,
                    "gap_one": None,
                    "gap_two": None,
                }
            else:
                # Create a list of (date, label) pairs.
                dates = [
                    (job_start, "JOB"),
                    (investment_date, "INVEST"),
                    (board_start, "BOARD"),
                ]
                # Sort by date.
                sorted_dates = sorted(dates, key=lambda x: x[0])
                ordering_str = " <= ".join(label for _, label in sorted_dates)
                gap_one = (sorted_dates[1][0] - sorted_dates[0][0]).days
                gap_two = (sorted_dates[2][0] - sorted_dates[1][0]).days
                ordering = {
                    "ordering_type": ordering_str,
                    "gap_one": gap_one,
                    "gap_two": gap_two,
                }
            orderings.append(ordering)
        return orderings
