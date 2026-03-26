# 🚀 GITHUB_UPLOAD_GUIDE - GitHub 업로드 가이드

자신의 결과를 GitHub에 공유하는 방법입니다.

---

## 📌 사전 준비

### 필수 준비사항
1. GitHub 계정 생성 (https://github.com)
2. 결과 CSV/MP4 파일 준비
3. 간단한 설명 문서 (선택사항)

---

## 🎯 3단계 업로드

### Step 1: GitHub 저장소 생성

1. GitHub 로그인
2. 오른쪽 상단 `+` 클릭
3. `New repository` 선택
4. 저장소 이름 입력 (예: `my-aruco-results`)
5. 설명 입력 (예: "ArUco marker tracking results")
6. `Create repository` 클릭

### Step 2: 로컬에서 준비

```bash
# 프로젝트 폴더로 이동
cd ~/my-project

# Git 초기화
git init

# 파일 추가
git add .

# 첫 번째 커밋
git commit -m "Initial commit: ArUco tracking results"

# 브랜치 이름 설정 (main이 표준)
git branch -M main
```

### Step 3: GitHub에 업로드

```bash
# 원격 저장소 연결 (GitHub에서 복사한 URL 사용)
git remote add origin https://github.com/YOUR_USERNAME/my-aruco-results.git

# 업로드
git push -u origin main
```

**완료!** ✅

---

## 📁 업로드할 파일 구조 추천

```
my-aruco-results/
│
├── README.md                    # 프로젝트 설명
├── results.csv                  # 추적 결과
├── results.mp4                  # 시각화 영상 (선택)
│
├── docs/                        # 설명 문서
│   ├── EXPERIMENT_SETUP.md
│   └── ANALYSIS.md
│
└── data/                        # 원본 데이터
    ├── original_video.mov
    └── marker_info.txt
```

---

## 📝 README.md 예시

```markdown
# ArUco Marker Tracking Results

iPhone으로 촬영한 영상에서 ArUco 마커를 추적한 결과입니다.

## 실험 조건

- **마커 크기**: 5.0 cm
- **촬영 환경**: 밝은 실내
- **카메라**: iPhone 12
- **영상 길이**: 10초
- **추적 성공률**: 99.5%

## 결과 파일

- `results.csv`: 좌표 데이터 (14 컬럼)
- `results.mp4`: 시각화 영상

## 분석

마커가 일정하게 이동했으며 추적이 안정적입니다.
X 좌표 범위: 10.5 ~ 15.3 cm
Y 좌표 범위: 8.2 ~ 12.7 cm

## 사용한 도구

- OpenCV 4.13.0
- Python 3.9
- ArUco Dictionary: DICT_6X6_250
```

---

## 🔄 나중에 업데이트하기

### 새 파일 추가
```bash
# 새로운 CSV 파일 추가
git add new_results.csv

# 커밋
git commit -m "Add new tracking results"

# 업로드
git push
```

### 파일 수정
```bash
# 수정한 README 커밋
git add README.md
git commit -m "Update analysis section"
git push
```

### 여러 파일 한 번에
```bash
# 모든 변경사항 추가
git add .

# 커밋
git commit -m "Add multiple result files"

# 업로드
git push
```

---

## 🆘 문제 해결

### "Permission denied" 에러
```bash
# SSH 키 설정
# 또는 HTTPS 대신 SSH 사용
# https://docs.github.com/en/authentication/connecting-to-github-with-ssh
```

### "Repository not found" 에러
```bash
# GitHub의 저장소 URL 확인
# 로그인 상태 확인
git remote -v  # 원격 저장소 확인
```

### 대용량 파일 업로드
```bash
# 100MB 이상 파일은 GitHub에서 제한됨
# 해결책:
# 1. 작은 크기로 압축
# 2. GitHub Releases 사용
# 3. Google Drive/Dropbox 링크 대신 README에 추가

# 압축 예시
zip results.zip *.mp4 *.csv
git add results.zip
git commit -m "Add compressed results"
git push
```

---

## 📊 CSV 파일 공유

GitHub에서 직접 CSV 미리보기:
1. GitHub에서 CSV 파일 클릭
2. 자동으로 테이블 표시됨
3. 다운로드 가능

---

## 🎯 협업 팁

### Pull Request로 피드백 받기
1. Fork된 저장소 생성
2. 새 브랜치 생성
3. 변경사항 커밋
4. Pull Request 제출
5. 리뷰 받기

### Issue로 질문하기
1. Issues 탭 클릭
2. "New issue" 클릭
3. 제목과 설명 작성
4. 제출

---

## 💡 베스트 프랙티스

### Commit 메시지 잘 쓰기
```bash
# ❌ 나쁜 예
git commit -m "update"
git commit -m "fix bug"

# ✅ 좋은 예
git commit -m "Add ArUco tracking results for 5cm marker"
git commit -m "Fix coordinate conversion error (issue #5)"
git commit -m "Update analysis with new experimental data"
```

### .gitignore 사용
```bash
# .gitignore 파일 생성
echo "venv/" > .gitignore
echo "*.pyc" >> .gitignore
echo ".DS_Store" >> .gitignore

# 업로드하지 않을 파일 목록
git add .gitignore
git commit -m "Add .gitignore"
```

---

이제 GitHub에서 프로젝트를 공유할 수 있습니다! 🎉
