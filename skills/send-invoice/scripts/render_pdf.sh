#!/usr/bin/env bash
# render_pdf.sh — stubbed PDF render step for the send-invoice Skill.
#
# Takes one positional arg: the path to an INV-NNNN.json file.
# In production, this would shell out to WeasyPrint / Prince / wkhtmltopdf;
# here it validates the JSON and prints the rendered path so the rest of
# the workflow runs cleanly end to end on stock macOS bash.

set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "usage: render_pdf.sh <path-to-invoice.json>" >&2
  exit 2
fi

json_path="$1"

if [[ ! -f "$json_path" ]]; then
  echo "error: invoice file not found: $json_path" >&2
  exit 1
fi

# Validate it's parseable JSON via stock python3.
if ! python3 -c "import json,sys; json.load(open(sys.argv[1]))" "$json_path" >/dev/null 2>&1; then
  echo "error: invoice file is not valid JSON: $json_path" >&2
  exit 1
fi

# Derive the PDF path next to the JSON.
pdf_path="${json_path%.json}.pdf"

# Stub: write a placeholder PDF marker so the file exists on disk.
# Real renderer plugs in here.
{
  echo "%PDF-1.4"
  echo "% send-invoice stub render"
  echo "% source: $json_path"
  echo "%%EOF"
} > "$pdf_path"

echo "Rendered $pdf_path"
