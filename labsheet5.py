
def precedence(op):
    if op == '+' or op == '-':
        return 1
    if op == '*' or op == '/':
        return 2
    if op == '^':
        return 3
    return 0


def infix_to_postfix(exp):
    stack = []
    result = ""

    for ch in exp:
        if ch.isalnum():
            result += ch

        elif ch == '(':
            stack.append(ch)

        elif ch == ')':
            while stack and stack[-1] != '(':
                result += stack.pop()
            if stack:
                stack.pop()

        else:
            while (stack and stack[-1] != '(' and
                   (precedence(stack[-1]) > precedence(ch) or
                   (precedence(stack[-1]) == precedence(ch)
                    and ch != '^'))):
                result += stack.pop()
            stack.append(ch)

    while stack:
        result += stack.pop()

    return result


exp = input("Enter infix expression: ")
print("Postfix expression:", infix_to_postfix(exp))