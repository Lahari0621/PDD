# PDD
# AI Debate Partner — Selenium E2E Automation Framework

## Overview

Enterprise-grade CI/CD pipeline with 450+ Selenium test cases targeting the
live GitHub Pages deployment at **https://Lahari0621.github.io/PDD/**

---

## Folder Structure

```
automation/
├── pages/              # Page Object Model classes
│   ├── base_page.py         # BasePage — shared driver interactions
│   ├── landing_page.py      # LandingPage POM
│   ├── login_page.py        # LoginPage POM
│   ├── register_page.py     # RegisterPage POM
│   ├── dashboard_page.py    # DashboardPage POM
│   ├── debate_page.py       # DebatePage POM
│   ├── learn_page.py        # LearnPage POM
│   ├── analytics_page.py    # AnalyticsPage POM
│   ├── profile_page.py      # ProfilePage POM
│   └── navbar.py            # Navbar POM
│
├── tests/              # 450+ pytest test cases
│   ├── conftest.py             # Fixtures, hooks, result collection
│   ├── test_01_authentication.py   # AUTH-001..040 (40 cases)
│   ├── test_02_authorization.py    # AUTHZ-001..040 (40 cases)
│   ├── test_03_navigation.py       # NAV-001..030 (30 cases)
│   ├── test_04_ui_validation.py    # UI-001..050 (50 cases)
│   ├── test_05_forms.py            # FORM-001..050 (50 cases)
│   ├── test_06_crud_operations.py  # CRUD-001..050 (50 cases)
│   ├── test_07_input_validation.py # INP-001..040 (40 cases)
│   ├── test_08_error_handling.py   # ERR-001..020 (20 cases)
│   ├── test_09_session_management.py # SES-001..020 (20 cases)
│   ├── test_10_accessibility.py    # ACC-001..020 (20 cases)
│   ├── test_11_responsive_design.py # RES-001..020 (20 cases)
│   ├── test_12_performance_smoke.py # PERF-001..020 (20 cases)
│   └── test_13_regression.py       # REG-001..050 (50 cases)
│
├── utils/              # Shared utilities
│   ├── driver_factory.py    # Chrome WebDriver factory
│   ├── screenshot_utils.py  # Screenshot capture
│   ├── logger.py            # Logging
│   ├── wait_utils.py        # Explicit waits
│   ├── test_data.py         # Test data generators
│   └── result_collector.py  # Test result aggregation
│
├── config/
│   └── settings.py          # Environment configuration
│
├── scripts/            # Report generators
│   ├── write_framework.py       # Bootstrap framework files
│   ├── setup_framework.py       # Directory setup
│   ├── generate_excel_report.py # Excel reports (4 files)
│   ├── generate_html_report.py  # HTML reports (2 files)
│   └── generate_summary.py      # GitHub Actions summary
│
├── reports/            # Generated after test run
│   ├── Excel/               # .xlsx reports
│   ├── HTML/                # .html reports
│   ├── JSON/                # execution-results.json
│   ├── Screenshots/
│   ├── Logs/
│   └── Summary/             # summary.md
│
├── screenshots/        # Captured screenshots
│   ├── failures/            # Failure screenshots
│   └── passed/
│
├── logs/               # Execution logs
├── history/            # Historical run records
├── pytest.ini          # pytest configuration
└── requirements.txt    # Python dependencies
```

---

## Test Coverage: 450+ Test Cases

| Module | Test IDs | Count |
|--------|----------|-------|
| Authentication | AUTH-001..040 | 40 |
| Authorization | AUTHZ-001..040 | 40 |
| Navigation | NAV-001..030 | 30 |
| UI Validation | UI-001..050 | 50 |
| Forms | FORM-001..050 | 50 |
| CRUD Operations | CRUD-001..050 | 50 |
| Input Validation | INP-001..040 | 40 |
| Error Handling | ERR-001..020 | 20 |
| Session Management | SES-001..020 | 20 |
| Accessibility | ACC-001..020 | 20 |
| Responsive Design | RES-001..020 | 20 |
| Performance Smoke | PERF-001..020 | 20 |
| Regression | REG-001..050 | 50 |
| **TOTAL** | | **450+** |

---

## Local Execution Guide

### Prerequisites

```bash
# Python 3.11+
python --version

# Google Chrome (stable)
google-chrome --version   # Linux/Mac
# or
"C:\Program Files\Google\Chrome\Application\chrome.exe" --version   # Windows
```

### Setup

```bash
cd automation
pip install -r requirements.txt
```

### Run All Tests

```bash
# From automation/ directory
cd automation

# Full suite
python -m pytest tests/ -v

# Single module
python -m pytest tests/test_01_authentication.py -v

# By keyword
python -m pytest tests/ -k "AUTH" -v

# Parallel (4 workers)
python -m pytest tests/ -n 4

# With HTML report
python -m pytest tests/ --html=reports/HTML/local-report.html --self-contained-html
```

### Environment Variables

```bash
# Windows CMD
set BASE_URL=https://Lahari0621.github.io/PDD/
set HEADLESS=true

# Linux/Mac
export BASE_URL=https://Lahari0621.github.io/PDD/
export HEADLESS=true
```

### Generate Reports Manually

```bash
# From automation/ directory
python scripts/generate_excel_report.py
python scripts/generate_html_report.py
python scripts/generate_summary.py
```

---

## CI/CD Execution Guide

### Repository Settings Required

1. Go to **Settings → Pages**
   - Source: **GitHub Actions**

2. Go to **Settings → Actions → General**
   - Workflow permissions: **Read and write**
   - Allow GitHub Actions to create and approve PRs: ✅

3. **Secrets** (Settings → Secrets and variables → Actions):
   - `VITE_API_URL` — your backend URL (optional, for production API)

### Workflow Triggers

```yaml
# Auto triggers:
- push to main/master
- pull_request to main/master

# Manual trigger:
Actions → "Deploy & E2E Test" → Run workflow
  run_tests: true
  test_suite: all  # or: auth | navigation | ui | regression
```

### Pipeline Stages

```
Stage 1:  Checkout
Stage 2:  Install Node.js Dependencies
Stage 3:  Build Application (vite build)
Stage 4:  ESLint Static Analysis
Stage 5:  Deploy to GitHub Pages
Stage 6:  Wait 90s for CDN propagation
Stage 7:  Verify deployment (HTTP 200, retry 15x)
Stage 8:  Run 450+ Selenium E2E tests (headless Chrome)
Stage 9:  Generate HTML reports
Stage 10: Generate Excel reports (4 xlsx files)
Stage 11: Upload all artifacts (30-day retention)
Stage 12: Publish GitHub Actions step summary
Stage 13: Store historical run record
```

### Pass/Fail Logic

| Condition | Result |
|-----------|--------|
| Pass rate ≥ 95% AND critical failures ≤ 5% | ✅ PASS |
| Pass rate < 95% | ❌ FAIL |
| Critical test failures > 5% | ❌ FAIL |
| Deployment fails | ❌ FAIL |

---

## Artifacts

All artifacts are retained for **30 days**:

| Artifact Name | Contents |
|---------------|----------|
| `Automation_Test_Report` | Full test report (6 sheets) |
| `Failed_Test_Cases` | Failed tests + root cause analysis |
| `Passed_Test_Cases` | All passing tests |
| `Summary_Report` | Executive summary |
| `HTML-Reports` | execution-report.html + dashboard.html |
| `Screenshots` | All failure screenshots |
| `Execution-Logs` | pytest output + test logs |
| `JSON-Results` | execution-results.json + junit XML |
| `Complete-Test-Evidence-Run-N` | Full bundle |

---

## Troubleshooting Guide

### 1. Build Fails

```bash
# Check Node version
node --version  # Should be v20+

# Clear cache and reinstall
cd frontend
rm -rf node_modules
npm ci

# Check for TypeScript errors
npx tsc --noEmit
```

### 2. GitHub Pages Not Deploying

- Ensure **Settings → Pages → Source** is set to **GitHub Actions**
- Check workflow permissions (Settings → Actions → General → Read and write)
- Verify `GITHUB_TOKEN` has `pages: write` and `id-token: write` permissions
- Check the `configure-pages` / `deploy-pages` action versions

### 3. Deployment Verification Timeout

The workflow waits up to 15 retries × 20s = 5 minutes.
If it still fails:
- Check GitHub Status: https://www.githubstatus.com/
- Verify repository is public (private repos need GitHub Pro for Pages)
- Try manually visiting https://Lahari0621.github.io/PDD/

### 4. Selenium Tests Fail — ChromeDriver

```bash
# The workflow uses webdriver-manager for auto ChromeDriver management
pip install webdriver-manager --upgrade

# If chrome is not found
which google-chrome
# or
google-chrome --version
```

### 5. Tests Show "Element Not Found"

- Selectors are based on current app structure
- If app is updated, update corresponding POM locators in `pages/`
- Use `EXPLICIT_WAIT=30` for slower connections

### 6. All Tests Fail with Auth Redirect

Protected-page tests inject fake localStorage auth.
If the app's auth key changes from `auth-storage`, update `conftest.py`
and the `inject_auth()` helpers in test files.

### 7. Report Generation Fails

```bash
pip install openpyxl jinja2 --upgrade

# If JSON results not found, reports use placeholder data
# Run tests first, then generate reports
```

### 8. Low Pass Rate on CI vs Local

GitHub Actions runs in a data center — some tests relying on external API
calls (login, dashboard data) will show expected failures since there's no
backend connected to GitHub Pages. These are captured as `FAILED` with reason
"API unavailable". The 95% threshold accounts for this.

---

## Important Notes

- ✅ **Selenium always runs against live GitHub Pages URL** — never localhost
- ✅ All URLs use `BASE_URL` environment variable — no hardcoded URLs
- ✅ Headless Chrome via `--headless=new` for CI compatibility
- ✅ Parallel execution with `pytest-xdist` (`-n 2` in CI)
- ✅ Auto-retry failing tests (`--reruns=2`)
- ✅ Screenshots captured on every failure
- ✅ Results tracked in JSON, Excel, and HTML

---

*AI Debate Partner QA Framework — https://github.com/Lahari0621/PDD*
