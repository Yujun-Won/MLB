from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# ChromeWebDriver 설정
service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

driver.get("https://www.spotrac.com/mlb/payroll/2022/")

# 테이블 데이터 크롤링
table = driver.find_element(By.XPATH,
                            "/html/body/div[1]/div[2]/div[1]/div/div/div[1]/div/div[3]/table")
tbody = table.find_element(By.TAG_NAME, "tbody")

data = []  # DataFrame을 위한 데이터 리스트 초기화

rows = tbody.find_elements(By.TAG_NAME, "tr")
for i, value in enumerate(rows, start=1):
    cells = value.find_elements(By.TAG_NAME, "td")

    if cells[0].text in ["LEAGUE AVERAGE", ""]:
        continue
    rank = cells[0].text
    team = cells[1].text
    winRate = cells[2].text
    roster = cells[3].text
    activeRoster = cells[4].text.replace("$", "").replace(",", "")
    injuredReserve = cells[5].text.replace("$", "").replace(",", "")
    retained = cells[6].text.replace("$", "").replace(",", "")
    buried = cells[7].text.replace("$", "").replace(",", "")
    suspended = cells[8].text.replace("$", "").replace(",", "")
    nextYear = cells[-1].text.replace("$", "").replace(",", "")

    data.append([rank, team, winRate, roster, activeRoster,
                 injuredReserve, retained, buried, suspended, nextYear])

# DataFrame 생성 및 CSV 저장
df = pd.DataFrame(data,
                  columns=["Rank", "Team", "Win%", "Roster", "26-Man Payroll",
                           "Injured Reserve", "Retained", "Buried",
                           "Suspended", "2023 Total Payroll"])
df.to_csv("./dataset_2022/07_team-salary.csv", index=False)

# WebDriver 종료
driver.quit()
