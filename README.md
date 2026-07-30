# Huffman File Compressor

A Python application that compresses and decompresses files using the Huffman coding algorithm. 
The project includes a graphical user interface built with Tkinter. 

> **Note:** `tkinter` is part of Python's standard library, but on many Linux distributions it is packaged separately and may not be installed by default. If you encounter a `ModuleNotFoundError` when running the application, install the `python3-tk` package using your distribution's package manager.

> `compress.py` is the application's entry point.

## Features

* Compress files (separetly or in group) using Huffman coding and outputs the compressed file in `.huff` extension
* Decompress previously compressed files
* Simple graphical user interface
* Lossless data compression

## Compression Analysis

The effectiveness of Huffman coding depends entirely on the distribution of byte values in the input data. It performs best when some bytes occur much more frequently than others, allowing shorter binary codes to be assigned to common symbols and longer codes to less frequent ones.

Files whose byte values are distributed more uniformly provide little opportunity for compression, since most symbols require codes of similar length. In such cases, the compressed file may show little or no size reduction.

For very small files, the compressed output may even be larger than the original. This is because the compressed file must also store metadata, such as the Huffman tree required for decompression. The metadata overhead can outweigh any savings achieved by compression.

Overall, Huffman coding is particularly effective for text-based data, where character frequencies are naturally uneven. For data that has already been compressed (such as ZIP, JPEG, PNG, or MP3 files) or has high entropy, Huffman coding typically provides little additional compression.
