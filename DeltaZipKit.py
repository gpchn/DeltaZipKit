#!/usr/bin/env python
# coding: utf-8

from pathlib import Path
from typing import Any, List, Generator

# default config
CHUNK_SIZE = 1048576  # bytes = 1 MB
ZIP_COMPRESS_LEVEL = 9


class Compressor:
    def __init__(self, data) -> None:
        self.data = data

        results: List[bytes] = [self.zip.compress(), self.gzip.compress()]
        result = min(len(r) for r in results)
        return result

    class zip:
        def compress(self) -> bytes:
            from zlib import compress

            return compress(self.data, ZIP_COMPRESS_LEVEL)

        def decompress(self) -> bytes:
            from zlib import decompress

            return decompress(self.data)

    class gzip:
        def compress(self) -> bytes: ...
        def decompress(self) -> bytes: ...


class IO:
    class file:
        def __init__(self, file: Path) -> None:
            assert file.is_file()
            self.file: Path = file

        def rb(self) -> Generator[bytes, Any, None]:
            with self.file.open("rb") as f:
                while True:
                    chunk = f.read(CHUNK_SIZE)
                    if not chunk:
                        break
                    yield chunk

        def wb(self, data_generator: Generator):
            with self.file.open("wb") as file:
                file.write(data_generator)


def main() -> None:
    from argparse import ArgumentParser

    parser = ArgumentParser(
        description="DeltaZipKit [Version 0.1b]\nDeltaZipKit is an intelligent compression tool. It segments files and each segment is compressed using the algorithm with the highest compression rate, thereby achieving the ultimate compression rate for the final result.",
        epilog="",
    )
    parser.add_argument(
        "-i", "--input", type=Path, required=True, help="input file path"
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        required=False,
        default="out.dzk",
        help="output file path",
    )

    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument(
        "-c", "--compress", action="store_true", default=True, help="compress mode"
    )
    group.add_argument(
        "-d", "--decompress", action="store_true", help="decompress mode"
    )

    group2 = parser.add_argument_group()
    group2.add_argument(
        "--github-repo",
        action="store_true",
        help="get this program's github repository",
    )
    group2.add_argument("--")

    args = parser.parse_args()

    segments: bytes = IO.file(args.input).rb()
    for segment in segments:
        final_data = Compressor(segment)


if __name__ == "__main__":
    main()
