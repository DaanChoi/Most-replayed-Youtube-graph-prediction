
# Prediction of Most-replayed graph by LSTM
Made by Daan Choi  
☎️ dadols53@gmail.com


<br>

## Requirements
- OS : windows 64bit
- Python version : 3.11
- Package list  
```
scikit-learn              1.3.0
lxml                      4.9.3
matplotlib                3.7.2
numpy                     1.24.3
pandas                    2.0.3
selenium                  4.16.0
youtube-transcript-api    0.6.1
transformers              4.32.1
tensorflow
```

<br>

## Project structure
```
Open-source-AI
├─ chrome-win64 # 테스트용 chrome.exe가 들어있는 폴더
├─ chromedriver-win64 # 크롬드라이버가 들어있는 폴더
├─ .gitattributes
├─ all_graph.py # Most-replayed graph를 그리는 코드
├─ baseline_deeper_epoch_20.py # Model 3 epoch 20 
├─ baseline_deeper_epoch_5.py # Model 3 epoch 5
├─ baseline_epoch_20.py # Model 1 epoch 20
├─ baseline_epoch_5.py # Model 1 epoch 5
├─ bert_regression # Model 2 
├─ bfg-1.14.0.jar
├─ get-pip.py 
└─ youtube_url_to_heatmap_coordinates.py # dataset의 라벨 데이터 크롤링 코드
```
**get-pip.py**  
- selenium 설치 시 다음과 같은 에러를 해결하기 위한 파일   
[notice] A new release of pip is available: 23.2.1 -> 23.3.2   
[notice] To update, run: python.exe -m pip install --upgrade pip

=> ```python get-pip.py``` 실행하여 에러 해결 가능

**chrome-win64 폴더**
- 테스트용 chrome.exe가 들어있는 폴더
- 100MB가 넘는 파일 (chrome.dll)이 있어, lfs를 통해 깃허브에 업로드하였음
- 개별 로컬 pc에 설치되어있는 크롬 버전이 다르거나 아예 크롬이 설치되어 있지 않을때 발생 가능한 문제를 없애기 위해 포함
- 버전 : 119.0.6045.105

**chromedriver-win64**
- 크롬드라이버가 들어있는 폴더
- chrome.exe의 버전과 일치해야 에러가 발생하지 않음
- 버전 : 119.0.6045.105
     
**.gitattributes**
- 깃허브 업로드제한 100MB를 넘는 파일 업로드를 위해 **lfs**를 사용하면서 추가
- lfs로 관리할 파일 경로 / 관리옵션 세팅정보가 들어있음
      
**bfg-1.14.0.jar**
- lfs사용시 이미 commit완료하고 push대기중인 100MB이상 파일때문에 발생하는 문제 해결을 위한 파일
- 다운로드 링크 : https://rtyley.github.io/bfg-repo-cleaner/
- lfs 참고링크 : https://newsight.tistory.com/330
- bfg 참고링크 : https://velog.io/@yoogail/%EB%8C%80%EC%9A%A9%EB%9F%89-%ED%8C%8C%EC%9D%BC-github%EC%97%90-push%ED%95%A0-%EB%95%8C-%EC%83%9D%EA%B8%B0%EB%8A%94-%EC%98%A4%EB%A5%98-%EC%A0%95%EB%B3%B5%ED%95%98%EA%B8%B0feat.-git-lfs-bfg

<br>
