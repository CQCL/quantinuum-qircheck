# Copyright Quantinuum
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from os import listdir

import pytest

import quantinuum_qircheck as qc


def test_check_qir_fileset() -> None:
    for file in listdir("qir/valid"):
        with open(f"qir/valid/{file}") as f:
            qir_str = f.read()

            qc.qircheck(qir_str)


def test_check_qir_invalid_fileset() -> None:
    for file in listdir("qir/invalid"):
        with open(f"qir/invalid/{file}") as f:
            qir_str = f.read()

            with pytest.raises(ValueError) as e:
                qc.qircheck(qir_str)

            if file == "invalid_1.ll":
                assert "Qqis" in str(e)

            if file == "invalid_2.ll":
                assert "Found loop in CFG" in str(e)
