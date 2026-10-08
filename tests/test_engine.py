import os
import shutil
import tempfile
import pytest
from src.engine import ProjectAnalyzer

class TestCodeWeaverCore:
    @pytest.fixture(autouse=True)
    def setup_sandbox(self):
        """
        Scaffolds a deterministic temporary directory tree to mock 
        hybrid workspace structures before triggering detector engines.
        """
        self.test_dir = tempfile.mkdtemp()
        yield
        # Clean down transient storage environments following suite execution
        shutil.rmtree(self.test_dir)

    def test_deterministic_hybrid_detection(self):
        """
        Verifies that the engine safely handles ambiguous workspaces containing
        competing language signatures without dropping structural tracks.
        """
        # Scaffold a hybrid workspace matching your test_project state
        with open(os.path.join(self.test_dir, "package.json"), "w") as f:
            f.write('{"scripts": {"start": "node index.js"}}')
        with open(os.path.join(self.test_dir, "pyproject.toml"), "w") as f:
            f.write("# Mock Python config")
        os.makedirs(os.path.join(self.test_dir, "src"), exist_ok=True)

        # Run analysis pipeline
        analyzer = ProjectAnalyzer(self.test_dir)
        ctx = analyzer.analyze()

        # 1. Verify File Discovery Properties
        assert "package.json" in ctx.files_discovered
        assert "pyproject.toml" in ctx.files_discovered
        assert "src" in ctx.dirs_discovered

        # 2. Verify Ambiguity Preservation Rules
        project_types = [f.value for f in ctx.findings if f.subject == "project_type"]
        assert "Node.js" in project_types
        assert "Python" in project_types

        # 3. Verify Provenance Metadata Fields
        for finding in ctx.findings:
            assert finding.state in ["OBSERVED", "INFERRED", "PROPOSED", "UNKNOWN"]
            assert finding.confidence in ["high", "medium", "low"]
            assert finding.reason != ""

    def test_unknown_directory_fallback(self):
        """
        Verifies that an empty directory falls back gracefully to an UNKNOWN state
        instead of producing false certainties or throwing internal exceptions.
        """
        analyzer = ProjectAnalyzer(self.test_dir)
        ctx = analyzer.analyze()

        fallback_findings = [f for f in ctx.findings if f.state == "UNKNOWN"]
        assert len(fallback_findings) > 0
        assert fallback_findings[0].subject == "project_type"
        assert fallback_findings[0].value == "None Match"
