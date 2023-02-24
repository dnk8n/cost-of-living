import re
import csv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import ElementClickInterceptedException
from utils.logging import log


class CostOfLiving:
    def __init__(self, origin_country, origin_city, monthly_cost):
        # self.driver = webdriver.Chrome()
        self.driver = webdriver.Firefox()
        self.wait = WebDriverWait(self.driver, 10)
        self.origin_country = origin_country.replace(" ", "+")
        self.origin_city = origin_city.replace(" ", "+")
        self.monthly_cost = "{0:,.1f}".format(monthly_cost)
        self.data = {(origin_country, origin_city): (("", monthly_cost), ("", ""))}

    @staticmethod
    def _parse_cost_of_living(text):
        for clutter in (",", "(", ")"):
            text = text.replace(clutter, "")
        local, foreign = text.split()
        pattern = r"^([+-]?[0-9]*\.?[0-9]*)(.+)$"
        local = re.match(pattern, local)
        foreign = re.match(pattern, foreign)
        return (
            (local.group(2), float(local.group(1))),
            (foreign.group(2), float(foreign.group(1))),
        )

    def _click_like_a(self, max_tries):
        for _ in range(max_tries):
            like_a = self.wait.until(
                expected_conditions.element_to_be_clickable(
                    (By.CSS_SELECTOR, "span.like_a:nth-child(5)")
                )
            )
            try:
                like_a.click()
                return
            except ElementClickInterceptedException:
                self.driver.refresh()

    def compare(self, country, city):
        country = country.replace(" ", "+")
        city = city.replace(" ", "+")
        self.driver.get(
            (
                f"https://www.numbeo.com/cost-of-living/compare_cities.jsp?"
                f"country1={self.origin_country}&city1={self.origin_city}&"
                f"country2={country}&city2={city}"
            )
        )
        self._click_like_a(max_tries=3)
        amount_change_input = self.driver.find_element(By.ID, "amountChangeInput")
        amount_change_input.clear()
        amount_change_input.send_keys(self.monthly_cost)
        amount_change_input.send_keys(Keys.ENTER)
        self.wait.until(
            expected_conditions.text_to_be_present_in_element(
                (By.CSS_SELECTOR, "span.like_a:nth-child(3)"), self.monthly_cost
            )
        )
        cost_of_living = self._parse_cost_of_living(
            self.driver.find_element(By.CSS_SELECTOR, ".number_amount_nobreak").text
        )
        self.data[(country, city)] = cost_of_living

    def bulk_compare(self, dests):
        for dest in dests:
            self.compare(*dest)

    def export_csv(self, path):
        header_template = [
            "Country",
            "City",
            f"Monthly Cost of Living ({[*self.data.values()][1][0][0]})",
            "Monthly Cost of Living (local currency)",
        ]
        with open(path, mode="w") as csv_file:
            csv_writer = csv.writer(
                csv_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
            )
            csv_writer.writerow(header_template)
            for key, value in sorted(self.data.items(), key=lambda item: item[1][0][1]):
                csv_writer.writerow(
                    [key[0], key[1], value[0][1], "".join(map(str, value[1]))]
                )

    def __del__(self):
        self.driver.quit()
        log.debug(f"data: {self.data}")


if __name__ == "__main__":
    c = CostOfLiving("South Africa", "Cape Town", 20000)
    c.bulk_compare(
        [
            ("Netherlands", "Amsterdam"),
            ("Germany", "Berlin"),
            ("Turkey", "Istanbul"),
            ("Portugal", "Lisbon"),
            ("France", "Paris"),
            ("Egypt", "Cairo"),
            ("Georgia", "Tbilisi"),
            ("Cambodia", "Siem Reap"),
            ("Australia", "Sydney"),
            ("Canada", "Vancouver"),
            ("United States", "New York%2C NY")
        ]
    )
    c.export_csv("/home/dean/Downloads/col.csv")
