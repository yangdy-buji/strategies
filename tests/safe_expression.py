"""Tiny whitelist evaluator for numeric test cases, never Python eval or Pine."""
import ast
import operator

BIN={ast.Add:operator.add,ast.Sub:operator.sub,ast.Mult:operator.mul,ast.Div:operator.truediv,ast.Mod:operator.mod}
CMP={ast.Lt:operator.lt,ast.LtE:operator.le,ast.Gt:operator.gt,ast.GtE:operator.ge,ast.Eq:operator.eq,ast.NotEq:operator.ne}
ALLOWED=(ast.Expression,ast.Name,ast.Load,ast.Constant,ast.BinOp,ast.UnaryOp,ast.BoolOp,ast.Compare,ast.Subscript,ast.And,ast.Or,ast.Not,ast.UAdd,ast.USub,*BIN,*CMP)


def evaluate(expression,**values):
    def safe_value(v):
        return type(v) in (int,float,bool,type(None)) or (type(v) in (list,tuple) and all(type(x) in (int,float,bool,type(None)) for x in v))
    if len(expression)>5000 or not all(safe_value(x) for x in values.values()):raise ValueError('Unsupported test values')
    try:tree=ast.parse(expression.strip(),mode='eval')
    except (SyntaxError,RecursionError) as exc:raise ValueError('Invalid expression') from exc
    nodes=list(ast.walk(tree))
    if len(nodes)>256 or any(not isinstance(n,ALLOWED) for n in nodes):raise ValueError('Unsupported expression syntax')
    def visit(node):
        if isinstance(node,ast.Expression):return visit(node.body)
        if isinstance(node,ast.Constant):
            if type(node.value) not in (int,float,bool,type(None)):raise ValueError('Non-numeric literal')
            return node.value
        if isinstance(node,ast.Name):
            if node.id not in values:raise ValueError('Unknown name')
            return values[node.id]
        if isinstance(node,ast.BinOp):
            left,right=visit(node.left),visit(node.right)
            if type(left) not in (int,float) or type(right) not in (int,float):raise ValueError('Only numeric arithmetic')
            return BIN[type(node.op)](left,right)
        if isinstance(node,ast.UnaryOp):
            value=visit(node.operand)
            return not value if isinstance(node.op,ast.Not) else (-value if isinstance(node.op,ast.USub) else +value)
        if isinstance(node,ast.BoolOp):
            if isinstance(node.op,ast.And):return all(visit(n) for n in node.values)
            return any(visit(n) for n in node.values)
        if isinstance(node,ast.Compare):
            left=visit(node.left)
            for op,right in zip(node.ops,node.comparators):
                right=visit(right)
                if not CMP[type(op)](left,right):return False
                left=right
            return True
        if isinstance(node,ast.Subscript):
            base=visit(node.value);index=visit(node.slice)
            if type(base) not in (list,tuple) or type(index) is not int:raise ValueError('Only numeric array indexing')
            return base[index]
        raise ValueError('Unsupported node')
    return visit(tree)
