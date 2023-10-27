#!/usr/bin/env python3

from myhdl import bin
from bits import nasm_test
import os.path

import pytest
import yaml

try:
    from telemetry import telemetryMark

    pytestmark = telemetryMark()
except ImportError as err:
    print("Telemetry não importado")


def source(name):
    dir = os.path.dirname(__file__)
    src_dir = os.path.join(dir, ".")
    return os.path.join(src_dir, name)

def text_to_ram(text, offset=0):
    ram = {}
    for i in range(len(text)):
        ram[i + offset] = ord(text[i])
    ram[1 + len(text)] = 0
    return ram

@pytest.mark.telemetry_files(source("pseudo.nasm"))
def test_pseudo_if():
    ram = {0: 0, 1: 0, 5: 5}
    tst = {5: 6}
    assert nasm_test("pseudo.nasm", ram, tst)


@pytest.mark.telemetry_files(source("pseudo.nasm"))
def test_pseudo_if2():
    ram = {0: 1, 1: 0, 5: 5}
    tst = {5: 6}
    assert nasm_test("pseudo.nasm", ram, tst)


@pytest.mark.telemetry_files(source("pseudo.nasm"))
def test_pseudo_else():
    ram = {0: 3, 1: 0, 5: 5}
    tst = {5: 4}
    assert nasm_test("pseudo.nasm", ram, tst)


@pytest.mark.telemetry_files(source("pseudo.nasm"))
def test_pseudo_else2():
    ram = {0: 0, 1: 1, 5: 5}
    tst = {5: 4}
    assert nasm_test("pseudo.nasm", ram, tst)


@pytest.mark.telemetry_files(source("senha.nasm"))
def test_senha_certo():
    ram = {0: 9, 21184: 0, 21185: 9}
    tst = {21184: 1}
    assert nasm_test("senha.nasm", ram, tst)


@pytest.mark.telemetry_files(source("senha.nasm"))
def test_senha_errado():
    ram = {0: 9, 21184: 0, 21185: 2}
    tst = {21184: 6}
    assert nasm_test("senha.nasm", ram, tst)


@pytest.mark.telemetry_files(source("uppercase.nasm"))
def test_uppercase_exemplo():
    ram = text_to_ram("Hello", 8)
    tst = text_to_ram("HELLO", 8)
    assert nasm_test("uppercase.nasm", ram, tst, 4000)
