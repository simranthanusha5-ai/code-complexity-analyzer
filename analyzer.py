import ast

code = """
for i in range(10):
    print(i)
"""

tree = ast.parse(code)

loop_count = 0

for node in ast.walk(tree):
    if isinstance(node, ast.For) or isinstance(node, ast.While):
        loop_count += 1

print("Number of loops found:", loop_count)