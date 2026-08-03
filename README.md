# Huffman File Compressor

A Python application that compresses and decompresses files using the Huffman coding algorithm.
The project includes a graphical user interface built with Tkinter.

> `compress.py` is the application's entry point.

> **Note:** `tkinter` is part of Python's standard library, but on many Linux distributions it is packaged separately and may not be installed by default. If you encounter a `ModuleNotFoundError` when running the application, install the `python3-tk` package using your distribution's package manager.

## Features

- Compress files (separetly or in group) using Huffman coding
- Decompress previously compressed files
- Lossless data compression
- Simple GUI

## Behavior

- Output compressed files use `.huff` extension
- If no output directory specified, the directory of the first selected file is chosen
- In group compression, the name of the first file is selected as the output file name

## Limitations

- The application is currently not optimized for large files. Compression and decompression may become noticeably slower for files larger than a few megabytes.

## Compression Analysis

The effectiveness of Huffman coding depends entirely on the distribution of byte values in the input data. It compresses better when some bytes occur much more frequently than the others. So, files whose byte values are distributed more uniformly have little potential for compression, since most symbols (byte values in the input) require codes of similar length. In such cases, the compressed file may have little or no size reduction.

For very small files or files with low compressibility, the compressed output may even be larger in size. This is because the compressed file stores metadata that is required for decompression (e.g., the Huffman tree, file size, file name, padding size, etc), and might outweight the size reduction achieved by compression.

Overall, Huffman coding is particularly effective for text-based data, where character frequencies are naturally uneven, and for data that has already been compressed (e.g., ZIP, JPEG, PNG, MP3, or PDF files) or has high entropy, Huffman codinggit  provides little additional compression.
