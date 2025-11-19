from model.calculator_model import CalculatorModel
from utils.updater import check_for_update, apply_update


class CalculatorController:
    def __init__(self, view):
        self.view = view
        self.model = CalculatorModel()

        # Attach controller to the view
        self.view.set_controller(self)

        # Internal calculator state
        self.entry = "0"         # What user is typing
        self.history = ""        # The expression before hitting "="
        self.last_result = None  # Used to prevent concatenation after "="
        self.just_evaluated = False

        self.next_entry_starts_new_number = False

        self.history_internal = "" # prevents engine from contamination new calculation

        # Check for GitHub updates silently
        self._check_for_updates()

    # ----------------------------------------------------
    #   UPDATER CHECK
    # ----------------------------------------------------
    def _check_for_updates(self):
        update_available, download_url = check_for_update()
        if update_available and download_url:
            apply_update(download_url)

    # ----------------------------------------------------
    #   VIEW → CONTROLLER ENTRY POINT
    # ----------------------------------------------------
    def handle_button(self, text):
        if text.isdigit():  # 0–9
            self._handle_digit(text)

        elif text in {"+", "–", "×", "÷"}:
            self._handle_operator(text)

        elif text == ".":
            self._handle_decimal()

        elif text == "(":
            self._handle_open_paren()

        elif text == ")":
            self._handle_close_paren()

        elif text == "C":
            self._handle_clear()

        elif text == "±":
            self._handle_plus_minus()

        elif text == "=":
            self._handle_equals()

        self._update_view()

    # ----------------------------------------------------
    #   DIGITS
    # ----------------------------------------------------
    def _handle_digit(self, digit):

        if self.just_evaluated:
            self.history = ""              # <-- CRITICAL
            self.entry = digit
            self.just_evaluated = False
            self.next_entry_starts_new_number = False
            return

        if self.next_entry_starts_new_number:
            self.entry = digit
            self.next_entry_starts_new_number = False
            return

        if self.entry == "0":
            self.entry = digit
        else:
            self.entry += digit



    # ----------------------------------------------------
    #   OPERATORS
    # ----------------------------------------------------
    def _normalize_op(self, op):
        return {
            "×": "*",
            "÷": "/",
            "–": "-"
        }.get(op, op)

    def _handle_operator(self, op):
        op_norm = self._normalize_op(op)

        # Case: operator pressed after "=" → continue from entry
        if self.just_evaluated:
            self.history = str(self.entry)
            self.entry = ""
            self.just_evaluated = False

        # Add entry to history
        if self.entry:
            self.history += self.entry

        # Add operator
        self.history += op_norm

        # Prepare for next number
        self.entry = ""                                  # <-- CRITICAL FIX
        self.next_entry_starts_new_number = False


    # ----------------------------------------------------
    #   DECIMAL
    # ----------------------------------------------------
    def _handle_decimal(self):
        if self.just_evaluated:
            self.entry = "0."
            self.just_evaluated = False
            return

        if "." not in self.entry:
            self.entry += "."

    # ----------------------------------------------------
    #   PARENTHESES
    # ----------------------------------------------------
    def _handle_open_paren(self):
        # Start new expression after "="
        if self.just_evaluated:
            self.history = ""
            self.entry = ""
            self.just_evaluated = False

        # Add "(" to history. Parentheses belong to structure, not entry.
        self.history += "("
        self.entry = ""                     # <-- CRITICAL FIX
        self.next_entry_starts_new_number = False

    def _handle_close_paren(self):
        # Allow close only if there is something to close
        if "(" in (self.history + self.entry):
            self.entry += ")"

    # ----------------------------------------------------
    #   CLEAR
    # ----------------------------------------------------
    def _handle_clear(self):
        self.entry = "0"
        self.history = ""
        self.just_evaluated = False

    # ----------------------------------------------------
    #   PLUS/MINUS
    # ----------------------------------------------------
    def _handle_plus_minus(self):
        if self.entry.startswith("-"):
            self.entry = self.entry[1:]
        else:
            if self.entry != "0":
                self.entry = "-" + self.entry

    # ----------------------------------------------------
    #   EQUALS (EVALUATE)
    # ----------------------------------------------------
    def _handle_equals(self):
        if self.just_evaluated:
            return  # prevent repeated "="

        expression = self.history + self.entry

        # Replace UI symbols
        expression = expression.replace("×", "*")
        expression = expression.replace("÷", "/")
        expression = expression.replace("–", "-")

        result = self.model.evaluate(expression)

        # Display result
        self.entry = str(result)
        self.last_result = result

        # Show expression briefly
        self.history = expression + " ="

        # Set evaluation flags
        self.just_evaluated = True
        self.next_entry_starts_new_number = False

        # INTERNAL FIX: prevent expression from being reused!
        # Without this line the OLD expression contaminates the next calc.
        self.history_internal = ""      # <-- critical

    # ----------------------------------------------------
    #   VIEW UPDATE
    # ----------------------------------------------------

    def _paren_open(self):
        #Return True if expression is inside parentheses.
        expr = self.history + self.entry
        return expr.count("(") > expr.count(")")


    def _update_view(self):

        # Show full expression being built
        full = self.history + self.entry

        # Show full expression on top
        self.view.history_label.setText(full)

        # Show ONLY entry on bottom
        if self.entry == "":
            self.view.entry_label.setText("0")
        else:
            self.view.entry_label.setText(self.entry)



