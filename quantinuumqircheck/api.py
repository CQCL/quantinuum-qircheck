# Copyright 2020-2024 Quantinuum
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

"""
check for QIR module if it is compatible with quantinuum devices
"""

from typing import Union

import pyqir

from .qircheck import validate_qir_base


def qircheck(qir: Union[str, bytes, pyqir.Module]) -> bool:
    """
    check qir if it is valid
    Allowed types are: str, bytes and pyqir.module
    """
    if isinstance(qir, str):
        module = pyqir.Module.from_ir(pyqir.Context(), qir)
    elif isinstance(qir, bytes):
        module = pyqir.Module.from_bitcode(pyqir.Context(), qir)
    elif isinstance(qir, pyqir.Module):
        module = qir
    else:
        raise ValueError(
            f"unexpected types. Expected str, bytes or pyqir.module. got : {type(qir)}"
        )

    assert module.verify() is None

    return validate_qir_base(module)  # type: ignore
