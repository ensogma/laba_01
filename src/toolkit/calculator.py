# from .errors import EmptyExpressionError
# from errors import ToolkitError
from errors import (
    TwoBinaryOperatorsError,
    EmptyExpressionError,
    MissingOperandError,
    UnknownUnitError,
    
)
a='1.05+3.2--=-(23.5+8.1)/2.7-(+6.8)/2+'
a='3\t+\n4'
a='12+2543-34*4/5'



a='3+4'
a='3 - -2'
a='3 * -2'
a='*2'
a='3 +'
a='3 + * 2'
a='3 5'



import re


# _GAP_RE = re.compile(r"[0-9.]\s+[0-9.]")


# def check_gaps(a: str) -> None:
#     if _GAP_RE.search(a):
#         raise MissingOperandError("missed unary beetween nums")
# check_gaps(a)
OPERATORS = {"+","-","*","/"}
SIGNS = {"+","-"}
# while ' ' in a:
#     a=a.replace(' ', '')
# a=''

print(a)
nums='0123456789'
DIGITS=set('0123456789')
def is_num(tok):
    if tok.count('.')>1:
        return False
    digits_only = tok.replace('.','')
    return digits_only !='' and  set(digits_only)<=DIGITS
# print(DIGITS)


def tokenization(a):
    cur_n = ''
    tokens = []
    for c in a:
        if c in nums:
            cur_n+=c 
        elif c=='.':
            cur_n+=c
        else:
            if len(cur_n)!=0 and c!=' ':
                tokens.append(cur_n)
                cur_n=''
            if c!=' ':
                tokens.append(c)
    if len(cur_n)!=0 and c!=' ':
        tokens.append(cur_n)
    return tokens
tokenized = tokenization(a)
print(tokenized)
# for el in tokenized:
    # print(is_num(el),end=' ')
# print(' ')
# kal = ['1++++4',
#        '1*+2',
#        '',
#        ] 
# print(is_num('3'))
def validation(tokenized):
    if not tokenized:
        raise EmptyExpressionError('empty expression')
    if "+" not in set(a) or "-" not in set(a) or "*" not in set(a) or "/" not in set(a):
        print
    expect_num = True
    prev_was_unary = False
    beggining=True
    for c in tokenized:
        is_op = c in OPERATORS
        is_dig = is_num(c)
        if c not in OPERATORS and not is_dig:
            raise UnknownUnitError(f"Unknwon unit '{c}")
        else:
            if expect_num:
                if not is_op:
                    expect_num=False
                    prev_was_unary=False
                elif c in SIGNS and not prev_was_unary:
                    prev_was_unary=True
                elif beggining:
                    beggining=False
                    raise MissingOperandError(f"missed operand before '{c}'")
                else:
                    raise TwoBinaryOperatorsError(
                        f" lots of operators "
                    )
            else:
                if not is_op:
                    raise MissingOperandError("missed operand")    
                expect_num=True
        beggining=False
    if expect_num:
        raise MissingOperandError(f"expression finishes by{tokenized[-1]}")
    # return(0)
validation(tokenized)

def calculation():
    pass