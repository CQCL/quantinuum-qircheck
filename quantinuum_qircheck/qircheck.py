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

"""
check for QIR module if it is compatible with quantinuum devices
"""

import re
from typing import Callable, Union

import pyqir as pq


def qubit_number_regex_builder(gate_name: str, greater_than_1: bool = False) -> str:
    lower_bound = 2 if greater_than_1 else 1
    return f"__quantum__qis__{gate_name}([{lower_bound}-9]|[1-4][0-9]|[5][0-8])__body"


def is_qir_name(gate_name: str, fun_name: str, greater_than_1: bool = False) -> bool:
    gate_regex = qubit_number_regex_builder(gate_name, greater_than_1)
    gate_re = re.compile(gate_regex)
    return gate_re.match(fun_name) is not None


def is_barrier(gate_name: str) -> bool:
    return is_qir_name("barrier", gate_name)


def is_order(gate_name: str) -> bool:
    return is_qir_name("order", gate_name, greater_than_1=True)


def is_group(gate_name: str) -> bool:
    return is_qir_name("group", gate_name, greater_than_1=True)


def is_phi(instr: pq.Instruction) -> bool:
    return isinstance(instr, pq.Phi)


def is_select(instr: pq.Instruction) -> bool:
    return isinstance(instr, pq.Call) and instr.opcode == pq.Opcode.SELECT


def is_wasm_call_instr(instr: pq.Instruction, functions: list[pq.Function]) -> bool:
    """Indicate whether a QIR instruction is a call to a wasm function.

    Parameters
    ----------
    instr: Instruction
    An instruction in pyqir's model of a QIR program.

    functions: list[Function]
    A list of functions (declared or defined) in pyqir's representation of a QIR program.

    Returns
    -------
    bool"""
    if isinstance(instr, pq.Call):
        return is_wasm_call(instr, functions)
    return False


def is_wasm_call(fun_call: pq.Call, functions: list[pq.Function]) -> bool:
    """Indicate whether a QIR function call is a call to a wasm function

    Parameters
    ----------
    fun_call: Call
    A function call instruction in pyqir's representation of a QIR program.

    functions: list[Function]
    A list of functions (declared or defined) in pyqir's representation of a QIR program.

    Returns
    -------
    bool"""
    return has_wasm_attr(fun_call.callee.name, functions)


def has_wasm_attr(gate_name: str, functions: list[pq.Function]) -> bool:
    """Indicates whether the QIR gate's function definition was marked with the { "wasm" } group attribute

    Parameters
    ----------
    gate_name: str
    represents the name of the gate_name that we are inspecting the attributes for

    functions: list[Function]
    a list of pyqir function objects corresponding to QIR function declarations/definitions
    These can have attributes defined on them

    Returns
    -------
    bool"""
    for fun in functions:
        if fun.name == gate_name:
            return "wasm" in fun.attributes.func
    return False


def is_classical_op(instr: pq.Instruction) -> bool:
    op_opcodes = [
        pq.Opcode.ADD,
        pq.Opcode.SUB,
        pq.Opcode.MUL,
        pq.Opcode.UDIV,
        pq.Opcode.SDIV,
        pq.Opcode.UREM,
        pq.Opcode.SREM,
        pq.Opcode.AND,
        pq.Opcode.OR,
        pq.Opcode.XOR,
        pq.Opcode.SHL,
        pq.Opcode.LSHR,
        pq.Opcode.ASHR,
        pq.Opcode.FADD,
        pq.Opcode.FSUB,
        pq.Opcode.FMUL,
        pq.Opcode.FDIV,
        pq.Opcode.FREM,
        pq.Opcode.FNEG,
        pq.Opcode.ICMP,
        pq.Opcode.FCMP,
        pq.Opcode.ZEXT,
        pq.Opcode.SELECT,
    ]
    return isinstance(instr, pq.Instruction) and instr.opcode in op_opcodes


class ValidationError:
    # pylint: disable=too-few-public-methods
    def __init__(self, instr: pq.Instruction, line_num: int):
        self.error_message = f"Encountered Unexpected Instruction {str(instr)}"
        self.line_num = line_num


def validate_qir_base(qir_prog: pq.Module) -> bool:
    """Validate that the QIR corresponds to a valid quantinuum profile
    program that we can support, allowing pytket creg functions.
    This will return true or raises a ValidationError"""

    def _is_valid_call_help(instr: pq.Instruction) -> bool:
        return is_valid_call(instr, qir_prog.functions)

    if not isinstance(qir_prog.functions, list):
        raise ValueError(
            "Expected the QIR file to have at least one function but none was found",
            -1,
        )
    main_fun: pq.Function = next(filter(pq.is_entry_point, qir_prog.functions))
    if not main_fun:
        raise ValueError(
            "Expected the QIR file to have an entrypoint function "
            "but none was found",
            -1,
        )
    num_qubits = pq.required_num_qubits(main_fun)
    if not isinstance(num_qubits, int):
        raise ValueError(
            "Expected the QIR file to have qubit count specified "
            "but no annotation was found",
            -1,
        )
    num_results = pq.required_num_results(main_fun)
    if not isinstance(num_results, int):
        raise ValueError(
            "Expected the QIR file to have measurement result count "
            "specified but no annotation was found",
            -1,
        )

    line_num = 1
    i1_env: dict[str, pq.Call] = {}
    for block in main_fun.basic_blocks:
        for instr in block.instructions:
            if instr.opcode == pq.Opcode.BR:
                break
            if isinstance(instr, pq.Call) and instr.name:
                i1_env[instr.name] = instr

            fun_collection: list[Callable[[pq.Instruction], bool]] = [
                _is_valid_call_help,
                is_jump_instr,
                is_ret_instr,
                is_classical_op,
                is_phi,
                is_select,
            ]
            if not any(fun(instr) for fun in fun_collection):
                raise ValidationError(instr, line_num)
            line_num += 1
    return True


def is_valid_quantum_call(instr: pq.Call) -> bool:
    """Determines whether a gate application has a valid form"""
    quantum_instr_set = {
        "__quantum__qis__reset__body",
        "__quantum__qis__h__body",
        "__quantum__qis__y__body",
        "__quantum__qis__anynonzero__body",
        "__quantum__qis__read_result__body",
        "__quantum__qis__cnot__body",
        "__quantum__qis__cz__body",
        "__quantum__qis__x__body",
        "__quantum__qis__z__body",
        "__quantum__qis__rz__body",
        "__quantum__qis__ry__body",
        "__quantum__qis__rx__body",
        "__quantum__qis__mz__body",
        "__quantum__qis__s__body",
        "__quantum__qis__t__body",
        "__quantum__qis__s__adj",
        "__quantum__qis__t__adj",
        "__quantum__qis__zz__body",
        "__quantum__qis__u1q__body",
        "__quantum__qis__rzz__body",
        "__quantum__qis__rxxyyzz__body",
        # for tket support
        "__quantum__qis__zzmax__body",
        "__quantum__qis__phasedx__body",
        "__quantum__qis__zzphase__body",
        "__quantum__qis__tk2__body",
        # for pytket-qir support
        "__quantum__qis__sleep__body",
        "create_creg",
        "set_creg_to_int",
        "get_int_from_creg",
        "set_creg_bit",
        "get_creg_bit",
        "mz_to_creg_bit",
    }
    special_gate_funs = [is_barrier, is_order, is_group]
    if isinstance(instr, pq.Call):
        fun_name = instr.callee.name
        return (fun_name in quantum_instr_set) or any(
            fun(fun_name) for fun in special_gate_funs
        )


def is_valid_classical_call(instr: pq.Call) -> bool:
    """Determines whether a gate application has a valid form"""
    classical_instr_set = {
        "__quantum__rt__int_record_output",
        "__quantum__rt__result_record_output",
        "__quantum__rt__bool_record_output",
        "__quantum__rt__tuple_start_record_output",
        "__quantum__rt__tuple_end_record_output",
        "__quantum__rt__array_start_record_output",
        "__quantum__rt__array_end_record_output",
        "__quantum__rt__tuple_record_output",
        "__quantum__rt__array_record_output",
    }
    # for real support we should check an annotation instead of checking the name
    return instr.callee.name in classical_instr_set


def is_valid_call(instr: pq.Instruction, functions: list[pq.Function]) -> bool:
    """Determines whether the qir call instruction was valid"""
    return isinstance(instr, pq.Call) and any(
        (
            is_valid_quantum_call(instr),
            is_valid_classical_call(instr),
            is_valid_result_equal_instr(instr),
            is_result_get_one(instr),
            is_result_get_zero(instr),
            is_wasm_call(instr, functions),
        )
    )


def is_ret_instr(instr: pq.Instruction) -> bool:
    return isinstance(instr, pq.Instruction) and instr.opcode == pq.Opcode.RET


def is_jump_instr(instr: pq.Instruction) -> bool:
    return (
        isinstance(instr, pq.Instruction)
        and instr.opcode == pq.Opcode.BR
        and len(instr.operands) == 1
    )


def is_valid_read_result_instr(instr: pq.Instruction) -> bool:
    """Determines whether an llvm function call is a built-in QIR read result function"""
    if not isinstance(instr, pq.Call):
        return False
    return instr.callee.name == "__quantum__qis_read_result__body"


def is_valid_result_equal_instr(instr: pq.Instruction) -> bool:
    """Determines whether an llvm function call is a QIR result equal function"""
    if not isinstance(instr, pq.Call):
        return False
    return instr.callee.name == "__quantum__rt__result_equal"


def is_result_get_one(instr: pq.Instruction) -> bool:
    """Determines if the rt_get_one function was called"""
    if not isinstance(instr, pq.Call):
        return False
    return instr.callee.name == "__quantum__rt_get_one"


def is_result_get_zero(instr: pq.Instruction) -> bool:
    """Determines whether the _rt_get_zero function was called"""
    if not isinstance(instr, pq.Call):
        return False
    return instr.callee.name == "__quantum__rt_get_zero"
