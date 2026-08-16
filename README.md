# Munro Tracker

> Parses a CSV file produced by
[DoBIH (Database of British and Irish Hills) v18.4](https://www.hill-bagging.co.uk/dobih),
who are regarded as the authoritative source for hill data in Great Britain and Ireland,
including Munros. Extracts records classified as Munros from the latest survey-year and
writes them to a SQLite database.

---

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)
    - [Test Coverage](#test-coverage)
- [Project Structure](#project-structure)
- [Notes on DoBIH](#notes-on-dobih)
    - [IDs](#ids)
    - [New Release](#new-release)
- [Tooling](#tooling)
- [Contributing](#contributing)
    - [Prerequisites](#prerequisites)
    - [Installing Git Flow](#installing-git-flow)
    - [Initialising Git Flow](#initialising-git-flow)
    - [Branch Structure](#branch-structure)
    - [Workflow](#workflow)
        - [Feature Branches](#feature-branches)
        - [Release Branches](#release-branches)
        - [Hotfix Branches](#hotfix-branches)
    - [More Information](#more-information)

---

## Requirements

- [Git](https://git-scm.com/downloads)
- [Python 3.14.6](https://www.python.org/downloads/release/python-3146/)

---

## Installation

```bash
# Clone the repository:
git clone https://github.com/gregor-mcintyre/munro_tracker.git

# Create a virtual environment:
python3 -m venv .venv

# Activate the virtual environment depending on your operating system:
.venv\Scripts\activate # Windows
source .venv/bin/activate # macOS/Linux

# Install the project development dependencies:
pip install -e ".[dev]"

# Wire up git hooks so formatting/linting/type-checks run on every commit:
pre-commit install
```

---

## Usage

```bash
python build_munro_db.py
```

This creates a SQLite database named `munro.db` containing a single table, `munro`, with
the columns `id`, `name`, and `height_ft`.

---

## Testing

To run all tests:

```bash
pytest
```

Tests are separated into three categories:

- **Unit** - Test individual units of code in isolation. External
  collaborators/dependencies are mocked.
  ```bash
  pytest tests/unit
  ```
- **Integration** - Test interactions between multiple components. Real implementations
  are used.
  ```bash
  pytest tests/integration
  ```
- **End-to-end** - Test the whole system from start to finish, from a user's
  perspective. Real application components and external integrations are used where
  appropriate.
  ```bash
  pytest tests/e2e
  ```

### Test Coverage

Coverage is measured by the `pytest-cov` plugin and configured under `[tool.coverage.*]`
in `pyproject.toml`.

```bash
pytest --cov
```

---

## Project Structure

```
data/
    dobih_munros_and_tops.csv  # DoBIH Munros and Tops CSV file
    munro.db                   # SQLite database of Munros (created after running `python build_munro_db.py`)
munro_db_builder/              # CSV to SQLite pipeline
    __init__.py
    csv/                       # CSV file utilities
        __init__.py
        loader.py              # Load the CSV file
        normalizers.py         # Normalize cells
        row_type.py            # Type alias for a CSV row
    _latest_year_finder.py     # Find the latest survey-year column in the CSV file
    _mapper.py                 # Map CSV rows to internal schema
    _munro_filterer.py         # Filter to Munros from the CSV file
    _sqlite_initializer.py     # Initialize the SQLite database for Munros
    orchestrator.py            # Run the CSV to SQLite pipeline
tests/
    end_to_end/...
    integration/...
    unit/...
.pre-commit-config.yaml        # git hook wiring for the tools described in `pyproject.toml`
build_munro_db.py              # Build a SQLite database of Munros from the CSV file
paths.py                       # Paths to files throughout the project
pyproject.toml                 # Tool config (Ruff, mypy) + dev dependencies
```

---

## Notes on DoBIH

### IDs

The `DoBIH Number` column is used as the primary key of the `munro` table within the
generated `data.munro.db` SQLite database. It is assumed that this is a stable
identifier used across different released versions.

### New Release

It is possible that in the future DoBIH releases an updated version of the Munros and
Tops CSV file. This project currently targets v8.0.1, released on 06/06/2021. If this
happens:

1. Replace `data.dobih_munros_and_tops.csv` with the
   [latest version](https://www.hill-bagging.co.uk/dobih/downloads/). Keep the file name
   as `dobih_munros_and_tops.csv`.
2. Check the headers of the new CSV file and if any headers required for the successful
   operation of this project have been changed (`DoBIH Number`, `Name`, or
   `Height (ft)`), update the corresponding key in
   `munro_db_builder._mapper._CSV_COLUMN_TO_INTERNAL_SCHEMA_MAP` to match.
3. No action required for a new year column, the
   `munro_db_builder._latest_year_finder.find_latest_year_column()` function handles
   this automatically.

---

## Tooling

On every `git commit`, `Ruff` (linting + formatting) and `mypy` (type-checking) run
automatically. Ruff and mypy report issues without auto-fixing them. If a hook fails,
fix the flagged lines yourself, re-stage, and re-commit.

```bash
# Run everything manually against all files:
pre-commit run --all-files
```

**Maintenance note:** vulture's args list explicit paths to scan. When a new top-level
package or module is added, add its path to the vulture hook in
`.pre-commit-config.yaml`.

---

## Contributing

This project uses the **Git Flow** branching model where each branch has a unique
purpose ([see more on this later](#branch-structure)).

### Prerequisites

- The `git-flow` extension installed ([see below](#initialising-git-flow))

### Installing Git Flow

Follow the official installation guide for your platform:
[git-flow installation instructions](https://github.com/nvie/gitflow/wiki/Installation)

Verify the install:

```bash
git flow version
```

### Initialising Git Flow

From the root of the repository, run:

```bash
git flow init
```

You'll be prompted to name each branch type. **Accept the defaults** for consistency
with the rest of the team:

```
Branch name for production releases: [main]
Branch name for "next release" development: [develop]
Feature branch prefix: [feature/]
Release branch prefix: [release/]
Hotfix branch prefix: [hotfix/]
Support branch prefix: [support/]
Version tag prefix: []
```

### Branch Structure

| Branch      | Purpose                                                                                                                                           |
|-------------|---------------------------------------------------------------------------------------------------------------------------------------------------|
| `main`      | Production-ready code only. Every commit here is deployable and typically tagged with a release version.                                          |
| `develop`   | The integration branch for ongoing work. All finished features land here before a release is released.                                            |
| `feature/*` | Short-lived branches for individual features, backlog items, or bug work. Branched from and merged back into `develop`.                           |
| `release/*` | Created when preparing a new version. Used for final stabilisation, version bumps, and release-only fixes. Merged into both `main` and `develop`. |
| `hotfix/*`  | Urgent, isolated fixes for production issues. Branched from `main`, merged into both `main` and `develop`.                                        |

### Workflow

#### Feature Branches

Use for new features.

```
# Create a new feature
git flow feature start <feature-name>

# Publish it so it is visible to others
git flow feature publish <feature-name>

# Or pull another feature
git flow feature pull origin <feature-name>

# Commit and push as you go
git commit -m "Add feature description"
git push

# Finish the feature (merges into develop and deletes the feature branch)
git flow feature finish <feature-name>
git push
```

#### Release Branches

Use when preparing a new version for deployment. A release branch can bundle one or more
completed features.

```
# Create a new release
git flow release start <0.1.2>

# Publish it so it is visible to others
git flow release publish <0.1.2>

# Make any last-minute release fixes directly on the release branch
git commit -m "Final fixes for release v0.1.2"
git push

# Finish the release (merges into main and develop, and tags the release)
git flow release finish <0.1.2> -m "Release v0.1.2"
git push

# Resolve any merge conflicts, then push
git push

# Push the tagged release
git checkout main
git push --tags
```

#### Hotfix Branches

Use for urgent production fixes.

```
# Create a hotfix from main
git flow hotfix start <hotfix-name>

# Publish it so it is visible to others
git flow hotfix publish <hotfix-name>

# Or pull another hotfix
git pull origin hotfix/<hotfix-name>

# Commit and push as you go
git commit -m "Fix critical issue"
git push

# Finish the hotfix (merges into main and develop, and tags the release)
git flow hotfix finish <hotfix-name> -m "Hotfix v0.1.2"
git push

# Resolve any merge conflicts, then push
git push

# Push the hotfix release
git checkout main
git push --tags
```

### More Information

- [Branching Model](https://endjin.com/blog/a-step-by-step-guide-to-using-gitflow-with-teamcity-part-2-gitflow-a-branching-model-for-a-release-cycle)
- [A successful Git branching model](http://nvie.com/posts/a-successful-git-branching-model/)
