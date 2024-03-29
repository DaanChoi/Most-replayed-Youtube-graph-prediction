from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 테스트용 url
# youtube_url_test = "https://www.youtube.com/watch?v=X7158uQk1yI"

# 크롬 웹 드라이버 초기 설정하는 함수로, 매번 테스트브라우저가 열리고 닫히기 때문에 웹드라이버도 매번 설정해줘야 합니다.
def init_driver():
    options = webdriver.ChromeOptions()
    options.binary_location = './chrome-win64/chrome'
    # 크롬 버전 문제 때문에 로컬 pc에 설치된 크롬을 사용하지 않고, 프로젝트 폴더의 chrome-for-testing을 사용하도록 경로 설정.
    driver = webdriver.Chrome()
    # 크롬 웹 드라이버 자동 감지(selenium 4.6.xx 버전 이후부터)
    # 프로젝트 폴더에 119.0.6045버전 chrome-for-testing과 chrome-driver를 넣어뒀습니다.
    # selenium 버전 3.* 에서 실행 안 된다면 -> 4.* 로 업그레이드 pip install --upgrade selenium
    return driver

# url을 주면 히트맵 좌표 데이터를 반환하는 함수
def youtube_url_to_heatmap_coordinates(url):
    driver = init_driver()
    wait = WebDriverWait(driver, 1000)  # 전역적으로 사용 가능한 wait 객체 생성. timeout을 10으로 설정
    try:
        driver.implicitly_wait(100)
        driver.get(url) # 드라이버에 url전달해 GET메서드 호출

        driver.maximize_window()  # 유튜브 창 크기를 최대화 합니다. 왜냐하면 유튜브는 동적 페이지로 이뤄져 있기 때문에 창 크기에 따라서 html 구성이 달라질 수 있습니다.

        # 히트맵 그래프 정보가 담긴 html 태그의 클래스명은 "ytp-heat-map-path"입니다.
        wait.until( # 위에서 설정한 1000s동안,
            EC.presence_of_element_located((By.CLASS_NAME, 'ytp-heat-map-path')) # ytp-heat-map-path 클래스명을 가진 엘리먼트가 감지될때까지 기다리라는 뜻
        )
        heatmap = driver.find_element(By.CLASS_NAME, 'ytp-heat-map-path') # heatmap에 저장
    finally:
        html = BeautifulSoup(driver.page_source, 'lxml').prettify() # lxml 은 라이브러리를 설치해야 사용할 수 있는 파서 pip install lxml
        heatmap = heatmap.get_attribute("d")
        # print(heatmap) # 태그 내부 "d"에 들어있는 히트맵 데이터를 출력
        driver.quit()  # 드라이버 종료
    return heatmap_data_to_coordinate(heatmap)

# heatmap 데이터를 x,y좌표의 배열로 가공하는 함수
def heatmap_data_to_coordinate(heatmap):
    heatmap = heatmap.split("C")
    del heatmap[0]

    x_y_coordinates = []
    for data in heatmap:
        splited_data = data.split(" ")[3].split(",")
        x = (float(splited_data[0]) - 5) / 1000
        y = (100 - float(splited_data[1])) / 100 # x와 y를 0~1사이 값으로 바꿔줍니다.
        y = round(y,4) # y 소수점 아래 3자리 까지 제한
        x_y_coordinates.append([x,y])

    return x_y_coordinates

# 테스트코드
# print(youtube_url_to_heatmap_coordinates(youtube_url_test))