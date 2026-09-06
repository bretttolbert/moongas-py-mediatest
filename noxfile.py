"""Nox configuration file for linting, package validation, and testing."""

from pathlib import Path
import nox

# Global Nox options
nox.options.sessions = ["lint"]
nox.options.needs_version = ">= 2024.3.2"

PYTHON_VERSIONS: list[str] = ["3.10", "3.11", "3.12", "3.13", "3.14"]


@nox.session
def lint(session: nox.Session) -> None:
    """Run code linting and formatting checks via Ruff."""
    session.install("ruff")
    session.run("ruff", "check", ".")


@nox.session
def build_and_check_dists(session: nox.Session) -> None:
    """Build source distribution and wheels, then validate metadata with twine and check-manifest."""
    session.install("build", "check-manifest >= 0.42", "twine")

    session.run("check-manifest", "--ignore", "noxfile.py,tests/**")
    session.run("python", "-m", "build")
    session.run("python", "-m", "twine", "check", "dist/*")


@nox.session(python=PYTHON_VERSIONS)
def tests(session: nox.Session) -> None:
    """Build the package, install the built sdist into the session, and run tests."""
    session.install("pytest")

    # Build distributions inside this session
    build_and_check_dists(session)

    # Find the generated source distribution (.tar.gz) cleanly using pathlib
    dist_dir = Path("dist")
    sdists = list(dist_dir.glob("*.tar.gz"))

    if not sdists:
        session.error("No source distribution (.tar.gz) found in dist/")

    # Install the built sdist to test the real packaged output
    session.install(str(sdists[0]))

    # Run pytest directly (replacing the deprecated 'py.test' executable call)
    session.run("pytest", "tests", *session.posargs)