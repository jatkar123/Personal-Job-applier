"""Phase 0 worker scaffold.

This file will host scheduled ingestion and resume-tailoring background jobs in future phases.
"""


def ping() -> str:
    return "worker-ready"


if __name__ == "__main__":
    print(ping())
