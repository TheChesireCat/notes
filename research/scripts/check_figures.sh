#!/usr/bin/env bash
# Option (c) drift check, no Python needed: every committed SVG that carries a
# provenance stamp (dc:source + dc:identifier "sha256:...") must match the current
# sha256 of the script named in it. Run from the repo root; exits 1 on a stale figure.
set -euo pipefail
status=0
for svg in $(git ls-files '*.svg'); do
  src=$(sed -n 's:.*<dc\:source>\(.*\)</dc\:source>.*:\1:p' "$svg" | head -1)
  want=$(sed -n 's:.*<dc\:identifier>sha256\:\([0-9a-f]*\)</dc\:identifier>.*:\1:p' "$svg" | head -1)
  [ -z "$src" ] && continue
  if [ ! -f "$src" ]; then
    echo "STALE $svg: source $src is missing"; status=1; continue
  fi
  have=$(shasum -a 256 "$src" | cut -d' ' -f1)
  if [ "$have" != "$want" ]; then
    echo "STALE $svg: $src changed since the figure was made; rerun it"; status=1
  else
    echo "ok    $svg <- $src"
  fi
done
exit $status
