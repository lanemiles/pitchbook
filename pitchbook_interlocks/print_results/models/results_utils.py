from pitchbook_interlocks.models.data_models import Company, Person
from typing import Any
import numpy as np


class ResultsUtils:
    MIN_BOARD_MEMBER_THRESHOLDS = [1, 3, 5]

    @classmethod
    def group_companies_by_property(
        cls,
        companies: list[Company],
        property_mapper: Any,
        all_companies: list[Company],
    ) -> dict[str, list[Company]]:
        result = {}
        for company in all_companies:
            key = property_mapper(company)
            result.setdefault(key, [])

        for company in companies:
            key = property_mapper(company)
            result[key].append(company)
        return result

    @classmethod
    def group_companies_by_two_properties(
        cls,
        companies: list[Company],
        property_mapper_1: Any,
        property_mapper_2: Any,
        all_companies: list[Company],
    ) -> dict[str, dict[str, list[Company]]]:
        result = {}

        for company in all_companies:
            key1 = property_mapper_1(company)
            key2 = property_mapper_2(company)
            result.setdefault(key1, {}).setdefault(key2, [])

        for company in companies:
            key1 = property_mapper_1(company)
            key2 = property_mapper_2(company)
            result[key1][key2].append(company)
        return result

    @classmethod
    def filter_to_companies_with_at_least_n_board_members(
        cls, companies: list[Company], n: int
    ) -> list[Company]:
        return [company for company in companies if len(company.board_members) >= n]

    @classmethod
    def filter_to_people_with_investor_job(cls, people: list[Person]) -> list[Person]:
        return [person for person in people if person.investor_jobs]

    @classmethod
    def filter_to_people_with_individual_interlock(
        cls, people: list[Person]
    ) -> list[Person]:
        return [person for person in people if person.interlocks]

    @classmethod
    def filter_to_companies_with_individual_interlocks(
        cls, companies: list[Company]
    ) -> list[Company]:
        return [company for company in companies if company.person_interlocks]

    @classmethod
    def filter_to_companies_with_investor_interlocks(
        cls, companies: list[Company]
    ) -> list[Company]:
        return [company for company in companies if company.investor_interlocks]

    @classmethod
    def filter_to_companies_with_any_interlocks(
        cls, companies: list[Company]
    ) -> list[Company]:
        return [
            company
            for company in companies
            if company.person_interlocks or company.investor_interlocks
        ]

    @classmethod
    def pct_str(cls, a: int | float, b: int | float) -> str:
        if b == 0:
            return "N/A%"
        return f"{(a*1.0/b) * 100:.1f}%"

    @classmethod
    def print_csv_str(cls, vals: list[object]) -> None:
        print(",".join(str(val).replace(",", "") for val in vals))

    @classmethod
    def compute_stats(cls, gap_list: list[float]) -> dict[str, float | int | None]:
        if not gap_list:
            return {
                "Count": 0,
                "Min (Days)": None,
                "25th Percentile (Days)": None,
                "Median (Days)": None,
                "75th Percentile (Days)": None,
                "Mean (Days)": None,
                "Max (Days)": None,
            }
        arr = np.array(gap_list, dtype=float)
        return {
            "Count": len(gap_list),
            "Min (Days)": float(np.min(arr)),
            "25th Percentile (Days)": float(np.percentile(arr, 25)),
            "Median (Days)": float(np.median(arr)),
            "75th Percentile (Days)": float(np.percentile(arr, 75)),
            "Mean (Days)": float(np.mean(arr)),
            "Max (Days)": float(np.max(arr)),
        }
