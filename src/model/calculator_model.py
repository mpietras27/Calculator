class CalculatorModel:
    def evaluate(self, expression: str):
        try:
            result = eval(expression)

            # Remove trailing .0 for whole numbers
            if isinstance(result, float) and result.is_integer():
                return str(int(result))

            return str(result)
        except Exception:
            return "Error"