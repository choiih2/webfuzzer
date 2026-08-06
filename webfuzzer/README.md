# Web Application Vulnerability Fuzzer

> 웹 애플리케이션의 공격 표면을 자동으로 탐색하고 SQLi·XSS 취약점을 판정하는 웹 보안 진단 도구

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)
![Focus](https://img.shields.io/badge/focus-Web_Security-1a7f5a)

---

## 성능 요약

| 지표 | 값 |
|---|---|
| 총 요청 수 | **20,923건** |
| 전체 소요 시간 | **39.0초** |
| 초당 요청 처리 | **536 req/s** |
| 탐지 취약점 | **27건** (SQLi 18 · XSS 9) |

> 단일 실행 기준. 전체 리포트는 [`fuzz_report.txt`](fuzz_report.txt) 참고.

---

## 개요

수동 웹 취약점 점검은 엔드포인트와 폼 파라미터를 일일이 확인해야 해 시간이 오래 걸리고 누락이 발생합니다. 이 도구는 **탐색 → 폼 파싱 → 인젝션 지점 생성 → 퍼징 → 판정 → 리포트**의 파이프라인을 자동화합니다.

- 로그인 세션을 유지한 채 **인증 영역까지** 진단
- SQLi를 **Error / Boolean / Time-based** 세 방식으로 판정
- 컨텍스트별 XSS 페이로드로 반사형 XSS 탐지
- 테스트로 생성된 데이터를 자동 정리(cleanup)해 대상 환경 원복
- `docker-compose`로 취약 웹앱까지 포함한 재현 환경 제공

---

## 아키텍처

각 단계를 독립 모듈로 분리해 확장·유지보수가 쉽도록 설계했습니다.

```
main.py                    # 파이프라인 엔트리포인트
core/
├── discovery.py           # 엔드포인트 크롤링/탐색
├── parser.py              # HTML 폼 추출
├── injector.py            # 인젝션 지점 생성
├── fuzzer.py              # 페이로드 주입 및 실행
├── detectors_sqli.py      # SQLi 판정 (Error/Boolean/Time-based)
├── detectors_xss.py       # XSS 판정
├── payload_loader.py      # 페이로드 로딩
├── login.py               # 로그인 세션 처리
├── session.py             # 세션 상태 관리
├── cleanup.py             # 테스트 데이터 정리
├── report.py              # 결과 리포트 생성
├── config.py / utils.py   # 설정·유틸
payloads/
├── sqli_error.txt
├── sqli_boolean_true.txt
├── sqli_boolean_false.txt
├── sqli_time.txt
└── xss.txt
web/                       # 진단 대상 취약 웹앱 (테스트용)
db/                        # 초기 DB 스키마/시드
wordlists/                 # 엔드포인트 탐색용 워드리스트
docker-compose.yml         # 재현 환경
```

---

## 탐지 기법

**SQL Injection**
- Error-based — DB 오류 메시지 유발 (`EXTRACTVALUE`, `ORDER BY` 등)
- Boolean-based — 논리 우회 (`' OR 1=1 --` 등)
- Time-based — 시간 지연 (`SLEEP()`, `IF(...)`)

**Cross-Site Scripting (XSS)**
- 다양한 컨텍스트별 반사형 페이로드 (`<script>`, `onerror`, `onload`, `svg` 등)

---

## 실행

```bash
# 1) 재현 환경 기동 (취약 웹앱 + DB)
docker-compose up -d

# 2) 퍼저 실행
python main.py --url http://localhost:5000 --depth 2

# XSS 진단까지 포함
python main.py --url http://localhost:5000 --depth 2 --enable-xss
```

실행이 끝나면 취약 파라미터·페이로드·판정 유형이 정리된 리포트가 생성됩니다.

---

## 결과 예시

`/create_post.php`, `/login.php` 등에서 SQLi 18건 · XSS 9건, 총 27건의 취약점을 자동 검출했습니다. 각 항목은 취약 파라미터, 사용된 페이로드, 판정 유형과 함께 표 형태로 기록됩니다.

---

*최일혁 · 경희대학교 컴퓨터공학과 · [github.com/choiih2](https://github.com/choiih2)*
