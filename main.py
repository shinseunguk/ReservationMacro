from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
from enum import Enum, auto
from datetime import datetime, timedelta
import json

def load_config(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

config = load_config('config.json')
class Constants(Enum):
    ID = config["USER_ID"]
    PW = config["USER_PW"]

    LOGIN_URL = config["LOGIN_URL"]
    RESERVATION_URL = config["RESERVATION_URL"]

    TIMEOUT: float = 6000

# Chrome 브라우저의 드라이버 설정
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# 창을 전체화면으로 설정
driver.maximize_window()

# 10시까지 대기하는 함수
def wait_until():
    now = datetime.now()
    # 오늘의 10:00 AM 설정
    target_time = now.replace(hour=10, minute=0, second=0, microsecond=500000)

    # 현재 시간이 10:00 AM 이후인 경우, 다음 날 10:00 AM으로 설정
    if now > target_time:
        target_time += timedelta(days=1)

    now = datetime.now()
    if now < target_time:
        wait_time = (target_time - now).total_seconds()
        print(f"{wait_time}초 동안 대기합니다. 목표 시간: {target_time.strftime('%H:%M:%S')}")
        time.sleep(wait_time)
    else:
        print("목표 시간이 이미 지나버렸습니다.")

# 로그인 함수
def login():
    # 페이지 열기 (여기서는 예시 URL 사용, 실제로는 원하는 페이지 URL로 교체)
    driver.get(Constants.LOGIN_URL.value)

    # 페이지 로딩을 기다리기
    WebDriverWait(driver, Constants.TIMEOUT.value).until(EC.presence_of_element_located((By.ID, "user_id")))

    # 사용자 아이디 입력 필드 찾기
    user_id_field = driver.find_element(By.ID, "user_id")
    user_id_field.clear()  # 기존 값 지우기 (선택 사항)
    user_id_field.send_keys(Constants.ID.value)  # 아이디 입력하기

    # 비밀번호 입력 필드 찾기
    password_field = driver.find_element(By.ID, "user_password")
    password_field.clear()  # 기존 값 지우기 (선택 사항)
    password_field.send_keys(Constants.PW.value)  # 비밀번호 입력하기

    # 로그인 버튼 클릭하기
    login_button = WebDriverWait(driver, Constants.TIMEOUT.value).until(
        EC.element_to_be_clickable((By.XPATH, '//button[text()="로그인"]'))
    )
    login_button.click()

def ready_for_reservation() :
    # 페이지 열기
    driver.get(Constants.RESERVATION_URL.value)

    # '오늘 하루 안보기' 버튼 찾기 (XPATH로 찾기)
    today_button = WebDriverWait(driver, Constants.TIMEOUT.value).until(
        EC.element_to_be_clickable((By.XPATH, '//button[span[text()="오늘 하루 안보기"]]')))
    today_button.click()

    # select 요소 찾기
    select_element = WebDriverWait(driver, Constants.TIMEOUT.value).until(EC.presence_of_element_located((By.ID, "center")))
    select = Select(select_element)
    select.select_by_value("GUNPO01")  # value 속성을 사용하여 선택

    # 조회 버튼 찾기 (CSS 선택자로 찾기)
    submit_button = WebDriverWait(driver, Constants.TIMEOUT.value).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.submit[type="submit"]')))

    # submit_button이 제대로 찾았는지 확인
    if submit_button:
        print("Submit button found:")
        print(f"Button text: {submit_button.text}")
        print(f"Button class: {submit_button.get_attribute('class')}")
    else:
        print("Submit button not found")

    wait_until()  # 10:00 AM까지 대기

    # 조회 버튼 클릭하기
    submit_button.click()

    # '다음월' 링크 클릭하기
    next_month_link = WebDriverWait(driver, Constants.TIMEOUT.value).until(
        EC.element_to_be_clickable((By.ID, "next_month"))
    )
    next_month_link.click()

    # 특정 날짜(td) 클릭하기 ex) 당일이 8/2일 이면 9/2일을 선택
    date_td = WebDriverWait(driver, Constants.TIMEOUT.value).until(
        EC.element_to_be_clickable((By.ID, "date-20240907"))
    )
    date_td.click()

    # 08:00 ~ 10:00 체크박스 선택
    checkbox = WebDriverWait(driver, Constants.TIMEOUT.value).until(
        EC.element_to_be_clickable((By.ID, "checkbox_time_1"))
    )
    checkbox.click()

def apply_for_reservation():
    # 페이지 로딩을 기다리기
    WebDriverWait(driver, Constants.TIMEOUT.value).until(EC.presence_of_element_located((By.ID, "team_nm")))

    # '팀명' 입력 필드 찾기 및 값 입력
    team_nm_field = driver.find_element(By.ID, "team_nm")
    team_nm_field.clear()  # 기존 값 지우기 (선택 사항)
    team_nm_field.send_keys("김민제")  # 팀명 입력하기

    # '인원수' 입력 필드 찾기 및 값 입력
    users_field = driver.find_element(By.ID, "users")
    users_field.clear()  # 기존 값 지우기 (선택 사항)
    users_field.send_keys("14명")  # 인원수 입력하기

    # '목적' 입력 필드 찾기 및 값 입력
    purpose_field = driver.find_element(By.ID, "purpose")
    purpose_field.clear()  # 기존 값 지우기 (선택 사항)
    purpose_field.send_keys("축구")  # 목적 입력하기

    # 페이지 로딩을 기다리기
    WebDriverWait(driver, Constants.TIMEOUT.value).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    # JavaScript를 사용하여 스크롤을 페이지 맨 아래로 내리기
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # 페이지 로딩을 기다리기
    WebDriverWait(driver, Constants.TIMEOUT.value).until(EC.presence_of_element_located((By.ID, "agree_use1")))

    # 체크박스 요소 찾기
    checkbox = driver.find_element(By.ID, "agree_use1")

    # 체크박스가 이미 체크되어 있지 않다면 클릭하여 체크
    if not checkbox.is_selected():
        checkbox.click()

try:
    login()
    ready_for_reservation()
    apply_for_reservation()

    # 무한 루프를 사용하여 대기
    while True:
        time.sleep(1)  # 1초마다 반복 (CPU 사용을 줄이기 위해)
finally:
    # 드라이버 종료
    driver.quit()

