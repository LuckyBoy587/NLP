# AI Agent Workflow Instructions

## Overview
This repository uses an AI agent that operates in exactly one of two modes based on the task: **Python Script Mode (.py)** or **Jupyter Notebook Mode (.ipynb)**. The workflow is divided into five distinct phases to ensure consistency and correctness.

### Key Rules
- **Tool-Driven Execution:** Browser automation, compilation, and result extraction are handled exclusively by MCP tools.
- **No Manual Simulation:** The agent must never attempt to replicate browser behavior manually.
- **Mode Selection:** Select exactly one mode per question.

---

## 🚦 PHASE 1: Discovery & Mode Selection
Determine the required output type before taking action.

### 🐍 Python Script Mode (.py)
*Select if:*
- The platform provides an Ace Editor.
- The task expects printed output.
- The task mentions `.py`, code execution, compilation, or checking.

### 📓 Jupyter Notebook Mode (.ipynb)
*Select if:*
- The task includes plot images.
- The task requires visual output.
- The dataset is provided via a ZIP download.
- The output is explicitly or implicitly a notebook.

---

## 🔍 PHASE 2: Question Analysis & Environment Setup
Read the question directly from the webpage and prepare context.

### 🐍 Python Script Mode (.py)
1. **Identify Target File:** Use the **File Identification Protocol** to determine the filename (e.g., `Concept_Q1.py`).
2. **Understand Constraints:** Treat as ML-related homework. Output must match the expected format exactly.
3. **Execution Awareness:** All execution and validation occur via the `test_against_sample_testcases` or `compile_code` MCP tools.

### 📓 Jupyter Notebook Mode (.ipynb)
1. **Locate Dataset:** Identify the ZIP download link (do not click).
2. **Search Data Folder:** Locate the corresponding dataset in the `data/` folder.
3. **Identify File Type:** Determine if the dataset is CSV or XLSX.
4. **Environment Check:** If the required dataset is missing, stop and report an error.

---

## 🛠️ PHASE 3: Implementation & Development

### 🐍 Python Script Mode (.py)
- **Generate Code:** Write clean Python code without extra prints, debug logs, or inline comments.
- **Dataset Input Rule:** Always read datasets using:
  ```python
  os.path.join(sys.path[0], input())
  ```
- **TensorFlow Warning Policy:** If using TensorFlow related modules, include:
  ```python
  import os
  os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

  import spacy
  ```
  as the first lines of code in the file, then start importing other modules like spacy, nltk, etc.
- **Injection & Execution Rule:** Use the `test_against_sample_testcases` or `compile_code` MCP tools for code injection, compilation, and result extraction. **Do NOT inject code via JavaScript.**

### 📓 Jupyter Notebook Mode (.ipynb)
- **Create Notebook:** Create a valid `.ipynb` using an absolute path.
- **Structure Rules:**
  - **Cell 1:** Imports & setup.
  - **Cell 2:** Dataset loading (from CWD).
  - **Cell 3+:** One plot per cell.
- **Plot Priority:** Visual similarity (axes, titles, legends, colors, styles) > code elegance.

---

## 🧪 PHASE 4: Execution & Verification

### 🐍 Python Script Mode (.py)
- **Critical Rule:** **NO LOCAL TESTING.**
- **Single Source of Truth:** Use the `test_against_sample_testcases` (for testcase validation) or `compile_code` (for general execution) MCP tools exclusively.
- **Iterative Fix Policy:**
  1. Analyze mismatch in `expected`, `actual`, and `testcase_result` fields (from `test_against_sample_testcases`) or standard output (from `compile_code`).
  2. Fix code.
  3. Re-run the appropriate execution tool until all testcases pass or the desired output is achieved.

### 📓 Jupyter Notebook Mode (.ipynb)
- **Full Execution:** Run all cells top-to-bottom.
- **Visual Verification:** Ensure plots match reference images.
- **Clean State:** Ensure no broken or commented-out cells.

---

## 💾 PHASE 5: Finalization & Cleanup

### 🐍 Python Script Mode (.py)
- **Write-Back Rule:** Write the final clean code to the `.py` file **only after** MCP verification succeeds.
- **Clean Code Only:** No experimental or intermediate code.

### 📓 Jupyter Notebook Mode (.ipynb)
- **Save Notebook:** Save in a clean execution state.
- **Cleanup:** Remove temporary files (except the final notebook).

---

## ✍️ PROTOCOLS & POLICIES

### File Identification Protocol (PY Mode)
```javascript
const header = document.querySelector('[aria-labelledby="header-title-cont"]');
const text = header ? header.innerText : "";
const typeMatch = text.match(/(Concept|Practice)/i);
const qMatch = text.match(/Q\s?(\d+)/i);

return {
  type: typeMatch
    ? typeMatch[0].charAt(0).toUpperCase() + typeMatch[0].slice(1).toLowerCase()
    : "Unknown",
  qNumber: qMatch ? qMatch[1] : "X",
  fullTitle: text
};
```

---

### 🔎 DATASET DISCOVERY & INSPECTION POLICY (PY Mode)

#### 🚫 Local Dataset Access Rule
- The agent must **never** search for, open, inspect, or infer datasets from the local filesystem.
- The agent must **not** assume column names, shapes, dtypes, or sample values.
- The agent must **not** attempt to inspect datasets using local Python execution.
- **The local system is not a source of truth for datasets.**

#### ✅ Dataset Inspection via MCP Tool (MANDATORY)
If the agent needs any information about the dataset (column names, row count, data types, missing values, sample records, or target variables), it must do so by calling:
`compile_code(code: string, stdin_input: string | None)` or `test_against_sample_testcases(code: string)`

Use simple, minimal inspection code:
```python
print(df.head())
print(df.columns)
print(df.shape)
print(df.info())
```

**This inspection code must:**
- Read the dataset using `os.path.join(sys.path[0], input())`.
- Pass the dataset name via `stdin_input` if using `compile_code`.
- Run only on the webpage.
- Be treated as exploratory (not final submission code).

#### 🔁 Iterative Understanding Rule
1. Write minimal inspection code.
2. Call `compile_code` or `test_against_sample_testcases`.
3. Observe actual output from the platform.
4. Update understanding of the dataset.
5. Rewrite final solution code.
6. Call `test_against_sample_testcases` again for full validation.

**At no point should dataset understanding come from assumptions or local inspection.**

#### ❌ Explicitly Forbidden
- Guessing dataset schema.
- Hardcoding column names without verification.
- Reading files locally “just to check”.
- Using prior memory of similar datasets.

#### 🧠 Principle
If the agent doesn’t know something about the dataset, **it must ask the browser — not the filesystem.**

### ✅ Core Principles
- **Correctness > Cleverness**
- **Browser Truth > Assumptions**
- **Verify Before Saving**
- **Tool-Driven Execution, Not Prompt-Driven**
- **Homework Mindset, Not Production Heroics**

### 🚨 Absolute Rules
- Never reload the page.
- Never test Python locally.
- Never check other Python files in the workspace to identify how to code; use the webpage's question and description as the **only** source of information.
- In `.py` mode, always read datasets as `os.path.join(sys.path[0], input())`.
- Never bypass the `test_against_sample_testcases` or `compile_code` MCP tools.
- If the mcp tool call to `test_against_sample_testcases` returns status as PASS for all testcases, consider that code as the final code.

---

### 🛠️ Tool Definitions

#### `compile_code(code: str, stdin_input: str | None = None) -> dict`
Paste code into the webpage's Ace editor(s), trigger compilation, and return the execution result extracted from the DOM.
- **Input:**
  - `code`: Full source code to paste and compile.
  - `stdin_input`: Optional input for the program's stdin.
- **Output (Success):** `{"status": "OK", "result": string, "compiler_message": string}`
- **Output (Failure):** `{"error": string}`
- **Rules:** Results are returned only from visible DOM content. Timeout results in an error. Success and error are mutually exclusive.
