# 광운퀴즈쇼

Streamlit으로 만든 광운대학교 퀴즈 앱입니다. 회원가입과 로그인 정보는 로컬 CSV에 저장되고, 로그인한 사용자만 퀴즈를 풀 수 있습니다.

## 실행 방법

```bash
pip install -r requirements.txt
streamlit run app.py
```

EC2에서 외부 접속을 확인할 때는 다음처럼 실행합니다.

```bash
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

브라우저에서는 아래 형식으로 접속합니다.

```text
http://EC2_PUBLIC_IPV4:8501
```

## 제출 영상 체크리스트

- EC2 Public IPv4 주소가 화면에 보이도록 녹화
- 브라우저 주소창에 `http://EC2_PUBLIC_IPV4:8501` 접속 장면 포함
- Streamlit 앱 첫 화면과 학번, 이름 노출 확인
- 회원가입 또는 로그인 후 퀴즈 버튼을 눌러 앱 조작
- 앱 조작 중 EC2 터미널의 Streamlit 로그가 함께 보이도록 녹화

## 제출물

- GitHub repository 주소
- YouTube 부분공개 영상 링크

영상은 제출 기한 전에 업로드하고, 2026년 6월 20일까지 유지합니다.
