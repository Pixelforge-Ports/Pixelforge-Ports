"""Read game requirements from the README associated with a port release."""
import re


def game_requirements(readme):
    readme = readme.replace('\r\n', '\n')
    match = re.search(r'^## Get [^\n]+\n(.*?)(?=^## |\Z)', readme, re.M | re.S)
    instructions = match.group(1).strip() if match else ''
    version = re.search(r'supported build\s*\((\d+(?:\.\d+)+[a-zA-Z0-9.-]*)', instructions, re.I)
    if not version:
        version = re.search(r'Windows offline backup installer for version\s+(\d+(?:\.\d+)+[a-zA-Z0-9-]*)', instructions, re.I)
    android = bool(match and 'APK' in match.group(0).splitlines()[0])
    if android:
        version = re.search(r'This port requires\s+\*\*[^*]*?\s(\d+(?:\.\d+)+[a-zA-Z0-9-]*)\*\*', instructions)
    return {
        'windows_version': version.group(1) if version and not android else None,
        'game_version': version.group(1) if version else None,
        'platform': 'Android' if android else 'Windows',
        'instructions': instructions,
    }
