import os
import json
from dataclasses import dataclass, asdict
from typing import List

# --- TERM COLORS (FOR KITTY TERMINAL) ---
CLR_RESET   = "\033[0m"
CLR_BOLD    = "\033[1m"
CLR_DIM     = "\033[2m"
CLR_CYAN    = "\033[36m"
CLR_YELLOW  = "\033[33m"
CLR_GREEN   = "\033[32m"
CLR_RED     = "\033[31m"
CLR_MAGENTA = "\033[35m"

STATE_COLORS = {
    "OBSERVED": CLR_GREEN,
    "INFERRED": CLR_CYAN,
    "PROPOSED": CLR_YELLOW,
    "UNKNOWN":  CLR_DIM
}

@dataclass
class Finding:
    state: str       # OBSERVED, INFERRED, PROPOSED, UNKNOWN
    subject: str     # language_signal, project_type, layout, runtime_candidate, dependency, script
    value: str       
    source: str      
    confidence: str  # high, medium, low
    reason: str      

@dataclass
class ProjectContext:
    root_path: str
    files_discovered: List[str]
    dirs_discovered: List[str]
    findings: List[Finding]

# --- DETECTORS ---
class PythonDetector:
    @staticmethod
    def analyze(root_path: str, files: List[str], dirs: List[str]) -> List[Finding]:
        findings = []
        indicators = {
            "pyproject.toml": "declares project configuration and metadata",
            "requirements.txt": "lists project dependencies",
            "setup.py": "defines package distribution"
        }
        
        found_signals = [f for f in indicators if f in files]
        for filename in found_signals:
            findings.append(Finding(
                state="OBSERVED", subject="language_signal", value=filename,
                source=os.path.join(root_path, filename), confidence="high", reason=indicators[filename]
            ))
        
        if "requirements.txt" in files:
            req_path = os.path.join(root_path, "requirements.txt")
            try:
                with open(req_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#"):
                            findings.append(Finding(
                                state="OBSERVED", subject="dependency", value=line,
                                source=req_path, confidence="high", reason="Explicit package listed in dependencies file"
                            ))
            except Exception:
                pass
        
        if found_signals:
            findings.append(Finding(
                state="INFERRED", subject="project_type", value="Python",
                source="PythonDetector", confidence="high" if len(found_signals) > 1 else "medium",
                reason=f"Identified via presence of: {', '.join(found_signals)}"
            ))
            findings.append(Finding(
                state="PROPOSED", subject="runtime_candidate", value="python3 -m venv",
                source="PythonDetector", confidence="medium",
                reason="Standard virtual environment convention suggested for Python runtime management."
            ))
        return findings

class NodeDetector:
    @staticmethod
    def analyze(root_path: str, files: List[str], dirs: List[str]) -> List[Finding]:
        findings = []
        if "package.json" in files:
            pkg_path = os.path.join(root_path, "package.json")
            findings.append(Finding(
                state="OBSERVED", subject="language_signal", value="package.json",
                source=pkg_path, confidence="high",
                reason="contains Node.js project manifest and dependency trees"
            ))
            findings.append(Finding(
                state="INFERRED", subject="project_type", value="Node.js",
                source="NodeDetector", confidence="high",
                reason="package.json is directly present at the project root"
            ))
            
            try:
                with open(pkg_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if "scripts" in data and isinstance(data["scripts"], dict):
                        for script_name, cmd in data["scripts"].items():
                            findings.append(Finding(
                                state="OBSERVED", subject="script", value=f"npm run {script_name}",
                                source=pkg_path, confidence="high", reason=f"Configured script mapping to: `{cmd}`"
                            ))
                            if script_name in ["start", "dev", "test"]:
                                findings.append(Finding(
                                    state="PROPOSED", subject="runtime_candidate", value=f"npm run {script_name}",
                                    source="NodeDetector", confidence="high",
                                    reason=f"Explicit runtime script target found in package.json manifest."
                                ))
                    
                    for dep_type in ["dependencies", "devDependencies"]:
                        if dep_type in data and isinstance(data[dep_type], dict):
                            for pkg, ver in data[dep_type].items():
                                findings.append(Finding(
                                    state="OBSERVED", subject="dependency", value=f"{pkg} ({ver})",
                                    source=pkg_path, confidence="high", reason=f"Declared in project {dep_type}"
                                ))
            except Exception:
                pass
                
            if not any(f.subject == "script" for f in findings):
                findings.append(Finding(
                    state="PROPOSED", subject="runtime_candidate", value="npm start",
                    source="NodeDetector", confidence="medium",
                    reason="Standard entry point execution target suggested for Node platforms."
                ))
        return findings

class StructureDetector:
    @staticmethod
    def analyze(root_path: str, files: List[str], dirs: List[str]) -> List[Finding]:
        findings = []
        common_layouts = {
            "src": "Conventional source code subdirectory detected",
            "tests": "Conventional test suite directory detected",
            "dist": "Production compilation output/artifact layout detected",
            "build": "Build engine compilation artifact layout detected"
        }
        
        for dname in dirs:
            if dname in common_layouts:
                findings.append(Finding(
                    state="OBSERVED", subject="layout", value=f"{dname}/",
                    source=os.path.join(root_path, dname), confidence="high", reason=common_layouts[dname]
                ))
        return findings

# --- CORE ENGINE ---
class ProjectAnalyzer:
    def __init__(self, root_path: str):
        self.root_path = os.path.abspath(root_path)
        self.detectors = [PythonDetector, NodeDetector, StructureDetector]

    def scan_directory(self):
        try:
            items = os.listdir(self.root_path)
            files = sorted([f for f in items if os.path.isfile(os.path.join(self.root_path, f))])
            dirs = sorted([d for d in items if os.path.isdir(os.path.join(self.root_path, d))])
            return files, dirs
        except Exception:
            return [], []

    def analyze(self) -> ProjectContext:
        files, dirs = self.scan_directory()
        all_findings = []

        for detector in self.detectors:
            all_findings.extend(detector.analyze(self.root_path, files, dirs))

        if not any(f.subject == "project_type" for f in all_findings):
            all_findings.append(Finding(
                state="UNKNOWN", subject="project_type", value="None Match",
                source="ProjectAnalyzer", confidence="low",
                reason="No explicit project signals discovered."
            ))

        all_findings.sort(key=lambda x: (x.state, x.subject, x.value))
        return ProjectContext(root_path=self.root_path, files_discovered=files, dirs_discovered=dirs, findings=all_findings)

# --- RENDERING ENGINE ---
def render_ui(ctx: ProjectContext):
    print(f"\n{CLR_BOLD}{CLR_MAGENTA}🔮 CODEWEAVER // Alpha.1 — Project Understanding{CLR_RESET}")
    print(f"{CLR_DIM}────────────────────────────────────────────────────────────{CLR_RESET}")
    print(f"{CLR_BOLD}Target Root:{CLR_RESET} {ctx.root_path}")
    print(f"{CLR_BOLD}Discovered Files ({len(ctx.files_discovered)}):{CLR_RESET} {ctx.files_discovered}")
    print(f"{CLR_BOLD}Discovered Dirs  ({len(ctx.dirs_discovered)}):{CLR_RESET} {ctx.dirs_discovered}")
    print(f"{CLR_DIM}────────────────────────────────────────────────────────────{CLR_RESET}\n")

    print(f"{CLR_BOLD}🕵️  PROVENANCE LOG & FINDINGS:{CLR_RESET}\n")
    for f in ctx.findings:
        color = STATE_COLORS.get(f.state, CLR_RESET)
        print(f" ── [{color}{CLR_BOLD}{f.state:<8}{CLR_RESET}] {CLR_BOLD}{f.subject.upper()}{CLR_RESET} ──> {CLR_GREEN}'{f.value}'{CLR_RESET}")
        print(f"    {CLR_DIM}↳ Conf:{CLR_RESET} {f.confidence:<6} | {CLR_DIM}Source:{CLR_RESET} {os.path.basename(f.source)}")
        print(f"    {CLR_DIM}↳ Reason:{CLR_RESET} {f.reason}\n")
