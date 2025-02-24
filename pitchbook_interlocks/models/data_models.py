from datetime import datetime
from dataclasses import dataclass, field


@dataclass(frozen=True)
class BoardMember:
    person_id: str
    company_id: str
    role_on_board: str
    is_current: bool
    start_date: datetime | None
    end_date: datetime | None


@dataclass(frozen=True)
class Employee:
    person_id: str
    investor_id: str
    full_title: str
    position_level: str
    is_current: bool
    start_date: datetime | None
    end_date: datetime | None


@dataclass(frozen=True)
class Investment:
    company_id: str
    investor_id: str
    investment_date: datetime


@dataclass(frozen=True)
class Interlock:
    entity_id: str
    entity_type: str
    person_1_id: str
    company_1_id: str
    person_2_id: str
    company_2_id: str

    PERSON_INTERLOCK = "person_interlock"
    INVESTOR_INTERLOCK = "investor_interlock"

    def __post_init__(self):
        if self.company_1_id > self.company_2_id:
            orig_company1 = self.company_1_id
            orig_person1 = self.person_1_id
            orig_company2 = self.company_2_id
            orig_person2 = self.person_2_id

            object.__setattr__(self, "company_1_id", orig_company2)
            object.__setattr__(self, "person_1_id", orig_person2)
            object.__setattr__(self, "company_2_id", orig_company1)
            object.__setattr__(self, "person_2_id", orig_person1)


@dataclass
class Company:
    company_id: str
    company_name: str
    revenue: float | None = None
    revenue_period_end_date: datetime | None = None
    business_status: str | None = None
    ownership_status: str | None = None
    primary_pb_industry_sector: str | None = None
    primary_pb_industry_group: str | None = None
    primary_pb_industry_code: str | None = None

    board_members: set[BoardMember] = field(default_factory=set)
    competitors: set[str] = field(default_factory=set)
    person_interlocks: set[Interlock] = field(default_factory=set)
    investor_interlocks: set[Interlock] = field(default_factory=set)
    investor_investments: set[Investment] = field(default_factory=set)

    @property
    def grouped_revenue(self) -> str:
        if self.revenue is None or self.revenue < 0:
            return "Unknown"
        elif 0 <= self.revenue < 5:
            return "$0M - $4.999M"
        else:
            return ">= 5M"

    @property
    def grouped_ownership_status(self) -> str:
        if self.ownership_status is None:
            return "Unknown"
        elif self.ownership_status == "Publicly Held":
            return "Publicly Held"
        else:
            return "Privately Held"

    @property
    def grouped_business_status(self) -> str:
        if self.business_status is None:
            return "Unknown"
        elif self.business_status in [
            "Generating Revenue",
            "Profitable",
            "Generating Revenue/Not Profitable",
        ]:
            return "Generating Revenue"
        else:
            return "Not Generating Revenue"

    @property
    def grouped_industry_sector(self) -> str:
        if self.primary_pb_industry_sector is None:
            return "Unknown"
        else:
            return self.primary_pb_industry_sector

    @property
    def grouped_industry_subsector(self) -> str:
        if self.primary_pb_industry_group is None:
            return "Unknown"
        else:
            return self.primary_pb_industry_group


@dataclass
class Investor:
    investor_id: str
    investor_name: str
    employees: set[Employee] = field(default_factory=set)
    board_seats: set[BoardMember] = field(default_factory=set)
    interlocks: set[Interlock] = field(default_factory=set)
    investments: set[Investment] = field(default_factory=set)

    def invested_in_company(self, company_id: str) -> bool:
        return any(
            investment.company_id == company_id for investment in self.investments
        )

    def earliest_investment_date(self, company_id: str) -> datetime | None:
        if not self.invested_in_company(company_id):
            raise ValueError(
                f"Investor {self.investor_id} did not invest in {company_id}"
            )
        return min(
            investment.investment_date
            for investment in self.investments
            if investment.company_id == company_id
        )


@dataclass
class Person:
    person_id: str
    person_full_name: str
    board_seats: set[BoardMember] = field(default_factory=set)
    investor_jobs: set[Employee] = field(default_factory=set)
    interlocks: set[Interlock] = field(default_factory=set)

    def works_at_investor(self, investor_id: str) -> bool:
        return any(job.investor_id == investor_id for job in self.investor_jobs)

    def start_date_at_investor(self, investor_id: str) -> datetime | None:
        if not self.works_at_investor(investor_id):
            raise ValueError(
                f"Person {self.person_id} does not work at investor {investor_id}"
            )
        for job in self.investor_jobs:
            if job.investor_id == investor_id:
                return job.start_date

    def position_level_at_investor(self, investor_id: str) -> str:
        if not self.works_at_investor(investor_id):
            raise ValueError(
                f"Person {self.person_id} does not work at investor {investor_id}"
            )
        for job in self.investor_jobs:
            if job.investor_id == investor_id:
                return job.position_level

        raise ValueError(
            f"Person {self.person_id} does not work at investor {investor_id}"
        )

    def has_board_seat(self, company_id: str) -> bool:
        return any(seat.company_id == company_id for seat in self.board_seats)

    def start_date_on_board(self, company_id: str) -> datetime | None:
        if not self.has_board_seat(company_id):
            raise ValueError(
                f"Person {self.person_id} does not have a board seat at {company_id}"
            )
        for seat in self.board_seats:
            if seat.company_id == company_id:
                return seat.start_date
