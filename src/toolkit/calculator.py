from .errors import (
    DivisionByZeroError,
    EmptyExpressionError,
    InvalidCharacterError,
    InvalidValueError,
    MissingOperandError,
    TwoBinaryOperatorsError,
    UnbalancedParenthesesError,
)

OPERATORS = {"+", "-", "*", "/", "(", ")"}
BINARY = {"+", "-", "*", "/"}
SIGNS = {"+", "-"}
DIGITS = set("0123456789")


def is_num(tok):
    if tok.count(".") > 1:
        return False
    digits_only = tok.replace(".", "")
    return digits_only != "" and set(digits_only) <= DIGITS


def tokenization(a):
    cur_n = ""
    tokens = []
    for c in a:
        if c in DIGITS or c == ".":
            cur_n += c
        else:
            if len(cur_n) != 0:
                if cur_n.count(".") > 1 or cur_n == ".":
                    raise InvalidValueError(f"неверное число '{cur_n}'")
                tokens.append(cur_n)
                cur_n = ""
            if c.isspace():
                continue
            if c not in OPERATORS:
                raise InvalidCharacterError(f"недопустимый символ '{c}'")
            tokens.append(c)
    if len(cur_n) != 0:
        if cur_n.count(".") > 1 or cur_n == ".":
            raise InvalidValueError(f"неверное число '{cur_n}'")
        tokens.append(cur_n)
    if not tokens:
        raise EmptyExpressionError("пустое выражение")
    return tokens


def validation(tokenized):
    beggining = True
    if not tokenized:
        raise EmptyExpressionError("empty expression")
    expect_num = True
    prev_was_unary = False
    depth = 0
    prev = ""
    for c in tokenized:
        is_op = c in OPERATORS
        if expect_num:
            if c == "(":
                depth += 1
                prev_was_unary = False
            elif c == ")":
                raise MissingOperandError(f"missed operand before '{c}'")
            elif not is_op:
                expect_num = False
                prev_was_unary = False
            elif c in SIGNS and not prev_was_unary:
                prev_was_unary = True
            elif prev in BINARY:
                raise TwoBinaryOperatorsError(f"lots of operators: '{prev}' and '{c}'")
            elif beggining != True or beggining and c in "*/":
                raise MissingOperandError(f"missed operand before '{c}'")
        else:
            if c == ")":
                depth -= 1
                if depth < 0:
                    raise UnbalancedParenthesesError("extra closing parenthesis")
            elif c in BINARY:
                expect_num = True
                prev_was_unary = False
            elif beggining != True:
                raise MissingOperandError(f"missed operator before '{c}'")
            elif beggining and c in "*/":
                raise MissingOperandError(f"missed operand before '{c}'")
        beggining = False
        prev = c
    if depth > 0:
        raise UnbalancedParenthesesError("unclosed parenthesis")
    if expect_num:
        raise MissingOperandError(f"expression finishes by '{tokenized[-1]}'")


def priorities(op):
    if op == "neg":
        return 3
    elif op in "*/":
        return 2
    elif op in "-+":
        return 1


def calculation(tokens):

    def transition():
        stack = []
        out = []

        for i in range(len(tokens)):
            tok = tokens[i]
            if is_num(tok):
                out.append(tok)
            elif tok in SIGNS and (
                i == 0 or tokens[i - 1] in BINARY or tokens[i - 1] == "("
            ):
                if tok == "-":
                    stack.append("neg")
            elif tok in BINARY:
                while (
                    stack
                    and stack[-1] != "("
                    and priorities(stack[-1]) >= priorities(tok)
                ):
                    out.append(stack.pop())
                stack.append(tok)
            elif tok == "(":
                stack.append(tok)
            else:
                while stack[-1] != "(":
                    out.append(stack.pop())
                stack.pop()
        while stack:
            out.append(stack.pop())
        return out

    rpn = transition()
    stack = []
    for tok in rpn:
        if tok == "neg":
            stack.append(-stack.pop())
        elif tok in BINARY:
            y = stack.pop()
            x = stack.pop()
            if tok == "+":
                stack.append(x + y)
            elif tok == "-":
                stack.append(x - y)
            elif tok == "*":
                stack.append(x * y)
            else:
                if y == 0:
                    raise DivisionByZeroError("деление на ноль")
                stack.append(x / y)
        else:
            stack.append(float(tok))
    return stack[0]


def calculate(expression):
    tokenized = tokenization(expression)
    validation(tokenized)
    return calculation(tokenized)
