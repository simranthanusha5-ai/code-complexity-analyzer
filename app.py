import streamlit as st
import ast
import matplotlib.pyplot as plt

st.title("Code Complexity Analyzer")

st.write("Paste your Python code or upload a .py file to analyze its time complexity.")

uploaded_file = st.file_uploader("Upload a Python file", type=["py"])

code_input = ""

if uploaded_file is not None:
    code_input = uploaded_file.read().decode("utf-8")
    st.code(code_input, language="python")
else:
    code_input = st.text_area("Enter Python Code", height=300)


class LoopDepthAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.current_depth = 0
        self.max_depth = 0

    def visit_For(self, node):
        self.current_depth += 1
        self.max_depth = max(self.max_depth, self.current_depth)
        self.generic_visit(node)
        self.current_depth -= 1

    def visit_While(self, node):
        self.current_depth += 1
        self.max_depth = max(self.max_depth, self.current_depth)
        self.generic_visit(node)
        self.current_depth -= 1


if st.button("Analyze Code"):

    if code_input.strip() == "":
        st.warning("Please enter or upload some Python code.")

    else:
        try:
            tree = ast.parse(code_input)

            loop_count = 0
            function_count = 0
            recursive_functions = []

            for node in ast.walk(tree):

                if isinstance(node, (ast.For, ast.While)):
                    loop_count += 1

                if isinstance(node, ast.FunctionDef):
                    function_count += 1

                    for child in ast.walk(node):
                        if isinstance(child, ast.Call):
                            if (
                                isinstance(child.func, ast.Name)
                                and child.func.id == node.name
                            ):
                                recursive_functions.append(node.name)

            depth_analyzer = LoopDepthAnalyzer()
            depth_analyzer.visit(tree)

            max_depth = depth_analyzer.max_depth

            if recursive_functions:
                complexity = "Recursive Function"
            elif max_depth == 0:
                complexity = "O(1)"
            elif max_depth == 1:
                complexity = "O(n)"
            elif max_depth == 2:
                complexity = "O(n²)"
            elif max_depth == 3:
                complexity = "O(n³)"
            else:
                complexity = f"O(n^{max_depth})"

            st.subheader("Analysis Report")

            st.write("Number of loops:", loop_count)
            st.write("Number of functions:", function_count)
            st.write("Recursive Functions:", recursive_functions)
            st.write("Maximum Loop Depth:", max_depth)

            st.success(f"Estimated Time Complexity: {complexity}")

            st.subheader("Performance Insights")

            if complexity == "O(1)":
                st.info(
                    "Constant time operation. Performance remains stable as input grows."
                )

            elif complexity == "O(n)":
                st.info(
                    "Linear complexity. Runtime grows proportionally with input size."
                )

            elif complexity == "O(n²)":
                st.warning(
                    "Quadratic complexity detected. Performance may degrade for large inputs."
                )

            elif "Recursive" in complexity:
                st.warning(
                    "Recursive function detected. Complexity depends on recursion pattern."
                )

            else:
                st.warning(
                    "Higher-order complexity detected. Consider optimization."
                )

            st.subheader("Visual Dashboard")

            metrics = ["Loops", "Functions", "Max Loop Depth"]
            values = [loop_count, function_count, max_depth]

            fig, ax = plt.subplots()
            ax.bar(metrics, values)
            ax.set_ylabel("Count")
            ax.set_title("Code Analysis Metrics")

            st.pyplot(fig)

        except SyntaxError:
            st.error("Invalid Python code.")