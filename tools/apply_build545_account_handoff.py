"""Account handoff detaches old media without interpreting it as hangup.
Apply after Build544; explicit hangup and committed terminal-room policy stay intact.
"""
from pathlib import Path
MARK = '// Build545 account handoff preserves the remote invitation'

def transform(source):
    if MARK in source:
        return source
    old = 'if(entry.value.uid==uid)await ngelx445EndBackground(entry.key);'
    assert source.count(old) == 1
    source = source.replace(old, 'if(entry.value.uid==uid)await ngelxArkaPlanAramayiTemizle(entry.key);', 1)
    source = source.replace("    // Finish the old identity's server departure before replacing its token.\n    // A denied/offline departure keeps this account active for an explicit retry.",
        '    // Release old local media before replacing its token.\n    // Switching accounts does not reject or end the remote invitation.', 1)
    return source + '\n' + MARK + '\n'

if __name__ == '__main__':
    path = Path('app/lib/main.dart')
    path.write_text(transform(path.read_text()))
