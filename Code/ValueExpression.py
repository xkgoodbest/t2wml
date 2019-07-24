from typing import Union
from Code.utility_functions import check_if_empty


class ValueExpression:
    def __init__(self) -> None:
        self.cell_expression = None
        self.boolean_equation = None

    def evaluate(self, bindings: dict, ignore_iterator: bool = False, return_only_cell: bool = False, return_cell_and_value: bool = False) -> tuple:
        """
        This function calls evaluate function of its respective not null members
        and then finds the value of the respective column and row in the excel file
        :param bindings:
        :param ignore_iterator:
        :param return_only_cell:
        :param return_cell_and_value:
        :return:
        """
        if self.cell_expression:
            column_data, row_data = self.cell_expression.evaluate(bindings)
        else:
            cell_expression = self.boolean_equation.evaluate(bindings)
            if cell_expression:
                column_data = cell_expression[0]
                row_data = cell_expression[1]
            else:
                raise ValueError("Invalid Row and Column values")
        # when there's no iterator in $col and $row or we have to ignore the iterator
        column_value = column_data['column']
        row_value = row_data['row']
        if not ignore_iterator and column_data['operations'] or row_data['operations']:
            # when there's an iterator in $col but not in $row
            if column_data['operations'] and not row_data['operations']:
                abs_left = None
                abs_right = None
                if "-" in column_data['operations']:
                    left = column_value
                    while check_if_empty(str(bindings['excel_sheet'][row_value, left])):
                        left = left - 1
                    abs_left = column_value - left
                if "+" in column_data['operations']:
                    right = column_value
                    while check_if_empty(str(bindings['excel_sheet'][row_value, right])):
                        right = right + 1
                    abs_right = right - column_value
                if abs_left is not None and abs_right is not None:
                    if abs_left <= abs_right:
                        column_value = left
                    else:
                        column_value = right
                elif abs_left is None:
                    column_value = right
                elif abs_right is None:
                    column_value = left
            # when there's an iterator in $row but not in $col
            elif not column_data['operations'] and row_data['operations']:
                abs_up = None
                abs_down = None
                if "-" in row_data['operations']:
                    up = row_value
                    while check_if_empty(str(bindings['excel_sheet'][up, column_value])):
                        up = up - 1
                    abs_up = row_value - up
                if "+" in row_data['operations']:
                    down = row_value
                    while check_if_empty(str(bindings['excel_sheet'][down, column_value])):
                        down = down + 1
                    abs_down = down - row_value
                if abs_up is not None and abs_down is not None:
                    if abs_up <= abs_down:
                        row_value = up
                    else:
                        row_value = down
                elif abs_up is None:
                    row_value = down
                elif abs_down is None:
                    row_value = up
            # when there are iterators in both $col and $row
            else:
                raise Exception('$col and $row cannot be iterators simultaneously')
        if return_only_cell:
            return column_value, row_value
        elif return_cell_and_value:
            return column_value, row_value, str(bindings['excel_sheet'][row_value, column_value])
        else:
            return str(bindings['excel_sheet'][row_value, column_value])

    # def get_cell(self, bindings: dict) -> tuple:
    #     """
    #     This function returns the cell index on which this expression evaluates
    #     :param bindings:
    #     :return:
    #     """
    #     if self.cell_expression:
    #         ce, re = self.cell_expression.evaluate(bindings)
    #     else:
    #         cell_expression = self.boolean_equation.evaluate(bindings)
    #         if cell_expression:
    #             ce = cell_expression[0]
    #             re = cell_expression[1]
    #         else:
    #             raise ValueError("Invalid Row and Column values")
    #     return ce, re
    #
    # def evaluate_and_get_cell(self, bindings: dict) -> tuple:
    #     """
    #     This function evaluates the Value expression and returns the result along with the cell index
    #     :param bindings:
    #     :return:
    #     """
    #     if self.cell_expression:
    #         ce, re = self.cell_expression.evaluate(bindings)
    #     else:
    #         cell_expression = self.boolean_equation.evaluate(bindings)
    #         if cell_expression:
    #             ce = cell_expression[0]
    #             re = cell_expression[1]
    #         else:
    #             raise ValueError("Invalid Row and Column values")
    #     return ce, re, str(bindings['excel_sheet'][re, ce])
