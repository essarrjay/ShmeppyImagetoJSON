import tarfile
from pathlib import Path
import markdown
from os import remove

ERSION = input("Version Number: ")
BASE_DIR = Path(__file__).resolve().parent.parent
out_path = BASE_DIR.joinpath('build', f'shmeppytools_python_bundle_v{ERSION}.tar')
in_path = BASE_DIR.joinpath('shmeppytools')

print(f'Base Dir: {BASE_DIR}')
print(f'Out_path: {out_path}')
print(f'In_path: {in_path}')

def reset(tarinfo):
    tarinfo.uid = tarinfo.gid = 0
    tarinfo.uname = tarinfo.gname = ""
    return tarinfo

def md_to_html_file(p):
    """pathlib.Path markdown file to html file"""
    with open(p, "r", encoding="utf-8") as input_file:
        text = input_file.read()
    html = markdown.markdown(text)

    out_path = p.resolve().parent.joinpath(p.stem + ".html")

    with open(out_path, "w", encoding="utf-8", errors="xmlcharrefreplace") as out_file:
        out_file.write(html)

    return out_path

def main():
    """Bundles files needed to run app in Python"""
    readme_html = md_to_html_file(BASE_DIR.joinpath("README.md"))

    with tarfile.open(out_path, "w") as tar:
        tar.add(readme_html,arcname=readme_html.name)
        for f in in_path.iterdir():
            print(f'Checking File: {"/".join(f.parts[-3:])}')
            if not f.is_dir():
                fin = Path(*f.parts[-2:])
                print(f'Adding file as: {fin}\n')
                tar.add(f, arcname=fin, recursive="False", filter=reset)
            else:
                print("Directory excluded.\n")
    remove(readme_html)
    return print(f'Files bundled to: {out_path}')

if __name__ == '__main__':
    main()
