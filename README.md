# 관심종목 브리핑 — 웹앱 (Liner 스타일)

`latest.json` 데이터를 보여주는 모바일 웹앱. iOS 26.5 등 **어떤 아이폰에서도** 홈 화면에 추가하면 전체화면 앱처럼 쓸 수 있습니다. Xcode·맥 불필요.

## 파일

```
web/
├─ index.html            앱 본체 (HTML+CSS+JS 한 파일)
├─ latest-sample.json    개발용 샘플 데이터
├─ latest.json           ★ 실제 데이터 (배포 시 여기에 올림 — 지금은 없음)
├─ manifest.webmanifest  PWA 설정
├─ icon.svg / icon-180.png / icon-512.png   앱 아이콘
└─ make_icons.py         아이콘 재생성 스크립트 (선택)
```

## 데이터 로딩 동작 (자동)

앱은 **같은 폴더의 `latest.json`** 을 fetch 합니다. 순서대로 자동 폴백:

1. **`latest.json`** 있으면 → 그걸 사용 (배포 환경)
2. 없으면 → **`latest-sample.json`** 사용 (개발 환경)
3. 그것도 없으면(`file://` 더블클릭 등) → index.html 내장 샘플

> 상단에 배지로 출처 표시: `샘플파일`(latest-sample.json) / `샘플`(내장) / 배지 없음(실제 latest.json).
> 브라우저 콘솔에도 `[브리핑] 데이터 출처: ...` 가 찍혀서 어떤 걸 읽었는지 확인 가능.
> ⚙ 설정에서 다른 주소(GitHub raw 등)를 직접 넣거나 `sample`로 강제할 수도 있습니다.

## 1. 로컬에서 테스트 (개발 중)

`fetch`는 보안상 `file://`(더블클릭)에선 막히므로 **로컬 서버**로 띄워야 `latest-sample.json`을 읽습니다.

터미널에서:

```bash
cd ~/Downloads/test/web
python3 -m http.server 8000
```

그 다음 브라우저에서 **http://localhost:8000** 접속.
- `latest.json`이 아직 없으니 → 자동으로 `latest-sample.json`을 읽어 화면이 뜸 (상단 배지 `샘플파일`).
- 실제 데이터 테스트는 `latest.json` 파일을 이 폴더에 만들어 두면 그걸 우선 사용.
- 서버 끄기: 터미널에서 `Ctrl + C`.

> 폰에서도 같은 와이파이면 `http://<맥 IP>:8000` 으로 접속해 미리 볼 수 있어요. (맥 IP: 시스템 설정 > 네트워크)

## 2. GitHub Pages에 올리기 (배포)

1. GitHub에 새 저장소 생성 → `web` 폴더 안 파일 전부 업로드
   (실제 데이터 `latest.json`도 함께 올리거나, 자동화로 이 위치에 갱신되게 설정)
2. 저장소 **Settings → Pages → Branch `main` / `/ (root)` → Save**
3. 몇 분 뒤 주소: `https://<아이디>.github.io/<저장소>/`
4. 그 주소를 아이폰 사파리로 열기 → 앱은 같은 경로의 `latest.json`을 자동으로 읽음

> **실제 자동 데이터**: 가이드의 "Cowork 예약작업 → GitHub `latest.json` 갱신" 흐름을 그대로 쓰면 됩니다.
> Cowork가 같은 스키마의 JSON을 저장소의 `latest.json`(같은 폴더)에 push 하도록 설정하면 끝. 앱은 코드 수정 없이 자동 반영.

## 3. 아이폰 홈 화면에 앱으로 추가

1. 아이폰 **사파리**로 배포 주소 열기
2. 하단 **공유(⬆️)** → **"홈 화면에 추가"**
3. 민트그린 아이콘 생김 → 누르면 **전체화면 앱처럼** 실행 ✅ (7일 재설치 같은 제약 없음)

## 화면

- **아침 브리핑**: 관심종목 상승(빨강)/하락(파랑) · 🔥hot · ETF 예상 시초가 · 간밤 미국증시(VIX 등락폭) · 반도체 방향성 · 매크로 · 경제일정/발표지표(표) · 실적
- **개장 전 급등락**: 카테고리별. `empty=true`면 "오늘 ±5% 종목 없음"
- **리서치**: 리포트 카드 → 탭하면 PDF 새 탭으로 열림
- 공통: 상단 updatedAt, 당겨서 새로고침(↻), ⚙ 설정(DATA_URL), 로딩/에러 처리, 다크모드 자동

## 아이콘 바꾸기 (선택)

`make_icons.py` 의 색/도형 수정 후 `python3 make_icons.py` 실행 → PNG 재생성.
민트그린 `#00c471` 은 `index.html` / `manifest.webmanifest` / `icon.svg` 에서 함께 바꾸세요.
