#!/usr/bin/env bash
cd "$(cd -P -- "$(dirname -- "$0")" && pwd -P)" || exit
cd ..

# Matches the Version incremented 'x.x.x' => 'x.x.x' automated release string from release.py
regex_version='[^0-9]+([0-9]+)\.([0-9]+)\.([0-9]+)[^0-9]+([0-9]+)\.([0-9]+)\.([0-9]+)'
repo_url="$(git config --get remote.origin.url)"

echo "# Changelog"
echo ""
echo "Generated on $(date)."
echo ""
echo "## [Unreleased](${repo_url})"
echo ""

# Format of the git log command
fmt="%s ([%h](${repo_url}/commit/%H))"

git log --oneline --decorate --color --pretty="$fmt" --color | while read -r line; do
  if [[ $line =~ $regex_version ]]; then
    version_str="${BASH_REMATCH[4]}.${BASH_REMATCH[5]}.${BASH_REMATCH[6]}"
    echo ""
    echo "## [$version_str](${repo_url}/releases/tag/$version_str)"
    echo ""
  fi
  echo "- ${line}"
done