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


import pytest

import quantinuum_qircheck as qc


def test_check_qir_simpel() -> None:
    qc.qircheck(
        """; ModuleID = 'test_pytket_qir'
source_filename = "test_pytket_qir"

%Qubit = type opaque
%Result = type opaque

define void @main() #0 {
entry:
  call void @__quantum__qis__h__body(%Qubit* null)
  ret void
}

declare i1 @__quantum__qis__read_result__body(%Result*)

declare void @__quantum__rt__int_record_output(i64, i8*)

declare void @__quantum__rt__result_record_output(%Result*, i8*)

declare void @__quantum__qis__h__body(%Qubit*)

attributes #0 = { "entry_point" "output_labeling_schema" "qir_profiles"="custom" "required_num_qubits"="3" "required_num_results"="3" }

!llvm.module.flags = !{!0, !1, !2, !3}

!0 = !{i32 1, !"qir_major_version", i32 1}
!1 = !{i32 7, !"qir_minor_version", i32 0}
!2 = !{i32 1, !"dynamic_qubit_management", i1 false}
!3 = !{i32 1, !"dynamic_result_management", i1 false}"""
    )


def test_check_qir_simpel_wrong() -> None:

    qir = """; ModuleID = 'test_pytket_qir'
source_filename = "test_pytket_qir"

%Qubit = type opaque
%Result = type opaque

define void @main() #0 {
entry:
  call void @__quantum__Qqis__h__body(%Qubit* null)
  ret void
}

declare i1 @__quantum__qis__read_result__body(%Result*)

declare void @__quantum__rt__int_record_output(i64, i8*)

declare void @__quantum__rt__result_record_output(%Result*, i8*)

declare void @__quantum__qis__h__body(%Qubit*)

attributes #0 = { "entry_point" "output_labeling_schema" "qir_profiles"="custom" "required_num_qubits"="3" "required_num_results"="3" }

!llvm.module.flags = !{!0, !1, !2, !3}

!0 = !{i32 1, !"qir_major_version", i32 1}
!1 = !{i32 7, !"qir_minor_version", i32 0}
!2 = !{i32 1, !"dynamic_qubit_management", i1 false}
!3 = !{i32 1, !"dynamic_result_management", i1 false}"""

    with pytest.raises(ValueError) as e:
        qc.qircheck(qir)

    assert "Qqis" in str(e)


def test_check_qir_complex() -> None:
    qc.qircheck(
        """; ModuleID = 'test_pytket_qir'
source_filename = "test_pytket_qir"

%Qubit = type opaque
%Result = type opaque

define void @main() #0 {
entry:
  call void @__quantum__qis__h__body(%Qubit* null)
  ret void
}

declare i1 @__quantum__qis__read_result__body(%Result*)

declare void @__quantum__rt__int_record_output(i64, i8*)

declare void @__quantum__rt__result_record_output(%Result*, i8*)

declare void @__quantum__qis__h__body(%Qubit*)

attributes #0 = { "entry_point" "output_labeling_schema" "qir_profiles"="custom" "required_num_qubits"="3" "required_num_results"="3" }

!llvm.module.flags = !{!0, !1, !2, !3}

!0 = !{i32 1, !"qir_major_version", i32 1}
!1 = !{i32 7, !"qir_minor_version", i32 0}
!2 = !{i32 1, !"dynamic_qubit_management", i1 false}
!3 = !{i32 1, !"dynamic_result_management", i1 false}"""
    )


fileslist = [
    "test_pytket_qir_10-QIRProfile.ADAPTIVE_CREGSIZE.ll",
    "test_pytket_qir_7-QIRProfile.AZUREADAPTIVE.ll",
    "test_pytket_qir_conditional_4-QIRProfile.AZUREADAPTIVE.ll",
    "test_pytket_qir_10-QIRProfile.ADAPTIVE.ll",
    "test_pytket_qir_7-QIRProfile.PYTKET.ll",
    "test_pytket_qir_conditional_4-QIRProfile.PYTKET.ll",
    "test_pytket_qir_10-QIRProfile.AZUREADAPTIVE.ll",
    "test_pytket_qir_8-QIRProfile.ADAPTIVE_CREGSIZE.ll",
    "test_pytket_qir_conditional_5-QIRProfile.ADAPTIVE_CREGSIZE.ll",
    "test_pytket_qir_10-QIRProfile.PYTKET.ll",
    "test_pytket_qir_8-QIRProfile.ADAPTIVE.ll",
    "test_pytket_qir_conditional_5-QIRProfile.ADAPTIVE.ll",
    "test_pytket_qir_11-QIRProfile.ADAPTIVE_CREGSIZE.ll",
    "test_pytket_qir_8-QIRProfile.AZUREADAPTIVE.ll",
    "test_pytket_qir_conditional_5-QIRProfile.AZUREADAPTIVE.ll",
    "test_pytket_qir_11-QIRProfile.ADAPTIVE.ll",
    "test_pytket_qir_8-QIRProfile.PYTKET.ll",
    "test_pytket_qir_conditional_5-QIRProfile.PYTKET.ll",
    "test_pytket_qir_11-QIRProfile.AZUREADAPTIVE.ll",
    "test_pytket_qir_9-QIRProfile.ADAPTIVE_CREGSIZE.ll",
    "test_pytket_qir_conditional_6-QIRProfile.ADAPTIVE_CREGSIZE.ll",
    "test_pytket_qir_11-QIRProfile.PYTKET.ll",
    "test_pytket_qir_9-QIRProfile.ADAPTIVE.ll",
    "test_pytket_qir_conditional_6-QIRProfile.ADAPTIVE.ll",
    "test_pytket_qir_12-QIRProfile.ADAPTIVE_CREGSIZE.ll",
    "test_pytket_qir_9-QIRProfile.AZUREADAPTIVE.ll",
    "test_pytket_qir_conditional_6-QIRProfile.AZUREADAPTIVE.ll",
    "test_pytket_qir_12-QIRProfile.ADAPTIVE.ll",
    "test_pytket_qir_9-QIRProfile.PYTKET.ll",
    "test_pytket_qir_conditional_6-QIRProfile.PYTKET.ll",
    "test_pytket_qir_12-QIRProfile.AZUREADAPTIVE.ll",
    "test_pytket_qir_barrier_2-QIRProfile.ADAPTIVE.ll",
    "test_pytket_qir_conditional_7-QIRProfile.ADAPTIVE_CREGSIZE.ll",
    "test_pytket_qir_12-QIRProfile.PYTKET.ll",
    "test_pytket_qir_barrier-QIRProfile.ADAPTIVE.ll",
    "test_pytket_qir_conditional_7-QIRProfile.ADAPTIVE.ll",
    "test_pytket_qir_13-QIRProfile.ADAPTIVE_CREGSIZE.ll",
    "test_pytket_qir_conditional_10-QIRProfile.ADAPTIVE_CREGSIZE.ll",
    "test_pytket_qir_conditional_7-QIRProfile.AZUREADAPTIVE.ll",
    "test_pytket_qir_13-QIRProfile.ADAPTIVE.ll",
    "test_pytket_qir_conditional_10-QIRProfile.ADAPTIVE.ll",
    "test_pytket_qir_conditional_7-QIRProfile.PYTKET.ll",
    "test_pytket_qir_13-QIRProfile.AZUREADAPTIVE.ll",
    "test_pytket_qir_conditional_10-QIRProfile.AZUREADAPTIVE.ll",
    "test_pytket_qir_conditional_8-QIRProfile.ADAPTIVE_CREGSIZE.ll",
    "test_pytket_qir_13-QIRProfile.PYTKET.ll",
    "test_pytket_qir_conditional_10-QIRProfile.PYTKET.ll",
    "test_pytket_qir_conditional_8-QIRProfile.ADAPTIVE.ll",
    "test_pytket_qir_14-QIRProfile.ADAPTIVE_CREGSIZE.ll",
    "test_pytket_qir_conditional_11-QIRProfile.ADAPTIVE_CREGSIZE.ll",
    "test_pytket_qir_conditional_8-QIRProfile.AZUREADAPTIVE.ll",
    "test_pytket_qir_14-QIRProfile.ADAPTIVE.ll",
    "test_pytket_qir_conditional_11-QIRProfile.ADAPTIVE.ll",
    "test_pytket_qir_conditional_8-QIRProfile.BASE.ll",
    "test_pytket_qir_14-QIRProfile.AZUREADAPTIVE.ll",
    "test_pytket_qir_conditional_11-QIRProfile.AZUREADAPTIVE.ll",
    "test_pytket_qir_conditional_8-QIRProfile.PYTKET.ll",
    "test_pytket_qir_14-QIRProfile.PYTKET.ll",
    "test_pytket_qir_conditional_11-QIRProfile.PYTKET.ll",
    "test_pytket_qir_conditional_9-QIRProfile.ADAPTIVE_CREGSIZE.ll",
    "test_pytket_qir_15-QIRProfile.ADAPTIVE_CREGSIZE.ll",
    "test_pytket_qir_conditional_12-QIRProfile.ADAPTIVE_CREGSIZE.ll",
    "test_pytket_qir_conditional_9-QIRProfile.ADAPTIVE.ll",
    "test_pytket_qir_15-QIRProfile.ADAPTIVE.ll",
    "test_pytket_qir_conditional_12-QIRProfile.ADAPTIVE.ll",
    "test_pytket_qir_conditional_9-QIRProfile.AZUREADAPTIVE.ll",
    "test_pytket_qir_15-QIRProfile.AZUREADAPTIVE.ll",
    "test_pytket_qir_conditional_12-QIRProfile.AZUREADAPTIVE.ll",
    "test_pytket_qir_conditional_9-QIRProfile.BASE.ll",
    "test_pytket_qir_15-QIRProfile.PYTKET.ll",
    "test_pytket_qir_conditional_12-QIRProfile.PYTKET.ll",
    "test_pytket_qir_conditional_9-QIRProfile.PYTKET.ll",
    "test_pytket_qir_16-QIRProfile.ADAPTIVE_CREGSIZE.ll",
    "test_pytket_qir_conditional_13-QIRProfile.ADAPTIVE_CREGSIZE.ll",
    "test_pytket_qir_conditional-QIRProfile.ADAPTIVE_CREGSIZE.ll",
    "test_pytket_qir_16-QIRProfile.ADAPTIVE.ll",
    "test_pytket_qir_conditional_13-QIRProfile.ADAPTIVE.ll",
    "test_pytket_qir_conditional-QIRProfile.ADAPTIVE.ll",
    "test_pytket_qir_16-QIRProfile.AZUREADAPTIVE.ll",
    "test_pytket_qir_conditional_13-QIRProfile.AZUREADAPTIVE.ll",
    "test_pytket_qir_conditional-QIRProfile.AZUREADAPTIVE.ll",
    "test_pytket_qir_16-QIRProfile.PYTKET.ll",
    "test_pytket_qir_conditional_13-QIRProfile.PYTKET.ll",
    "test_pytket_qir_conditional-QIRProfile.PYTKET.ll",
    "test_pytket_qir_17-QIRProfile.ADAPTIVE_CREGSIZE.ll",
    "test_pytket_qir_conditional_14-block-QIRProfile.ADAPTIVE_CREGSIZE.ll",
    "test_pytket_qir_module-QIRProfile.ADAPTIVE.ll",
    "test_pytket_qir_17-QIRProfile.ADAPTIVE.ll",
    "test_pytket_qir_conditional_14-block-QIRProfile.ADAPTIVE.ll",
    "test_pytket_qir_qasm_classical_0-QIRProfile.ADAPTIVE.ll",
    "test_pytket_qir_17-QIRProfile.AZUREADAPTIVE.ll",
    "test_pytket_qir_conditional_14-block-QIRProfile.AZUREADAPTIVE.ll",
    "test_pytket_qir_qasm_classical_0-QIRProfile.AZUREADAPTIVE.ll",
    "test_pytket_qir_17-QIRProfile.PYTKET.ll",
    "test_pytket_qir_conditional_14-block-QIRProfile.PYTKET.ll",
    "test_pytket_qir_qasm_classical_0-QIRProfile.PYTKET.ll",
    "test_pytket_qir_19-QIRProfile.ADAPTIVE_CREGSIZE.ll",
    "test_pytket_qir_conditional_15-block-QIRProfile.ADAPTIVE_CREGSIZE.ll",
    "test_pytket_qir_qasm_classical_1-QIRProfile.ADAPTIVE.ll",
    "test_pytket_qir_19-QIRProfile.ADAPTIVE.ll",
    "test_pytket_qir_conditional_15-block-QIRProfile.ADAPTIVE.ll",
    "test_pytket_qir_qasm_classical_1-QIRProfile.AZUREADAPTIVE.ll",
    "test_pytket_qir_19-QIRProfile.AZUREADAPTIVE.ll",
    "test_pytket_qir_conditional_15-block-QIRProfile.AZUREADAPTIVE.ll",
    "test_pytket_qir_qasm_classical_1-QIRProfile.PYTKET.ll",
    "test_pytket_qir_19-QIRProfile.BASE.ll",
    "test_pytket_qir_conditional_15-block-QIRProfile.PYTKET.ll",
    "test_pytket_qir_qasm-QIRProfile.ADAPTIVE.ll",
    "test_pytket_qir_19-QIRProfile.PYTKET.ll",
    "test_pytket_qir_conditional_16-block-QIRProfile.ADAPTIVE_CREGSIZE.ll",
    "test_pytket_qir-QIRProfile.ADAPTIVE_CREGSIZE.ll",
    "test_pytket_qir_20-QIRProfile.ADAPTIVE_CREGSIZE.ll",
    "test_pytket_qir_conditional_16-block-QIRProfile.ADAPTIVE.ll",
    "test_pytket_qir-QIRProfile.ADAPTIVE.ll",
    "test_pytket_qir_20-QIRProfile.ADAPTIVE.ll",
    "test_pytket_qir_conditional_16-block-QIRProfile.AZUREADAPTIVE.ll",
    "test_pytket_qir-QIRProfile.AZUREADAPTIVE.ll",
    "test_pytket_qir_20-QIRProfile.AZUREADAPTIVE.ll",
    "test_pytket_qir_conditional_16-block-QIRProfile.PYTKET.ll",
    "test_pytket_qir-QIRProfile.BASE.ll",
    "test_pytket_qir_20-QIRProfile.BASE.ll",
    "test_pytket_qir_conditional_17-block-QIRProfile.ADAPTIVE_CREGSIZE.ll",
    "test_pytket_qir-QIRProfile.PYTKET.ll",
    "test_pytket_qir_20-QIRProfile.PYTKET.ll",
    "test_pytket_qir_conditional_17-block-QIRProfile.ADAPTIVE.ll",
    "test_pytket_qir_quantum_2-QIRProfile.ADAPTIVE.ll",
    "test_pytket_qir_2-QIRProfile.ADAPTIVE_CREGSIZE.ll",
    "test_pytket_qir_conditional_17-block-QIRProfile.AZUREADAPTIVE.ll",
    "test_pytket_qir_quantum_3-QIRProfile.ADAPTIVE.ll",
    "test_pytket_qir_2-QIRProfile.ADAPTIVE.ll",
    "test_pytket_qir_conditional_17-block-QIRProfile.PYTKET.ll",
    "test_pytket_qir_quantum_4-QIRProfile.ADAPTIVE.ll",
    "test_pytket_qir_2-QIRProfile.AZUREADAPTIVE.ll",
    "test_pytket_qir_conditional_18-QIRProfile.ADAPTIVE_CREGSIZE.ll",
    "test_pytket_qir_quantum_5-QIRProfile.ADAPTIVE.ll",
    "test_pytket_qir_2-QIRProfile.BASE.ll",
    "test_pytket_qir_conditional_18-QIRProfile.ADAPTIVE.ll",
    "test_pytket_qir_quantum-QIRProfile.ADAPTIVE.ll",
    "test_pytket_qir_2-QIRProfile.PYTKET.ll",
    "test_pytket_qir_conditional_18-QIRProfile.AZUREADAPTIVE.ll",
    "test_pytket_qir_rangepredicate.ll",
    "test_pytket_qir_3-QIRProfile.ADAPTIVE_CREGSIZE.ll",
    "test_pytket_qir_conditional_18-QIRProfile.PYTKET.ll",
    "test_pytket_qir_wasm_2-QIRProfile.ADAPTIVE_CREGSIZE.ll",
    "test_pytket_qir_3-QIRProfile.ADAPTIVE.ll",
    "test_pytket_qir_conditional_19-QIRProfile.ADAPTIVE_CREGSIZE.ll",
    "test_pytket_qir_wasm_2-QIRProfile.ADAPTIVE.ll",
    "test_pytket_qir_3-QIRProfile.AZUREADAPTIVE.ll",
    "test_pytket_qir_conditional_19-QIRProfile.ADAPTIVE.ll",
    "test_pytket_qir_wasm_2-QIRProfile.PYTKET.ll",
    "test_pytket_qir_3-QIRProfile.BASE.ll",
    "test_pytket_qir_conditional_19-QIRProfile.AZUREADAPTIVE.ll",
    "test_pytket_qir_wasm_3-QIRProfile.ADAPTIVE_CREGSIZE.ll",
    "test_pytket_qir_3-QIRProfile.PYTKET.ll",
    "test_pytket_qir_conditional_19-QIRProfile.PYTKET.ll",
    "test_pytket_qir_wasm_3-QIRProfile.ADAPTIVE.ll",
    "test_pytket_qir_4-QIRProfile.ADAPTIVE_CREGSIZE.ll",
    "test_pytket_qir_conditional_20-QIRProfile.ADAPTIVE_CREGSIZE.ll",
    "test_pytket_qir_wasm_3-QIRProfile.PYTKET.ll",
    "test_pytket_qir_4-QIRProfile.ADAPTIVE.ll",
    "test_pytket_qir_conditional_20-QIRProfile.ADAPTIVE.ll",
    "test_pytket_qir_wasm_4-QIRProfile.ADAPTIVE_CREGSIZE.ll",
    "test_pytket_qir_4-QIRProfile.AZUREADAPTIVE.ll",
    "test_pytket_qir_conditional_20-QIRProfile.AZUREADAPTIVE.ll",
    "test_pytket_qir_wasm_4-QIRProfile.ADAPTIVE.ll",
    "test_pytket_qir_4-QIRProfile.PYTKET.ll",
    "test_pytket_qir_conditional_20-QIRProfile.PYTKET.ll",
    "test_pytket_qir_wasm_4-QIRProfile.PYTKET.ll",
    "test_pytket_qir_5-QIRProfile.ADAPTIVE_CREGSIZE.ll",
    "test_pytket_qir_conditional_2-QIRProfile.ADAPTIVE_CREGSIZE.ll",
    "test_pytket_qir_wasm_5-QIRProfile.ADAPTIVE_CREGSIZE.ll",
    "test_pytket_qir_5-QIRProfile.ADAPTIVE.ll",
    "test_pytket_qir_conditional_2-QIRProfile.ADAPTIVE.ll",
    "test_pytket_qir_wasm_5-QIRProfile.ADAPTIVE.ll",
    "test_pytket_qir_5-QIRProfile.AZUREADAPTIVE.ll",
    "test_pytket_qir_conditional_2-QIRProfile.AZUREADAPTIVE.ll",
    "test_pytket_qir_wasm_5-QIRProfile.PYTKET.ll",
    "test_pytket_qir_5-QIRProfile.PYTKET.ll",
    "test_pytket_qir_conditional_2-QIRProfile.PYTKET.ll",
    "test_pytket_qir_wasm_6-QIRProfile.ADAPTIVE_CREGSIZE.ll",
    "test_pytket_qir_6-QIRProfile.ADAPTIVE_CREGSIZE.ll",
    "test_pytket_qir_conditional_3-QIRProfile.ADAPTIVE_CREGSIZE.ll",
    "test_pytket_qir_wasm_6-QIRProfile.ADAPTIVE.ll",
    "test_pytket_qir_6-QIRProfile.ADAPTIVE.ll",
    "test_pytket_qir_conditional_3-QIRProfile.ADAPTIVE.ll",
    "test_pytket_qir_wasm_6-QIRProfile.PYTKET.ll",
    "test_pytket_qir_6-QIRProfile.AZUREADAPTIVE.ll",
    "test_pytket_qir_conditional_3-QIRProfile.AZUREADAPTIVE.ll",
    "test_pytket_qir_wasm-QIRProfile.ADAPTIVE_CREGSIZE.ll",
    "test_pytket_qir_6-QIRProfile.PYTKET.ll",
    "test_pytket_qir_conditional_3-QIRProfile.PYTKET.ll",
    "test_pytket_qir_wasm-QIRProfile.ADAPTIVE.ll",
    "test_pytket_qir_7-QIRProfile.ADAPTIVE_CREGSIZE.ll",
    "test_pytket_qir_conditional_4-QIRProfile.ADAPTIVE_CREGSIZE.ll",
    "test_pytket_qir_wasm-QIRProfile.BASE.ll",
    "test_pytket_qir_7-QIRProfile.ADAPTIVE.ll",
    "test_pytket_qir_conditional_4-QIRProfile.ADAPTIVE.ll",
    "test_pytket_qir_wasm-QIRProfile.PYTKET.ll",
]


def test_check_qir_fileset() -> None:
    for file in fileslist:

        with open(f"qir/{file}") as f:
            qir_str = f.read()

            qc.qircheck(qir_str)
