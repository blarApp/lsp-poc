import os
from typing import List
from .Folder import Folder
from .File import File


class ProjectFilesIterator:
    def __init__(
        self,
        root_path: str,
        paths_to_skip: List[str] = None,
        names_to_skip: List[str] = None,
        blarignore_path: str = None,
    ):
        self.paths_to_skip = paths_to_skip or []
        self.root_path = root_path
        self.names_to_skip = names_to_skip or []

        if blarignore_path:
            self.names_to_skip.extend(self.get_ignore_files(blarignore_path))

    def get_ignore_files(self, gitignore_path: str) -> List[str]:
        with open(gitignore_path, "r") as f:
            return [line.strip() for line in f.readlines()]

    def __iter__(self):
        for root, dirs, files in os.walk(self.root_path, topdown=True):
            dirs[:] = self._get_filtered_dirs(root, dirs)
            files = self._get_filtered_files(root, files)

            folders = self.empty_folders_from_dirs(root, dirs)

            if not self._should_skip(root):
                yield Folder(
                    root,
                    files,
                    folders,
                )

    def _get_filtered_dirs(self, root: str, dirs: List[str]) -> List[Folder]:
        dirs = [dir for dir in dirs if not self._should_skip(os.path.join(root, dir))]
        return dirs

    def _get_filtered_files(self, root: str, files: List[str]) -> List[File]:
        files = [
            file for file in files if not self._should_skip(os.path.join(root, file))
        ]

        return [File(name=file, root_path=root) for file in files]

    def _should_skip(self, path: str) -> bool:
        is_basename_in_names_to_skip = os.path.basename(path) in self.names_to_skip

        is_path_in_paths_to_skip = any(
            path.startswith(path_to_skip) for path_to_skip in self.paths_to_skip
        )

        return is_basename_in_names_to_skip or is_path_in_paths_to_skip

    def empty_folders_from_dirs(self, root: str, dirs: List[str]) -> List[Folder]:
        return [Folder(os.path.join(root, dir), [], []) for dir in dirs]


if __name__ == "__main__":
    for folder in ProjectFilesIterator(
        "/home/juan/devel/blar/lsp-poc/",
        paths_to_skip=[
            "/home/juan/devel/blar/lsp-poc/__pycache__",
            "/home/juan/devel/blar/lsp-poc/.git",
            "/home/juan/devel/blar/lsp-poc/.venv",
            "/home/juan/devel/blar/lsp-poc/Graph/__pycache__",
            "/home/juan/devel/blar/lsp-poc/Graph/Node/__pycache__",
            "/home/juan/devel/blar/lsp-poc/Graph/Relationship/__pycache__",
            "/home/juan/devel/blar/lsp-poc/LSP/__pycache__",
        ],
    ):
        print(folder)
