from pitchbook_interlocks.models.data_models import Company
from pitchbook_interlocks.print_results.models.results_utils import ResultsUtils


class InterlockBreakdownResult:
    def __init__(self, companies: list[Company]) -> None:
        total: int = len(companies)
        self.num_companies: int = total
        self.num_companies_any_interlock: int = len(
            ResultsUtils.filter_to_companies_with_any_interlocks(companies)
        )
        self.pct_companies_any_interlock: str = ResultsUtils.pct_str(
            self.num_companies_any_interlock, total
        )
        self.num_companies_person_interlock: int = len(
            ResultsUtils.filter_to_companies_with_individual_interlocks(companies)
        )
        self.pct_companies_person_interlock: str = ResultsUtils.pct_str(
            self.num_companies_person_interlock, total
        )
        self.num_companies_investor_interlock: int = len(
            ResultsUtils.filter_to_companies_with_investor_interlocks(companies)
        )
        self.pct_companies_investor_interlock: str = ResultsUtils.pct_str(
            self.num_companies_investor_interlock, total
        )
