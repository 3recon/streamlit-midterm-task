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
