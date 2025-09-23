# Changelog


## [0.6.1] - 2025-09-23

### Added
- add tests for document storage signal handling (post_delete, pre_save) (307c487)
- proactively create upload directory for tests in `conftest.py` (b0c054f)
- set up Django test environment and databases in pytest via session-scoped fixture (4bd9715)
- configure pytest for `src` layout; add `conftest.py` with Django test settings (a653b92)
- add pytest and pytest-cov to dependencies and dev dependency group in pyproject.toml (9f19f0b)

### Changed
- bump version to 0.6.0 in pyproject.toml (1428f8c)
- create and update GitHub Actions workflow
- refactor: reorganize project structure, update migrations and dependencies, and enhance test coverage (1698d1b)

## 2025-09-18

### Added
- optional Django REST Framework integration with serializers, viewsets, permissions, and settings (8591ff3)

### Changed
- remove `setup.py` in favor of `pyproject.toml` and update `.gitignore` (9104143)
- rewrite and expand README, switch to Markdown format, and add project metadata (28b97d9)

## 2025-09-13

### Changed
- refactor file upload path to support customizable structures and update migration for FileField changes (e574ec6)

## 2025-09-12

### Changed
- set `on_delete=models.SET_NULL` for ForeignKey to ensure compatibility with modern Django versions (f6ab719)
- Updates to ensure Django 4.2 compatibility (4c0b644)
- add pyproject.toml for project metadata and update .gitignore (0aa8629)
- set default_auto_field, update .gitignore, and simplify MANIFEST.in (c5a7b93)

## 2025-09-11

### Changed
- update README and switch license to BSD 3-Clause (baa02c8)
