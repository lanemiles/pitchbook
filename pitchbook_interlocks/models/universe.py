import os
from pitchbook_interlocks.models.data_models import (
    Company,
    Investor,
    Person,
)
from pitchbook_interlocks.models.store import Store


class Universe:
    DEFAULT_NAME: str = "Universe"
    INPUT_DATA_DIR: str = "input_data"
    OUTPUT_CSV: str = "results.csv"
    REQUIRED_FILES: list[str] = [
        "Company.csv",
        "Investor.csv",
        "Person.csv",
        "PersonPositionRelation.csv",
        "PersonBoardSeatRelation.csv",
        "PersonAdvisoryRelation.csv",
        "CompanyCompetitorRelation.csv",
        "CompanyInvestorRelation.csv",
    ]

    def __init__(self, verbose_mode: bool = False) -> None:
        self.name: str = self.DEFAULT_NAME
        self.input_data_dir: str = self.INPUT_DATA_DIR
        self.output_file: str = self.OUTPUT_CSV
        self.company_store: Store[Company] = Store()
        self.investor_store: Store[Investor] = Store()
        self.person_store: Store[Person] = Store()
        self.verbose_mode: bool = verbose_mode

    def input_data_exists(self) -> bool:
        missing = []
        for filename in self.REQUIRED_FILES:
            file_path = os.path.join(os.getcwd(), self.input_data_dir, filename)
            if not os.path.isfile(file_path):
                missing.append(filename)

        if missing:
            for file in missing:
                print(f"Missing file in input_data: {file}")
            return False

        return True

    def get_pb_csv_path(self, table_name: str) -> str:
        return f"{os.getcwd()}/{self.input_data_dir}/{table_name}"
