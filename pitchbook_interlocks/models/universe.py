import pickle
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

    def __init__(self, verbose_mode: bool = False) -> None:
        self.name: str = self.DEFAULT_NAME
        self.input_data_dir: str = self.INPUT_DATA_DIR
        self.output_file: str = self.OUTPUT_CSV
        self.company_store: Store[Company] = Store()
        self.investor_store: Store[Investor] = Store()
        self.person_store: Store[Person] = Store()
        self.verbose_mode: bool = verbose_mode

    def get_pb_csv_path(self, table_name: str) -> str:
        return f"{os.getcwd()}/{self.input_data_dir}/{table_name}"

    # def save(self) -> None:
    #     """Serialize this Universe instance to a file."""
    #     with open(f"{self.name}.pkl", "wb") as f:
    #         pickle.dump(self, f)

    # @classmethod
    # def load(cls, filename: str) -> "Universe":
    #     """Load a Universe instance from a file."""
    #     with open(filename, "rb") as f:
    #         return pickle.load(f)
