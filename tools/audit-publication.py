# Copyright (c) 2026 Marco Pezzullo / Silicon LogiX. See LICENSE.
"""Check public distributions without displaying potentially confidential values."""
import argparse
import hashlib
import json
import re
import struct
import subprocess
import tarfile
import zipfile
from pathlib import Path

CODE = {'.py', '.ps1', '.cmd', '.h', '.hpp', '.toml', '.yml', '.yaml', '.rs', '.cpp', '.slint', '.fbt', '.sys'}
TEXT = CODE | {'.md', '.txt', '.json', '.xml', '.svg', '.xsd', '.cmake', '.license'}
SOURCE_ARCHIVES = {'open62541.zip', 'forte.zip', 'ua-nodeset.zip', 'dwrote-0.11.5.crate'}
PUBLIC_DOCS = ['architecture.md', 'custom-development.md', 'dependencies.md', 'opcua-learning.md',
               'opcua.md', 'operator-interface.md', 'physical-model.md', 'quick-start.md', 'validation.md']
PUBLIC_SCREENSHOTS = ['opcua-studio.png', 'overview.png', 'ua-node-detail.png', 'ua-watchlist.png',
                      'opcua-tour-quality.png', 'history-trends.png', 'test-plan.png', 'about.png']
PUBLIC_FILES = {'.gitignore', '.gitattributes', '.github/workflows/ci.yml', 'README.md', 'LICENSE',
                'NOTICE.txt', 'THIRD_PARTY_NOTICES.md', 'THIRD_PARTY_SOURCE.md', 'CONTRIBUTING.md',
                'SECURITY.md', 'CHANGELOG.md', 'START-HERE.txt', 'publication-manifest.json',
                'tools/audit-publication.py'} | {'docs/' + name for name in PUBLIC_DOCS} | {
                'assets/screenshots/' + name for name in PUBLIC_SCREENSHOTS}
NOTES = re.compile(r'\b(?:' + '|'.join(['TO' + 'DO', 'FIX' + 'ME', 'CO' + 'DEX' + '_HANDOFF', 'AGENTS' + r'\.md', 'Chat' + 'GPT', 'Code' + 'x']) + r')\b', re.I)
PERSONAL = re.compile(rb'(?i)[A-Z]:[\\/]+Users[\\/]+(?!Public[\\/]|Default[\\/])[^\x00\r\n\s"\x27\\/]+')
SECRETS = [
    re.compile(rb'-----BEGIN (?:[A-Z0-9]+ )?PRIVATE KEY-----'),
    re.compile(rb'\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{50,})\b'),
    re.compile(rb'\b(?:AKIA|ASIA)[A-Z0-9]{16}\b'),
    re.compile(rb'\b(?:sk-[A-Za-z0-9_-]{30,}|AIza[A-Za-z0-9_-]{30,}|xox[baprs]-[A-Za-z0-9-]{20,})\b'),
    re.compile(rb'(?i)\b[a-z][a-z0-9+.-]{0,20}://[a-z0-9._~%!$&()*+,;=-]{1,100}:[a-z0-9._~%!$&()*+,;=:-]{1,150}@'),
    re.compile(rb'(?im)(?:^|[,{\r\n])[\t ]*["\x27]?(?:password|passwd|api[_-]?key|access[_-]?token|client[_-]?secret|secret[_-]?key)["\x27]?[\t ]*[=:][\t ]*["\x27][^"\x27\r\n]+["\x27]'),
]


def require(condition, description):
    if not condition:
        raise AssertionError(description)


def check_credentials(data, relative, third_party=False):
    for index, pattern in enumerate(SECRETS):
        if third_party and index == len(SECRETS) - 1:
            continue
        require(not pattern.search(data), f'Credential pattern {index + 1}: {relative}')


def pe_symbols(data):
    require(data[:2] == b'MZ', 'Invalid Windows binary')
    offset = struct.unpack_from('<I', data, 60)[0]
    require(data[offset:offset + 4] == b'PE\0\0', 'Invalid PE header')
    return struct.unpack_from('<I', data, offset + 16)[0]


def original_notice(data):
    if b'SLX-UPSTREAM-NOTICE-HEADER v1' not in data[:100]:
        return data
    checksum = re.search(rb'Original-SHA256: ([a-f0-9]{64})', data[:1500])
    marker = re.search(rb'(?:# )?SLX-UPSTREAM-NOTICE-BODY\n(?:-->\n)?', data[:2000])
    require(checksum and marker, 'Invalid upstream notice provenance header')
    original = data[marker.end():]
    require(hashlib.sha256(original).hexdigest().encode() == checksum[1], 'Upstream notice text changed')
    return original


def archive_entries(path):
    if zipfile.is_zipfile(path):
        with zipfile.ZipFile(path) as archive:
            require(archive.testzip() is None, f'Dependency archive CRC: {path.name}')
            for entry in archive.infolist():
                if not entry.is_dir():
                    yield entry.filename, archive.read(entry)
    else:
        with tarfile.open(path, 'r:gz') as archive:
            for entry in archive:
                if entry.isfile():
                    yield entry.name, archive.extractfile(entry).read()


def audit(root, repository=False):
    manifest_path = root / 'publication-manifest.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8')) if manifest_path.is_file() else None
    if repository and not manifest:
        git_root = subprocess.run(['git', '-C', str(root), 'rev-parse', '--show-toplevel'], capture_output=True, text=True)
        require(git_root.returncode == 0 and Path(git_root.stdout.strip()).resolve() == root, 'Repository boundary')
        listed = subprocess.run(['git', '-C', str(root), 'ls-files', '-z', '--cached', '--others', '--exclude-standard'],
                                capture_output=True, check=True).stdout.decode().split('\0')
        paths = sorted(set(name for name in listed if name))
    else:
        paths = sorted(f.relative_to(root).as_posix() for f in root.rglob('*')
                       if f.is_file() and '.git' not in f.relative_to(root).parts)
    if not repository:
        require(manifest is not None, 'Missing publication inventory')
    if manifest:
        expected = {entry['path']: entry for entry in manifest['files']}
        require(set(paths) == set(expected) | {'publication-manifest.json'}, 'Publication inventory changed')
        for relative, entry in expected.items():
            data = (root / relative).read_bytes()
            require(len(data) == entry['bytes'] and hashlib.sha256(data).hexdigest() == entry['sha256'], f'File hash: {relative}')
    minimal_repository = bool(manifest and manifest['profile'] == 'github')
    if minimal_repository:
        require(set(paths) == PUBLIC_FILES, 'Public repository allowlist changed')
    headers = binaries = archives = 0
    for relative in paths:
        file = root / relative
        require(file.resolve().is_relative_to(root) and not file.is_symlink(), f'File boundary: {relative}')
        parts = Path(relative).parts
        require(not any(part in {'.git', 'private', 'workspace', 'target', '__pycache__'} for part in parts), f'Private path: {relative}')
        require(not relative.startswith(('src/', 'ui/', 'backend/', '.cargo/', 'tests/')), f'Implementation source: {relative}')
        require(not relative.startswith(('interfaces/', 'core/')), f'Excluded SDK material: {relative}')
        require(not NOTES.search(relative), f'Development document: {relative}')
        require(not re.search(r'(?i)(^|/)(?:\.env(?:\.[^/]*)?|id_rsa|id_ed25519|credentials)$|\.(?:pfx|p12|pem|key|keystore|blend)$', relative), f'Confidential file: {relative}')
        third_party = relative.startswith(('third_party/', 'licenses/'))
        suffix = file.suffix.lower()
        if relative.startswith('third_party/sources/'):
            require(file.name in SOURCE_ARCHIVES, f'Unapproved dependency archive: {relative}')
        if relative.startswith('licenses/'):
            require(suffix not in {'.rs', '.cpp', '.cc', '.c', '.h', '.hpp', '.slint', '.fbt', '.sys', '.py', '.ps1', '.cmd', '.exe', '.dll'},
                    f'Implementation stored with notices: {relative}')
        if not third_party:
            require(suffix not in {'.rs', '.cpp', '.cc', '.c', '.slint', '.fbt', '.sys'}, f'Proprietary source: {relative}')
            if suffix == '.py':
                require(relative == 'tools/audit-publication.py', f'Private tool: {relative}')
            if suffix == '.ps1':
                require(relative == 'scripts/start-gridpilot.ps1', f'Private script: {relative}')
        data = file.read_bytes()
        if relative.startswith('licenses/'):
            original_notice(data)
            require(re.search(rb'Copyright|SPDX-FileCopyrightText', b'\n'.join(data.splitlines()[:35]), re.I),
                    f'Missing license header: {relative}')
        require(len(data) < 100 * 1024 * 1024 or (manifest and manifest['profile'] != 'github'), f'GitHub file-size limit: {relative}')
        check_credentials(data, relative, third_party)
        if not third_party:
            require(not PERSONAL.search(data) and not PERSONAL.search(data.replace(b'\0', b'')), f'Personal build path: {relative}')
        if suffix in {'.exe', '.dll'}:
            require(pe_symbols(data) == 0, f'Unstripped symbols: {relative}')
            binaries += 1
        if suffix in TEXT or file.name in {'LICENSE', '.gitignore', '.gitattributes', 'CMakeLists.txt'}:
            text = data.decode('utf-8-sig')
            if not third_party:
                require(not NOTES.search(text), f'Development note: {relative}')
                header = re.search(r'Copyright|SPDX-FileCopyrightText', '\n'.join(text.splitlines()[:35]), re.I)
                sidecar = file.with_name(file.name + '.license')
                if not header and sidecar.is_file():
                    header = re.search(r'SPDX-FileCopyrightText:', sidecar.read_text(encoding='utf-8'), re.I)
                require(header, f'Missing copyright header: {relative}')
                headers += 1
        if relative.startswith('third_party/sources/') and suffix in {'.zip', '.crate'}:
            for name, content in archive_entries(file):
                require(not Path(name).is_absolute() and '..' not in Path(name).parts, f'Archive path: {relative}')
                check_credentials(content, relative + ':' + name, third_party=True)
            archives += 1
    if minimal_repository:
        require(b'<!-- Copyright' in (root / 'README.md').read_bytes(), 'README ownership notice')
        return dict(result='passed', version=manifest['version'], files=len(paths),
                    copyright_headers=headers, stripped_binaries=0, dependency_source_archives=0,
                    dependency_packages=0, verified_notice_sources=0,
                    proprietary_sources_included=False, personal_build_paths_found=False,
                    credential_patterns_found=False, development_notes_found=False,
                    sdk_interfaces_included=False, runtime_assets_included=False)
    provenance = json.loads((root / 'assets/config/source-provenance.json').read_text(encoding='utf-8'))
    require({entry['archive'] for entry in provenance['dependency_sources']} == SOURCE_ARCHIVES,
            'Missing dependency source provenance')
    for entry in provenance['dependency_sources']:
        archive = root / 'third_party/sources' / entry['archive']
        require(archive.is_file() and hashlib.sha256(archive.read_bytes()).hexdigest() == entry['sha256'],
                f'Dependency source checksum: {entry["archive"]}')
    inventory = json.loads((root / 'licenses/rust-dependencies.json').read_text(encoding='utf-8'))
    notice_hashes = {}
    notice_sources = set()
    for dependency in inventory['packages']:
        require(bool(dependency['notices']), 'Missing dependency attribution')
        for notice in dependency['notices']:
            require((root / notice).is_file(), f'Missing dependency notice: {notice}')
            if notice not in notice_hashes:
                notice_hashes[notice] = hashlib.sha256(original_notice((root / notice).read_bytes())).hexdigest()
        for source in dependency.get('notice_sources', []):
            require(source['sha256'] in {notice_hashes[path] for path in dependency['notices']},
                    'Dependency notice provenance checksum')
            notice_sources.add((source['url'], source['sha256']))
        if dependency.get('bundled_source'):
            require(hashlib.sha256((root / dependency['bundled_source']).read_bytes()).hexdigest() ==
                    dependency['source_sha256'], 'Bundled dependency source checksum')
    require((root / 'third_party/slint-renderer/upstream.json').is_file(), 'Missing renderer source provenance')
    version = json.loads((root / 'assets/config/distribution.json').read_text(encoding='utf-8'))['version']
    require(not manifest or manifest['version'] == version, 'Distribution version mismatch')
    return dict(result='passed', version=version,
                files=len(paths), copyright_headers=headers, stripped_binaries=binaries,
                dependency_source_archives=archives, dependency_packages=len(inventory['packages']),
                verified_notice_sources=len(notice_sources),
                proprietary_sources_included=False, personal_build_paths_found=False,
                credential_patterns_found=False, development_notes_found=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('directory')
    parser.add_argument('--repository', action='store_true')
    parser.add_argument('--report')
    args = parser.parse_args()
    report = audit(Path(args.directory).resolve(), args.repository)
    if args.report:
        Path(args.report).write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report))
