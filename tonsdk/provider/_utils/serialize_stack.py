from base64 import b64encode
from ...boc import Cell, Slice
from ...utils import Address


def serialize_stack(elements: list[None | int | bool | Cell | Slice | Address \
                    | list | str]) -> list:
    """Prepare stack for running get method.

    Args:
        elements (list): list of elements of allowed types.

    Returns:
        list: serialized stack
    """

    stack = []

    for element in elements:
        if isinstance(element, int):
            stack.append(['int', str(element)])
        elif isinstance(element, bool):
            stack.append(['int', str(-1 if element else 0)])
        elif isinstance(element, Cell):
            stack.append(['tvm.Cell',
                          b64encode(element.to_boc(False)).decode()])
        elif isinstance(element, Slice):
            stack.append(['tvm.Slice',
                          b64encode(element.to_cell().to_boc(False)).decode()])
        elif isinstance(element, str):
            string_cell = Cell()
            string_cell.bits.write_string(element)
            stack.append(['tvm.Slice',
                          b64encode(string_cell.to_boc(False)).decode()])
        elif isinstance(element, Address):
            addr_cell = Cell()
            addr_cell.bits.write_address(element)
            stack.append(['tvm.Slice',
                          b64encode(addr_cell.to_boc(False)).decode()])
        elif type(element) == list:
            serialized_tuple = serialize_stack(element)
            stack.append(['tvm.Tuple', serialized_tuple])
        elif element is None:
            stack.append(['null'])

    return stack
