"""Class for web data scrapping for SARS-CoV-2019."""

import pandas as pd
import requests
from bs4 import BeautifulSoup


class CoV2019data:
    """CoV2019 data class."""

    def __init__(self, output_data_name: str = None):
        """

        Args:

        """
        self.output_data_name = output_data_name
        self.url = "https://www.worldometers.info/coronavirus/"
        self.columns = ["country", "total_cases", "new_cases", "total_deaths", "new_deaths",
                        "total_recovered", "active_cases", "serious_critical",
                        "total_cases_per_1m"]

    def get_data(self):
        """
        Get data method.
        Returns:

        """
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("tbody")
        rows = table.find_all("tr")
        data_rows = []
        for row in rows:
            cols = row.find_all("td")
            cols = [x.text.strip() for x in cols]
            data_rows.append(cols)
        return data_rows

    def save_data(self):
        """
        Save data method.
        """
        cov_data = []
        for cols in self.get_data():
            country = cols[0]
            total_cases = cols[1].replace(",", "")
            new_cases = cols[2].replace(",", "").replace("+", "")
            total_deaths = cols[3].replace(",", "")
            new_deaths = cols[4].replace("+", "")
            total_recovered = cols[5].replace(",", "")
            active_cases = cols[6].replace(",", "")
            serious_critical = cols[7].replace(",", "")
            total_cases_per_1m = cols[8]
            cov_data.append([country, total_cases, new_cases, total_deaths, new_deaths, total_recovered, active_cases,
                             serious_critical, total_cases_per_1m])
        data = pd.DataFrame(data=cov_data, columns=self.columns)
        data.to_csv(f"{self.output_data_name}.csv", index=False)


if __name__ == "__main__":
    data = CoV2019data(output_data_name="data_cov2019")
    print(data.save_data())
