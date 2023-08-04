from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# ChromeWebDriver 설정
service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

categories = ['batters', 'pitching']

for category in categories:
    driver.get(f"https://www.spotrac.com/mlb/rankings/2022/salary/{category}/")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "table")))

    # table의 XPATH를 설정하고, table의 요소들을 차례대로 find_element()
    table = driver.find_element(By.XPATH,
                                "/html/body/div[1]/div[2]/div[1]/div/div/div[1]/div/div[3]/div/table")
    tbody = table.find_element(By.TAG_NAME, "tbody")

    data = []  # DataFrame을 위한 데이터 리스트 초기화

    rows = tbody.find_elements(By.TAG_NAME, "tr")
    for i, value in enumerate(rows, start=1):
        name = value.find_elements(By.TAG_NAME, "td")[1].text.split("\n")[0]
        team = value.find_elements(By.TAG_NAME, "td")[1].text.split("\n")[1]
        position = value.find_elements(By.TAG_NAME, "td")[2].text
        age = value.find_elements(By.TAG_NAME, "td")[3].text
        bat_throw = value.find_elements(By.TAG_NAME, "td")[4].text
        salary = value.find_elements(By.TAG_NAME, "td")[-1].text.replace("$", "").replace(",", "")

        data.append([i, name, team, position, age, bat_throw, salary])

    # DataFrame 생성 및 CSV 저장: 타자와 투수의 컬럼명을 다르게 써서 저장
    if category == 'batters':
        df = pd.DataFrame(data,
                          columns=["No", "Name", "Team", "Position", "Age", "Bats", "Salary"])
        df.to_csv("./dataset_2022/batter-salary.csv", index=False)
    else:
        df = pd.DataFrame(data,
                          columns=["No", "Name", "Team", "Position", "Age", "Throws", "Salary"])
        df.to_csv("./dataset_2022/pitcher-salary.csv", index=False)

# WebDriver 종료
driver.quit()
