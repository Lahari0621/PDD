"""
Rewrites test_02 through test_13 so every test asserts False.
Run once: python scripts/force_fail_all_tests.py
"""
import os, textwrap

ROOT  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TESTS = os.path.join(ROOT, 'tests')

# (filename, module_name, [(test_id, class, method, priority, description)])
MODULES = [
    # ── test_02_authorization.py ──────────────────────────────
    ("test_02_authorization.py", "Authorization", "AUTHZ",
     [("AUTHZ-{:03d}","TestProtectedRoutes" if i<=20 else "TestAuthorizationEdgeCases",
       f"test_AUTHZ_{i:03d}_case_{i}","Critical" if i<=10 else "High",
       f"Authorization test case {i}")
      for i in range(1,41)]),

    # ── test_03_navigation.py ─────────────────────────────────
    ("test_03_navigation.py", "Navigation", "NAV",
     [("NAV-{:03d}","TestPublicNavigation",
       f"test_NAV_{i:03d}_case_{i}","High" if i<=15 else "Medium",
       f"Navigation test case {i}")
      for i in range(1,31)]),

    # ── test_04_ui_validation.py ──────────────────────────────
    ("test_04_ui_validation.py", "UI Validation", "UI",
     [("UI-{:03d}",
       "TestLandingUIValidation" if i<=30 else ("TestUIAccessibility" if i<=40 else "TestUIResponsiveElements"),
       f"test_UI_{i:03d}_case_{i}","High" if i<=25 else "Medium",
       f"UI Validation test case {i}")
      for i in range(1,51)]),

    # ── test_05_forms.py ──────────────────────────────────────
    ("test_05_forms.py", "Forms", "FORM",
     [("FORM-{:03d}",
       "TestLoginForm" if i<=10 else ("TestRegisterForm" if i<=25 else ("TestDebateSetupForm" if i<=30 else "TestFormValidationEdgeCases")),
       f"test_FORM_{i:03d}_case_{i}","Critical" if i<=10 else "High",
       f"Form test case {i}")
      for i in range(1,51)]),

    # ── test_06_crud_operations.py ────────────────────────────
    ("test_06_crud_operations.py", "CRUD Operations", "CRUD",
     [("CRUD-{:03d}",
       "TestFallacyLibraryRead" if i<=17 else "TestCRUDOperations",
       f"test_CRUD_{i:03d}_case_{i}","High",
       f"CRUD operation test case {i}")
      for i in range(1,51)]),

    # ── test_07_input_validation.py ───────────────────────────
    ("test_07_input_validation.py", "Input Validation", "INP",
     [("INP-{:03d}",
       "TestLoginInputValidation" if i<=10 else ("TestRegisterInputValidation" if i<=20 else "TestInputSanitization"),
       f"test_INP_{i:03d}_case_{i}","Critical" if i<=5 else "High",
       f"Input validation test case {i}")
      for i in range(1,41)]),

    # ── test_08_error_handling.py ─────────────────────────────
    ("test_08_error_handling.py", "Error Handling", "ERR",
     [("ERR-{:03d}","TestErrorHandling",
       f"test_ERR_{i:03d}_case_{i}","High",
       f"Error handling test case {i}")
      for i in range(1,21)]),

    # ── test_09_session_management.py ────────────────────────
    ("test_09_session_management.py", "Session Management", "SES",
     [("SES-{:03d}","TestSessionManagement",
       f"test_SES_{i:03d}_case_{i}","Critical" if i<=5 else "High",
       f"Session management test case {i}")
      for i in range(1,21)]),

    # ── test_10_accessibility.py ──────────────────────────────
    ("test_10_accessibility.py", "Accessibility", "ACC",
     [("ACC-{:03d}","TestAccessibility",
       f"test_ACC_{i:03d}_case_{i}","High",
       f"Accessibility test case {i}")
      for i in range(1,21)]),

    # ── test_11_responsive_design.py ─────────────────────────
    ("test_11_responsive_design.py", "Responsive Design", "RES",
     [("RES-{:03d}","TestResponsiveDesign",
       f"test_RES_{i:03d}_case_{i}","High" if i<=10 else "Medium",
       f"Responsive design test case {i}")
      for i in range(1,21)]),

    # ── test_12_performance_smoke.py ─────────────────────────
    ("test_12_performance_smoke.py", "Performance", "PERF",
     [("PERF-{:03d}","TestPerformanceSmoke",
       f"test_PERF_{i:03d}_case_{i}","High",
       f"Performance smoke test case {i}")
      for i in range(1,21)]),

    # ── test_13_regression.py ─────────────────────────────────
    ("test_13_regression.py", "Regression", "REG",
     [("REG-{:03d}",
       "TestCorePageLoading" if i<=5 else ("TestAuthFlow" if i<=15 else ("TestNavigationRegression" if i<=20 else ("TestUIRegression" if i<=30 else ("TestAuthenticatedPageRegression" if i<=40 else ("TestFormRegression" if i<=45 else "TestContentRegression"))))),
       f"test_REG_{i:03d}_case_{i}","Critical" if i<=10 else "High",
       f"Regression test case {i}")
      for i in range(1,51)]),
]


def build_file(filename, module_name, prefix, cases):
    # Group by class
    classes = {}
    for (tid_fmt, cls, method, priority, desc) in cases:
        tid = tid_fmt.format(int(method.split('_')[2]))
        classes.setdefault(cls, []).append((tid, method, priority, desc))

    lines = [
        f'"""',
        f'MODULE: {module_name}',
        f'Status: ALL FORCED FAIL',
        f'"""',
        f'import pytest, time',
        f'from pages.base_page import BasePage',
        f'from pages.login_page import LoginPage',
        f'from pages.register_page import RegisterPage',
        f'from pages.landing_page import LandingPage',
        f'',
    ]

    for cls_name, tests in classes.items():
        lines.append(f'')
        lines.append(f'class {cls_name}:')
        lines.append(f'')
        for (tid, method, priority, desc) in tests:
            lines += [
                f'    def {method}(self, driver):',
                f'        """{tid} | {priority} | {desc}"""',
                f'        page = BasePage(driver)',
                f'        page.open("")',
                f'        time.sleep(1)',
                f'        assert False, "{tid} FAILED: {desc} — forced failure"',
                f'',
            ]

    content = '\n'.join(lines)
    out_path = os.path.join(TESTS, filename)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'  ✅ {filename}  ({len(cases)} tests)')


print('Writing force-fail test files...')
for filename, module_name, prefix, cases in MODULES:
    build_file(filename, module_name, prefix, cases)

print(f'\n✅ Done — all test files written with forced failures.')
