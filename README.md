# CODEWEAVER — Alpha.1 Project Understanding

**CODEWEAVER** is a deterministic, read-only software project understanding system designed as a Human-Controlled AI Developer Assistant framework.

Alpha.1 establishes a clean baseline for exploring codebases, collecting metadata, isolating uncertainty from inference, and tracking findings with a rigorous provenance ledger.

## 🎛️ Product Identity & Mission
* **Release Phase**: Alpha.1 — Project Understanding
* **Engineering State**: SPECIFICATION → ARCHITECTURE
* **Author**: Vera Lynn DeGraw (<veralynndegraw10011@proton.me>)
* **Repository Link**: [VeraLynnDeGraw/CODEWEAVER](https://github.com)
* **Operational Control**: The human developer remains the final authority over architecture, implementation choices, testing, and production deployments.

## ⚡ Key Architectural Properties
* **Deterministic Execution**: Given the same project tree inputs, it will always guarantee identical execution outputs and internal sorting.
* **Pure Read-Only**: Zero code generation, side-effects, module installations, or external cloud requests. Runs at **\$0 infrastructure overhead**.
* **Ambiguity Preservation**: Retains competing findings (e.g., hybrid environments running both Python and Node.js manifests) without dropping competing tracks to force a false certainty.

## 📋 Found Knowledge States
Every discovery entry contains an explicit state classification:
* `OBSERVED`: Evidence directly present and read from files.
* `INFERRED`: Logic-deduced deductions spanning multiple observed facts.
* `PROPOSED`: Action candidates and configuration targets optimized for human review.
* `UNKNOWN`: Missing baseline indicators.

## 🔧 Installation & Build Manual

### 1. Build Standalone Binary Locally
Compile CODEWEAVER down to a single self-contained executable file inside your Kitty terminal environment:
```bash
pip install -r requirements.txt
pyinstaller --onefile src/main.py --name codeweaver
```

### 2. General Usage
Point the compiled binary at any project directory target:
```bash
./dist/codeweaver /path/to/target/project
```

### 🤖 3. Machine Integration Layer (External AI Agents)
Other local AI processes (such as IDE pipelines, Cursor scripts, or automated tools) can call the tool seamlessly. It automatically down-samples output to clean machine-readable data when a piping signal or explicit parameter is used:
```bash
./dist/codeweaver . --json
```
