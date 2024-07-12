import uuid

import pytest

import encryption


def test_e2e(tmp_path):
    assert "" == encryption.main("", "keygen", str(tmp_path / "key"))

    plaintext = "hi how are you"
    (tmp_path / "plaintext").write_text(plaintext)
    assert "" == encryption.main(
        "",
        "encrypt",
        str(tmp_path / "key"),
        str(tmp_path / "plaintext"),
        str(tmp_path / "ciphertext"),
    )

    assert "" == encryption.main(
        "",
        "decrypt",
        str(tmp_path / "key"),
        str(tmp_path / "ciphertext"),
        str(tmp_path / "decrypted"),
    )
    assert plaintext == (tmp_path / "decrypted").read_text()


@pytest.mark.parametrize(
    "argv",
    [
        [""],
        ["", "-h"],
        ["", "--help"],
        ["", "unknown", "-h"],
    ],
)
def test_print_usage(argv):
    assert encryption.main(*argv) == encryption.USAGE


@pytest.mark.parametrize(
    "argv",
    [
        ["", "unknown"],
        ["", "encrypt"],
        ["", "encrypt", "key"],
        ["", "encrypt", f"key {uuid.uuid4()}", f"input {uuid.uuid4()}"],
        ["", "decrypt"],
        ["", "decrypt", "key"],
        ["", "decrypt", f"key {uuid.uuid4()}", f"input {uuid.uuid4()}"],
    ],
)
def test_bad_args(argv):
    with pytest.raises(Exception):
        encryption.main(*argv)
