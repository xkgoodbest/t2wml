class RowExpression:
    def __init__(self) -> None:
        self.row_variable = None
        self.operations = []
    
    def evaluate(self, bindings: dict) -> int:
        """
        This function evaluates the row variable and find its respective index in the excel file.
        Then perform add or subtract operations to find the required row index
        based on the cell operator and cell operator argument
        :param bindings:
        :return: row variable of type int
        """
        rv = self.row_variable.evaluate(bindings)
        data = {"iterate_on": "row", "operations": dict()}
        for i in self.operations:
            value = i['cell_operator_argument'].evaluate(bindings)
            if value.isnumeric():
                if i['cell_operator'] == '+':
                    rv = rv+int(value)
                elif i['cell_operator'] == '-':
                    rv = rv-int(value)
            else:
                data['operations'][i['cell_operator']] = value
        data["row"] = rv
        if rv < -1:
            raise ValueError('Row value out of bound')
        return data
