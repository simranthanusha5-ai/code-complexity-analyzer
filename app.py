import streamlit as st
import ast
import matplotlib.pyplot as plt
import time

st.set_page_config(page_title="OptiCode", page_icon="⚡", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #fff7fb, #f9ecff, #fff1f6);
    background-size: 300% 300%;
    animation: gradientShift 10s ease infinite;
}

@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

@keyframes floatTitle {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
    100% { transform: translateY(0px); }
}

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(18px); }
    to { opacity: 1; transform: translateY(0px); }
}

@keyframes glowPulse {
    0% { box-shadow: 0 12px 30px rgba(157, 23, 77, 0.10); }
    50% { box-shadow: 0 18px 40px rgba(219, 39, 119, 0.25); }
    100% { box-shadow: 0 12px 30px rgba(157, 23, 77, 0.10); }
}

.hero {
    text-align: center;
    padding: 35px 10px 25px;
    animation: fadeInUp 0.9s ease;
}

.badge {
    display: inline-block;
    background: #ffffffcc;
    color: #9d174d;
    border: 1px solid #f9a8d4;
    padding: 8px 18px;
    border-radius: 999px;
    font-size: 13px;
    font-weight: 800;
    letter-spacing: 1.5px;
    animation: glowPulse 2.5s ease-in-out infinite;
}

.main-title {
    font-size: 60px;
    font-weight: 800;
    color: #831843;
    margin-top: 18px;
    margin-bottom: 6px;
    letter-spacing: -1.5px;
    animation: floatTitle 3s ease-in-out infinite;
}

.tagline {
    font-size: 23px;
    font-weight: 800;
    color: #be185d;
    margin-bottom: 15px;
}

.description {
    color: #4b5563;
    font-size: 17px;
    line-height: 1.7;
    max-width: 680px;
    margin: auto;
}

.card {
    background: rgba(255, 255, 255, 0.82);
    border: 1px solid rgba(244, 114, 182, 0.35);
    border-radius: 26px;
    padding: 24px;
    box-shadow: 0 18px 45px rgba(157, 23, 77, 0.12);
    margin-top: 20px;
    animation: fadeInUp 0.7s ease;
}

.metric-card {
    background: linear-gradient(180deg, #ffffff, #fff1f7);
    border: 1px solid #f9a8d4;
    border-radius: 22px;
    padding: 20px;
    text-align: center;
    box-shadow: 0 10px 25px rgba(157, 23, 77, 0.10);
    transition: 0.25s ease;
}

.metric-card:hover {
    transform: translateY(-5px);
}

.metric-value {
    font-size: 34px;
    font-weight: 800;
    color: #9d174d;
}

.metric-label {
    font-size: 13px;
    font-weight: 600;
    color: #6b7280;
}

.stButton > button {
    width: 100%;
    background: linear-gradient(90deg, #db2777, #a855f7);
    color: white;
    border: none;
    border-radius: 999px;
    padding: 14px 30px;
    font-weight: 800;
    font-size: 16px;
    box-shadow: 0 12px 25px rgba(219, 39, 119, 0.25);
    transition: 0.25s ease;
}

.stButton > button:hover {
    transform: translateY(-2px) scale(1.01);
}

textarea {
    border-radius: 18px !important;
    border: 1.5px solid #f9a8d4 !important;
}

[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.7);
    border: 1.5px dashed #f9a8d4;
    border-radius: 20px;
    padding: 16px;
}

h2, h3 {
    color: #831843 !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <div class="badge">STATIC CODE ANALYSIS</div>
    <div class="main-title">OptiCode</div>
    <div class="tagline">Detect. Analyze. Optimize.</div>
    <div class="description">
        Analyze Python code in seconds.<br>
        Detect loops, recursion, and performance bottlenecks.
    </div>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload a Python file", type=["py"])

code_input = ""

if uploaded_file is not None:
    code_input = uploaded_file.read().decode("utf-8")
    st.code(code_input, language="python")
else:
    code_input = st.text_area("Paste Python code", height=300)


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
        st.warning("Please enter or upload Python code.")

    else:
        try:
            progress = st.progress(0)
            for percent in range(100):
                time.sleep(0.003)
                progress.progress(percent + 1)

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
                            if isinstance(child.func, ast.Name) and child.func.id == node.name:
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

            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Analysis Summary")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown(
                    f'<div class="metric-card"><div class="metric-value">{loop_count}</div><div class="metric-label">Loops</div></div>',
                    unsafe_allow_html=True
                )

            with col2:
                st.markdown(
                    f'<div class="metric-card"><div class="metric-value">{function_count}</div><div class="metric-label">Functions</div></div>',
                    unsafe_allow_html=True
                )

            with col3:
                st.markdown(
                    f'<div class="metric-card"><div class="metric-value">{max_depth}</div><div class="metric-label">Loop Depth</div></div>',
                    unsafe_allow_html=True
                )

            st.write("Recursive functions:", recursive_functions)
            st.success(f"Estimated Time Complexity: {complexity}")
            st.markdown('</div>', unsafe_allow_html=True)

            st.subheader("Optimization Insights")

            if complexity == "O(1)":
                st.info("Constant-time code detected. Runtime stays stable as input grows.")
            elif complexity == "O(n)":
                st.info("Linear complexity detected. Runtime grows with input size.")
            elif complexity == "O(n²)":
                st.warning("Quadratic complexity detected. Large inputs may slow this code.")
            elif "Recursive" in complexity:
                st.warning("Recursive structure detected. Complexity depends on the recursion pattern.")
            else:
                st.warning("Higher-order complexity detected. Review nested loops for optimization.")

            st.subheader("Performance Dashboard")

            metrics = ["Loops", "Functions", "Loop Depth"]
            values = [loop_count, function_count, max_depth]

            fig, ax = plt.subplots(figsize=(8, 4))
            fig.patch.set_facecolor("#fff7fb")
            ax.set_facecolor("#fff7fb")

            colors = ["#F9A8D4", "#C4B5FD", "#FBCFE8"]

            bars = ax.bar(
                metrics,
                values,
                color=colors,
                edgecolor="#BE185D",
                linewidth=2
            )

            ax.set_ylabel("Count", fontsize=11, color="#6B7280")
            ax.set_title(
                "Code Structure Overview",
                fontsize=16,
                fontweight="bold",
                color="#831843",
                pad=20
            )

            ax.grid(axis="y", linestyle="--", alpha=0.25, color="#BE185D")
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
            ax.spines["left"].set_color("#F9A8D4")
            ax.spines["bottom"].set_color("#F9A8D4")
            ax.tick_params(colors="#6B7280", labelsize=11)

            for bar in bars:
                height = bar.get_height()
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    height + 0.05,
                    str(height),
                    ha="center",
                    va="bottom",
                    fontweight="bold",
                    color="#831843"
                )

            st.pyplot(fig)

        except SyntaxError:
            st.error("Invalid Python code. Please check your syntax.")