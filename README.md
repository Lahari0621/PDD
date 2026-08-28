# PDD App — Test Suite Repository

Automated test suites for the **AI Debate Partner** application.

## Repository Structure

```
PDD/
├── web-tests/          Selenium + Python web tests (browser automation)
│   ├── tests/          13 test modules, 160+ test cases
│   ├── pages/          Page Object Model classes
│   ├── utils/          Excel reporter, history tracker
│   └── scripts/        Report generation scripts
│
├── app-tests/          Appium + Java mobile tests (Android automation)
│   ├── src/test/java/  10 test classes, 160+ test cases
│   ├── pom.xml         Maven build file
│   └── testng.xml      TestNG suite configuration
│
├── frontend/           React + Vite frontend source
├── backend/            Node.js + Express backend source
└── .github/workflows/  CI/CD pipelines
```

## Web Tests (Selenium + Python)

Tests the web app through Chrome using Selenium WebDriver.

```bash
cd web-tests
pip install -r requirements.txt
pytest tests/ -v
```

## App Tests (Appium + Java)

Tests the Android app / web app via Chrome on Android using Appium.

```bash
cd app-tests
mvn compile test-compile
# With device: mvn test -Dappium.url=http://localhost:4723
```

## CI/CD

All workflows run automatically on push to `main`:

| Workflow | Folder | Tool | Output |
|----------|--------|------|--------|
| Selenium E2E Tests | web-tests | Python + Selenium | Excel report |
| Appium E2E Tests | app-tests | Java + Appium | Excel report |
| Deploy and Test | frontend | Vite build | GitHub Pages |
| Load Test | - | Shell | Excel report |
| Security Review | - | npm audit | Excel report |
