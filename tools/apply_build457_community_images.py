"""Build457: show a useful fallback instead of an unbounded spinner
on community avatars while preserving the existing image provider and uploads.
Run only after all older community patch steps.
"""
from pathlib import Path

SOURCE=Path("app/lib/community450.dart")

OLD="""          fit: BoxFit.cover,
          errorWidget: (_, __, ___) => SizedBox(
            width: size,
            height: size,
            child: const Icon(Icons.groups_rounded, color: mor),
          ),"""

NEW="""          fit: BoxFit.cover,
          // Image URLs may take time to retry: don't show an eternal spinner.
          placeholder: SizedBox(
            width: size,
            height: size,
            child: const ColoredBox(
              color: Color(0xFFF0E8FF),
              child: Center(child: Icon(Icons.groups_rounded, color: mor)),
            ),
          ),
          retryErrorBuilder: (context, error, retry) => SizedBox(
            width: size,
            height: size,
            child: Material(
              color: const Color(0xFFF0E8FF),
              child: InkWell(
                onTap: retry,
                child: const Center(
                  child: Icon(Icons.refresh_rounded, color: mor),
                ),
              ),
            ),
          ),"""

def transform(source):
    if "retryErrorBuilder: (context, error, retry)" in source:
        return source
    count=source.count(OLD)
    if count!=1:
        raise ValueError(f"Community avatar anchor mismatch: {count} occurrences")
    return source.replace(OLD,NEW,1)

def main():
    before=SOURCE.read_text()
    after=transform(before)
    if before!=after:
        SOURCE.write_text(after)
    print("Build457: bounded-feeling community avatar placeholder and manual retry")

if __name__=="__main__":
    main()
