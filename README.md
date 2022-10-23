# HINT, 투자 정보 플랫폼
![로고](/asset/intro.png){: width="400" height="135"}

[프로젝트 홈페이지 - https://koposoftware.github.io/2022_12_jhlee/](https://koposoftware.github.io/2022_12_jhlee/)

# 1. 프로젝트 개요
![배경](/asset/intro.png)

- 주식 거래 이용자수가 증가하고, 무분별한 투자가 증가함에 따라 부정적인 결과가 나오고 있습니다.
- 투자자들에게 합리적인 투자정보 즉, 힌트를 제공하고자 합니다.

## 1-1 개발환경

```
- Macbook Pro(macOS Monterey) M1 pro chip(10-core cpu) 16GB(RAM) 1TB
- Framework : SpringBoot, React, Flask
- IDE : IntelliJ, DataGrip, Github
- DBMS : Oracle, MySQL
- Cloud : Oracle Cloud(Oracle Linux8(1-core, 1GB(RAM), 50GB) / Ubuntu 21.04(4-core, 24GB(RAM), 100GB))
```

## 1-2 수행기간
![간트](/asset/gant.png)

# 2. 프로젝트 구성

## 2-1 아키텍쳐
![아키텍쳐1](/asset/architecture.png)

![아키텍쳐2](/asset/architecture2.png)
   
## 2-2 ERD
![erd](/asset/erd.png)

## 2-3 사용기술
- SpringBoot 기반 웹개발
- Python의 KoNLPy를 이용한 텍스트마이닝: WordCloud(React) 시각화
- WordCloud 키워드 선택시 검색 기능 제공: QueryDSL를 이용한 동적쿼리문 처리
- 주가 제공 시스템 API 서버 구축: Oracle Cloud, Flask
- 대용량 데이터 활용: Oracle Cloud, MySQL -> 약 1000만건의 주식 일봉, 재무제표 데이터
- Axios(React) 비동기 통신을 이용한 화면 갱신
- APScheduler를 이용한 데이터베이스 갱신(데이터 적재): 뉴스, 주식 일봉데이터
- 종목별 일봉과 재무제표를 활용한 데이터 분석: ython, Jupyter Notebook, Pandas, Numpy 등
- Plotly(차트 라이브러리)를 통한 분석 데이터 시각화: Python, Flask
- 프랙탈 패턴 기반 주가 추세 예측: Python, Jupyter Notebook
- Prophet(시계열 예측 라이브러리)를 이용한 주가 추세 예측: Python, Jupyter Notebook

## 2-4 주가 제공 시스템(API Server, Oracle Cloud)
![api](/asset/api.png)

# 3. 기능 설명
![기능1](/asset/f1.png)
![기능2](/asset/f1.png)
![기능3](/asset/f1.png)
![기능4](/asset/f1.png)
![기능5](/asset/f1.png)
![기능6](/asset/f1.png)
![기능7](/asset/f1.png)

# 4. 프로젝트 결과
   
## 4-1 발표 ppt 

[발표자료<img src="/asset/발표ppt.png"/>](/asset/발표ppt.pptx)<br>

## 4-2 시연 동영상 

[![영상](/asset/link.png)](https://github.com/koposoftware/2022_12_jhlee)
  
## 4-3 기대효과
- 다양한 투자 정보 제공으로 손님 유치
- 추후 구독서비스 전환으로 이익창출 도모

## 4-4 보완사항
- 투자 성향 진단 API 제공
- 웹소켓과 증권 API를 이용한 실시간 주가
  (현재는 크롤링 기반으로 제약사항이 많음)
- 분석을 기반으로 테스트를 해볼 수 매수/매도 기능 제공
- 주식 초보자들을 위한 차트 도우미 제공

# 5. 본인 소개

|이름 |이정환|![이정환](/asset/이정환.jpg)|
|연락처 |ljhwan8111@naver.com|
|skill set| Language - C, JAVA, Python, HTML/CSS/Javascript|
| | Frameword - Spring(Boot), Flask, React, JPA|
| | Database - Oracle, MySQL|
| | Etc - Git, Oracle Cloud|
|자격증| 정보처리기사(필기)| 2021.05|
| | |
|수상| |
| | |
|특기사항| 당구 꽤나 침|
|교육| 이노베이션 아카데미(42 Seoul)| 2021.11 ~ 2022.02|
| | 하나금융티아이 채용연계형 교육| 2022.03 ~ 현재|
