"""Check report structure and source locations; preserve measurable evidence."""

import collections
import json
from pathlib import Path
import sys
from urllib.parse import unquote

root = Path.cwd().resolve()
report = json.loads(Path("bandit-report.sarif").read_text())
assert report["version"] == "2.1.0", "Unexpected SARIF version"
assert report["runs"], "No SARIF runs"
counts = collections.Counter()
rules = collections.Counter()
locations = 0
snippets = 0
for run in report["runs"]:
    driver = run["tool"]["driver"]
    assert driver["name"].lower() == "bandit", driver
    assert driver["version"] == "1.9.4", driver
    for result in run.get("results", []):
        counts[result.get("level", "warning")] += 1
        rules[result["ruleId"]] += 1
        for location in result.get("locations", []):
            physical = location["physicalLocation"]
            uri = unquote(physical["artifactLocation"]["uri"])
            path = (root / uri).resolve()
            assert path.is_relative_to(root) and path.is_file(), uri
            assert ".private-actions" not in path.parts, uri
            lines = path.read_text().splitlines()
            region = physical.get("region", {})
            line = region.get("startLine")
            assert isinstance(line, int) and 1 <= line <= len(lines), (uri, line)
            locations += 1
            if region.get("snippet", {}).get("text"):
                snippets += 1

summary = {
    "phase": sys.argv[1],
    "tool": "bandit",
    "version": "1.9.4",
    "results": sum(counts.values()),
    "levels": dict(counts),
    "rules": dict(sorted(rules.items())),
    "valid_source_locations": locations,
    "locations_with_snippet": snippets,
    "schema_validation": "basic structure only; not full JSON Schema",
}
if sys.argv[1] == "after":
    before = json.loads(Path("bandit-evidence/summary-before.json").read_text())
    for field in ("results", "levels", "rules", "valid_source_locations"):
        assert summary[field] == before[field], f"Uploader changed {field}"
Path(f"bandit-evidence/summary-{sys.argv[1]}.json").write_text(
    json.dumps(summary, indent=2) + "\n"
)
print(json.dumps(summary, indent=2))
