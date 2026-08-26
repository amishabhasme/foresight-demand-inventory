from pathlib import Path


def check_project_structure():

    project_root = Path(__file__).resolve().parent

    required_paths = [
        project_root / "data" / "processed",
        project_root / "notebooks",
        project_root / "src",
        project_root / "dashboard",
    ]

    print("\nFORESIGHT PROJECT CHECK")
    print("=" * 40)

    for path in required_paths:

        status = "OK" if path.exists() else "MISSING"

        print(f"{status:8} {path.relative_to(project_root)}")


if __name__ == "__main__":

    check_project_structure()