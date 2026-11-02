import shutil
import unittest
from pathlib import Path
from typing import Optional, Tuple


class Entry:
    """Represents a generic item in a storage hierarchy."""

    def __init__(self, name: str, parent: Optional["Entry"] = None) -> None:
        """Create a storage entry with a name and optional parent entry.

        Args:
            name: The name of the entry.
            parent: The parent entry containing this entry, if any.
        """
        self.name: str = name
        self._parent: Optional["Entry"] = parent

    def parent(self) -> Optional["Entry"]:
        """Return the parent entry for this item.

        Returns:
            The parent entry, or None if this entry has no parent.
        """
        return self._parent

    def size(self) -> int:
        """Return the storage size used by this entry in bytes.

        Returns:
            The number of bytes used by this entry. Base entries use 0 bytes.
        """
        return 0

    def absolute_path(self) -> list["Entry"]:
        """Return the path from this entry up to the root entry.

        The returned list starts with the current entry and then moves upward
        through each parent until the highest-level root is reached.

        Returns:
            A list of entry objects representing the full ancestor path.
        """
        if self._parent is None:
            return [self]
        return [self] + self._parent.absolute_path()


class File(Entry):
    """Represents a file with a specific number of bytes used."""

    def __init__(self, name: str, bytes_used: int, parent: Optional["Entry"] = None) -> None:
        """Create a file entry with a validated non-negative byte count.

        Args:
            name: The name of the file.
            bytes_used: The number of bytes used by the file.
            parent: The parent entry containing this file, if any.

        Raises:
            ValueError: If bytes_used is negative.
        """
        super().__init__(name, parent)
        if bytes_used < 0:
            raise ValueError("bytes_used cannot be negative.")
        self.bytes_used: int = bytes_used

    def size(self) -> int:
        """Return the number of bytes used by this file.

        Returns:
            The file's byte size.
        """
        return self.bytes_used


class Folder(Entry):
    """Represents a folder that can contain other entries as children."""

    def __init__(self, name: str, parent: Optional["Entry"] = None) -> None:
        """Create a folder entry with an empty list of child entries.

        Args:
            name: The name of the folder.
            parent: The parent entry containing this folder, if any.
        """
        super().__init__(name, parent)
        self._children: list[Entry] = []

    def add(self, entry: Entry) -> None:
        """Add a child entry to the folder.

        Args:
            entry: The entry to add as a child of this folder.
        """
        self._children.append(entry)
        entry._parent = self

    def children(self) -> Tuple[Entry, ...]:
        """Return all child entries in this folder as a tuple.

        Returns:
            A tuple containing every child entry stored in the folder.
        """
        return tuple(self._children)

    def size(self) -> int:
        """Return the total storage size used by this folder and all descendants.

        Returns:
            The sum of all sizes for every child entry, including nested folders.
        """
        return sum(child.size() for child in self._children)


def find_large_files(entry: Entry, minimum_size: int) -> list[File]:
    """Return all file entries whose size is at least the minimum threshold.

    If the provided entry is a file, the file is compared against the threshold and
    returned only if it meets or exceeds the minimum. If the provided entry is a
    folder, all nested files are searched recursively and matching files are returned.

    Args:
        entry: The starting entry to inspect.
        minimum_size: The minimum number of bytes a file must use to qualify.

    Returns:
        A list of File objects that meet or exceed the minimum size threshold.

    Raises:
        ValueError: If minimum_size is negative.
    """
    if minimum_size < 0:
        raise ValueError("minimum_size cannot be negative.")

    if isinstance(entry, File):
        return [entry] if entry.size() >= minimum_size else []

    if isinstance(entry, Folder):
        matches: list[File] = []
        for child in entry.children():
            matches.extend(find_large_files(child, minimum_size))
        return matches

    return []


class TestStorageHierarchy(unittest.TestCase):
    """Unit tests for the storage hierarchy behavior."""

    def test_absolute_path_from_file(self) -> None:
        """Verify that a file path is reported from the file up to the root."""
        root = Folder("root")
        subfolder = Folder("subfolder", parent=root)
        file_entry = File("notes.txt", 128, parent=subfolder)

        path = file_entry.absolute_path()
        self.assertEqual([entry.name for entry in path], ["notes.txt", "subfolder", "root"])

    def test_absolute_path_from_folder(self) -> None:
        """Verify that a folder path correctly includes its full ancestor chain."""
        root = Folder("root")
        subfolder = Folder("subfolder", parent=root)
        nested = Folder("nested", parent=subfolder)

        path = nested.absolute_path()
        self.assertEqual([entry.name for entry in path], ["nested", "subfolder", "root"])

    def test_find_large_files_from_folder(self) -> None:
        """Verify that large files are found recursively from a folder."""
        root = Folder("root")
        file1 = File("small.txt", 10)
        file2 = File("large.txt", 200)
        subfolder = Folder("subfolder")
        file3 = File("medium.txt", 75)

        root.add(file1)
        root.add(file2)
        root.add(subfolder)
        subfolder.add(file3)

        matches = find_large_files(root, 75)
        self.assertEqual([file.name for file in matches], ["large.txt", "medium.txt"])

    def test_find_large_files_from_single_file(self) -> None:
        """Verify that a single file is checked against the minimum size threshold."""
        file_entry = File("single.txt", 30)

        self.assertEqual(find_large_files(file_entry, 30), [file_entry])
        self.assertEqual(find_large_files(file_entry, 31), [])

    def test_find_large_files_rejects_negative_minimum(self) -> None:
        """Verify that a negative minimum size raises a ValueError."""
        with self.assertRaises(ValueError):
            find_large_files(Folder("root"), -1)


def build_demo_storage_system() -> tuple[Folder, Path, dict[str, int], File]:
    """Create a demo directory tree and mirror it with the Folder/File hierarchy.

    Returns:
        A tuple containing the outer folder, the demo directory path, the file-size
        mapping, and the deepest file entry used for the absolute_path showcase.
    """
    base_dir = Path(__file__).resolve().parent / "storage_demo"
    if base_dir.exists():
        shutil.rmtree(base_dir)

    level1_dir = base_dir / "level1"
    level2_dir = level1_dir / "level2"
    level3_dir = level2_dir / "level3"
    for directory in (level1_dir, level2_dir, level3_dir):
        directory.mkdir(parents=True)

    file_contents = {
        level1_dir / "top.txt": "12345",
        level2_dir / "mid.txt": "abcdefghij",
        level3_dir / "final.txt": "hello world!",
        level3_dir / "extra.txt": "this is a test",
    }

    for file_path, content in file_contents.items():
        file_path.write_text(content, encoding="utf-8")

    outer = Folder("storage_demo")
    level1_folder = Folder("level1", outer)
    level2_folder = Folder("level2", level1_folder)
    level3_folder = Folder("level3", level2_folder)
    outer.add(level1_folder)
    level1_folder.add(level2_folder)
    level2_folder.add(level3_folder)

    file_sizes = {
        "top.txt": (level1_dir / "top.txt").stat().st_size,
        "mid.txt": (level2_dir / "mid.txt").stat().st_size,
        "final.txt": (level3_dir / "final.txt").stat().st_size,
        "extra.txt": (level3_dir / "extra.txt").stat().st_size,
    }

    top_file = File("top.txt", file_sizes["top.txt"], level1_folder)
    middle_file = File("mid.txt", file_sizes["mid.txt"], level2_folder)
    final_file = File("final.txt", file_sizes["final.txt"], level3_folder)
    extra_file = File("extra.txt", file_sizes["extra.txt"], level3_folder)

    level1_folder.add(top_file)
    level2_folder.add(middle_file)
    level3_folder.add(final_file)
    level3_folder.add(extra_file)

    return outer, base_dir, file_sizes, final_file


class PassFailTestResult(unittest.TextTestResult):
    """Custom result runner that prints each test as PASS or FAIL."""

    def startTest(self, test: unittest.TestCase) -> None:
        """Print the test start and then run it."""
        print(f"\nRUNNING TEST: {test._testMethodName}")
        super().startTest(test)

    def addSuccess(self, test: unittest.TestCase) -> None:
        """Print PASS for a passing test."""
        print(f"RESULT: {test._testMethodName} -> PASS")
        super().addSuccess(test)

    def addFailure(self, test: unittest.TestCase, err) -> None:
        """Print FAIL for a failing test."""
        print(f"RESULT: {test._testMethodName} -> FAIL")
        print(f"Failure details: {err[1]}")
        super().addFailure(test, err)

    def addError(self, test: unittest.TestCase, err) -> None:
        """Print ERROR for a test that raised an exception."""
        print(f"RESULT: {test._testMethodName} -> ERROR")
        print(f"Error details: {err[1]}")
        super().addError(test, err)


class PassFailTextTestRunner(unittest.TextTestRunner):
    """Use the custom result class for clear per-test PASS/FAIL output."""

    resultclass = PassFailTestResult


if __name__ == "__main__":
    print("Running unit tests...")
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestStorageHierarchy)
    runner = PassFailTextTestRunner(verbosity=2)
    test_result = runner.run(suite)
    print(f"OVERALL UNIT TEST RESULT: {'PASS' if test_result.wasSuccessful() else 'FAIL'}")

    outer, demo_path, file_sizes, final_file = build_demo_storage_system()

    print("\nDemo storage folder:", demo_path)
    print("Outer folder size using size():", outer.size())
    print("Actual total file size on disk:", sum(file_sizes.values()))

    final_path = final_file.absolute_path()
    level2_folder = final_file.parent().parent()
    level2_path = level2_folder.absolute_path()

    print("Absolute path showcase:")
    print("  final.txt path:", " -> ".join(entry.name for entry in final_path))
    print("  level2 folder path:", " -> ".join(entry.name for entry in level2_path))

    threshold_1 = 5
    threshold_2 = 13
    large_files_threshold_1 = find_large_files(outer, threshold_1)
    large_files_threshold_2 = find_large_files(outer, threshold_2)

    print(f"find_large_files with minimum size {threshold_1}: {[file.name for file in large_files_threshold_1]}")
    print(f"find_large_files with minimum size {threshold_2}: {[file.name for file in large_files_threshold_2]}")
    
print("Louis Betensky, Z-Number: Z23542578")
