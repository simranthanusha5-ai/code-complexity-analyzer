# OptiCode ⚡

### Detect. Analyze. Optimize.

OptiCode is a Python-based static code analysis tool that estimates algorithmic complexity and identifies potential performance bottlenecks in Python programs.

Built using Python's Abstract Syntax Tree (AST), OptiCode analyzes code structure, detects loops and recursion, estimates time complexity, and visualizes results through an interactive dashboard.

---

## Live Demo

https://code-complexity-analyzer-ijmsykxpjahurhvxvk2kpg.streamlit.app/

---

## GitHub Repository

https://github.com/simranthanusha5-ai/code-complexity-analyzer

---

## Features

* Python code analysis
* Python file upload support
* Loop detection
* Nested loop detection
* Recursion detection
* Function detection
* Time complexity estimation
* Performance insights
* Interactive dashboard
* Modern Streamlit interface

---

## Tech Stack

### Frontend

* Streamlit

### Backend

* Python

### Analysis Engine

* Python AST (Abstract Syntax Tree)

### Visualization

* Matplotlib

### Deployment

* GitHub
* Streamlit Cloud

---

## How It Works

1. User uploads a Python file or pastes code.
2. The code is parsed using Python's AST module.
3. AST nodes are traversed to identify:

   * Loops
   * Nested loops
   * Functions
   * Recursive calls
4. Loop depth is calculated.
5. Time complexity is estimated.
6. Results are displayed through a visual dashboard.

---

## Example Complexity Detection

### Linear Complexity

```python
for i in items:
    print(i)
```

Estimated Complexity:

```text
O(n)
```

### Quadratic Complexity

```python
for i in items:
    for j in items:
        print(i, j)
```

Estimated Complexity:

```text
O(n²)
```

### Recursive Function

```python
def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)
```

Detected as:

```text
Recursive Function
```

---

## Project Architecture

User Input
↓
AST Parser
↓
Pattern Detection
↓
Complexity Estimator
↓
Performance Dashboard

---

## Future Improvements

* Detect O(log n) algorithms
* Detect O(n log n) algorithms
* AI-powered optimization suggestions
* PDF report generation
* Multi-language support

---

## Author

Thanusha Simran

Built as a portfolio project to explore static code analysis, algorithmic complexity estimation, AST parsing, and web application deployment using Python.
