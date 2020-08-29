import tarfile
from pathlib import Path
import markdown
from os import remove

ERSION = input("Version Number: ")
BASE_DIR = Path(__file__).resolve().parent.parent
OUT_PATH = BASE_DIR.joinpath('build', f'shmeppytools_python_bundle_v{ERSION}.tar')
IN_PATH = BASE_DIR.joinpath('shmeppytools')
EXCLUDE_LIST = ['__pycache__']
README_LIST = ['imageconverter', 'maptools', 'simple_scripts']

print(f'BASE_DIR: {BASE_DIR}')
print(f'OUT_PATH: {OUT_PATH}')
print(f'IN_PATH: {IN_PATH}')


def exclude_and_reset(tarinfo):
    """excludes files from tarinfo and resets ID info"""
    fpath = Path(tarinfo.name)

    # Exclude EXCLUDE_LIST
    if fpath.name in EXCLUDE_LIST:
        print(f" tarfile filter: EXCLUDING EXCLUDE_LIST File: {fpath}")
        return None

    # Exclude markdown files
    elif Path(tarinfo.name).suffix == '.md':
        print(f" tarfile filter: EXCLUDING MARKDOWN File: {fpath}")
        return None

    else:
        print(f" tarfile filter: INCLUDING File: {fpath}")
        tarinfo.uid = tarinfo.gid = 0
        tarinfo.uname = tarinfo.gname = ""
        return tarinfo


def md_to_html_file(p):
    """pathlib.Path markdown file to html file"""
    with open(p, "r", encoding="utf-8") as input_file:
        text = input_file.read()
    html = markdown.markdown(text)

    out_path = p.resolve().parent.joinpath(p.stem + ".html")
    print(f" md_to_html: SAVING .md as .html: {out_path}")
    with open(out_path, "w", encoding="utf-8", errors="xmlcharrefreplace") as out_file:
        out_file.write(html)

    return out_path


def main():
    """Bundles files needed to run app in Python"""
    with tarfile.open(OUT_PATH, "w") as tar:
        # add project readme (left separate for flexibilty in packaging)
        readme_html = md_to_html_file((IN_PATH.parent / "README.md"))
        tar.add(readme_html, arcname=readme_html.name)
        remove(readme_html)

        # add shmeppytools readme (left separate for flexibilty)
        readme_html = md_to_html_file((IN_PATH.parent / "README.md"))
        tar.add(readme_html, arcname=f"{IN_PATH.stem}/{readme_html.name}")
        remove(readme_html)

        # convert README.md to .html and add
        for pkg in README_LIST:
            readme_path = (IN_PATH / pkg / "README.md")
            readme_html = md_to_html_file(readme_path)
            print(f'Attempting to add file as: {readme_html}\n')
            arcname = f"{IN_PATH.stem}/{pkg}/{pkg}_README.html"
            tar.add(readme_html, arcname=arcname)
            remove(readme_html)

        # convert /docs/* to .html and add
        for f in (BASE_DIR / 'docs').iterdir():
            doc_html = md_to_html_file(f)
            tar.add(doc_html, arcname=Path(*doc_html.parts[-2:]))
            remove(doc_html)

        # add source files, exclude __pycache__
        for f in IN_PATH.iterdir():
            print(f'\nCurrent File: {"/".join(f.parts[-3:])}')
            fin = Path(*f.parts[-2:])
            print(f'Attempting to archive file as: {fin}')
            tar.add(f, arcname=fin, recursive="True", filter=exclude_and_reset)
    return print(f'\nFiles bundled to: {OUT_PATH}\n')


if __name__ == '__main__':
    main()
