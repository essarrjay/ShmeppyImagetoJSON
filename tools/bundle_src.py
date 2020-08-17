import tarfile
from pathlib import Path

ersion = "2.2.1"
BASE_DIR = Path(__file__).parent.parent
out_path = BASE_DIR.joinpath('build', f'img_to_json_python_bundle_v{ersion}.tar')
in_path = BASE_DIR.joinpath('src')

print(f'Base Dir: {BASE_DIR}')
print(f'Out_path: {out_path}')
print(f'In_path: {in_path}')

with tarfile.open(out_path, "w") as tar:
    tar.add(Path("../README.md"))
    for f in in_path.iterdir():
        if f.is_file(): tar.add(f)
