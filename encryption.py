import sys
import textwrap
from pathlib import Path

from cryptography.fernet import Fernet

USAGE = textwrap.dedent(
    f"""
    Usage:
        {sys.argv[0]} keygen [KEY_FILE]
        {sys.argv[0]} encrypt KEY_FILE INPUT_FILE [OUTPUT_FILE]
        {sys.argv[0]} decrypt KEY_FILE INPUT_FILE [OUTPUT_FILE]
    """
).strip()


def main(*argv: str) -> str:
    """
    Returns the empty string if:
    * command is `keygen` and `KEY_FILE` is provided
    * command is `encrypt`/`decrypt` and `OUTPUT_FILE` is provided

    Otherwise, returns what would have been written to `KEY_FILE`/`OUTPUT_FILE`.
    """
    if len(argv) <= 1 or "-h" in argv or "--help" in argv:
        return USAGE

    command = argv[1]
    if command == "keygen":
        output_path = Path(argv[2]) if len(argv) > 2 else None
        output = Fernet.generate_key()
    elif command in ["encrypt", "decrypt"] and len(argv) >= 4:
        key = Path(argv[2]).read_bytes()
        input = Path(argv[3]).read_bytes()
        output_path = Path(argv[4]) if len(argv) > 4 else None
        output = getattr(Fernet(key), command)(input)
    else:
        raise ValueError("invalid arguments")

    if output_path is None:
        return output.decode("utf-8", errors="backslashreplace")

    output_path.write_bytes(output)
    return ""


if __name__ == "__main__":
    print(main(*sys.argv) or "Success!")
