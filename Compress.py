import os
import pickle
import struct
from collections import Counter
import tkinter as tk
from tkinter import filedialog, messagebox
from HuffmanTree import huffmanCode, huffmanDecode

inputFiles = []
tkFileLabels = []
folderPath = None # Specified directory for storing output file

class CostumeFile:
    def __init__(self, path= ''):
        self.path = path
        self.name =  os.path.basename(path)
        self.encodedName = self.name.encode('utf-8')
    
        # These veriables holds the specified values for file name and file data
        self.d_padding = None
        self.n_padding = None
        self.compressedData = None #String
        self.compressedName = None #String
        self.byteCompressedData = None # byte array
        self.byteCompressedName = None # byte array

    def readBinaryData(self):
        if self.path:

            with open(self.path, 'rb') as file:
                binaryData = file.read() #returns a bytes object

            return binaryData
        
    def fileExtentsion(self):
        _, extension = os.path.splitext(self.path)
        return extension

def uploadFile():

    # Get file or files path
    filePaths = filedialog.askopenfilenames()

    if filePaths:
        # Create file objects and display a list of the file on the window
        for fpath in filePaths:
            f = CostumeFile(path= fpath)
            inputFiles.append(f)
            fpathlable = tk.Label(root, text= f.name, fg="blue")
            fpathlable.pack()
            tkFileLabels.append(fpathlable)

        # Set the defualt directory in case if user didn't select one
        defaultDirectory()

def outputFileName():
    outputName, _ = os.path.splitext(inputFiles[0].name)
    return outputName

def defaultDirectory():
    global folderPath
    folderPath =  os.path.dirname(inputFiles[0].path)

# This function asks user a directory to save the compreseed/decompressed file
def askOutputDirectory():
    global folderPath
    folderPath = filedialog.askdirectory()

def clearProgramInputs():
    global inputFiles, tkFileLabels
    inputFiles = []

    for label in tkFileLabels:
        label.destroy()

    tkFileLabels = []

def showNoInputMessage():
    messagebox.showwarning("No Input File", "Please upload your files for exceution.")

def showEmptyfileMessagae():
    messagebox.showwarning("Empty file", "Your given file(s) is(are) empty.")

def showNotDecompressable():
    messagebox.showwarning("Unsupported file", "Your given file for decopmression is not in .hff format.")

def countFrequencies():
    frequencies = Counter()

    for f in inputFiles:
        frequencies.update(f.encodedName)
        frequencies.update(f.readBinaryData())

    return frequencies

def compress_data(codeBook, binaryData):
    return ''.join(codeBook[byte] for byte in binaryData)

def add_padding(data):
    if (padding := 8 - len(data) % 8) < 8:
        data = data + "0" * padding
    else:
        padding = 0
    return (data, padding)

def create_byte_data(data):
    byte_data = bytearray()
    for i in range(0, len(data), 8):
        byte = data[i:i+8]
        byte_data.append(int(byte, 2))

    return byte_data

def compress():
    # inform user if there were no input paths given by user
    if not inputFiles:
        showNoInputMessage()
        return
    
    frequncies = countFrequencies()
    
    # inform user if input files are empty
    if not frequncies : 
        showEmptyfileMessagae()
        return
    
    codeBook, huffmanTree = huffmanCode(frequncies)
    print('codebook:')
    print(codeBook)

    for f in inputFiles:
        assert isinstance(f, CostumeFile)
        # generate compressed data using Huffman codes
        compressedData = compress_data(codeBook, f.readBinaryData())
        compressedName = compress_data(codeBook, f.encodedName)

        # If compressed data is not divisible by 8, add padding to the end of the content
        compressedData, f.d_padding  = add_padding(compressedData)
        compressedName, f.n_padding = add_padding(compressedName)

        # Convert each 8-bit chunk into a byte and append it to the corresponding bytearray
        f.byteCompressedData = create_byte_data(compressedData)
        f.byteCompressedName = create_byte_data(compressedName)

    outputFilePath = createCompressedFile(huffmanTree)

    includedFiles = '\n'.join(f"{f.name}" for f in inputFiles)
    messagebox.showinfo("Succees", f"File compressed and saved successfully!\nPath: {outputFilePath} \nCompressed files:\n {includedFiles}")

    clearProgramInputs()

def createCompressedFile(huffmanTree):

    # Serialize huffman tree using pickle library
    serialized_tree = pickle.dumps(huffmanTree)

    outputFilePath = os.path.join(folderPath, outputFileName()+'.huff')

    with open(outputFilePath, 'wb') as file:

        file.write(struct.pack('I', len(serialized_tree)))
        file.write(serialized_tree)

        for f in inputFiles:
            assert isinstance(f, CostumeFile)

            file.write(struct.pack('B', f.n_padding))
            file.write(struct.pack('I', len(f.byteCompressedName)))

            file.write(f.byteCompressedName)

            file.write(struct.pack('B', f.d_padding))
            file.write(struct.pack('I', len(f.byteCompressedData)))

            file.write(f.byteCompressedData)

    return outputFilePath

def decompress():
    if not inputFiles:
        showNoInputMessage()
        # custom_warning()
        return
    
    for f in inputFiles:
        if f.fileExtentsion() != '.huff':
            showNotDecompressable()
            continue
        
        outFilesList = []

        with open(f.path, 'rb') as file:
            # read the tree
            serialized_tree_length = struct.unpack('I', file.read(4))[0] 
            serialized_tree = file.read(serialized_tree_length)
            huffmantree = pickle.loads(serialized_tree)
            outFile = CostumeFile()

            while True:
                try:
                    name_padding = struct.unpack('B', file.read(1))[0]
                    name_length = struct.unpack('I', file.read(4))[0]
                    byteCompressedName = file.read(name_length)
                    
                    data_padding = struct.unpack('B', file.read(1))[0]
                    data_length = struct.unpack('I', file.read(4))[0]
                    byteCompressedData = file.read(data_length)

                # catch and check if curser has reached the end of the file
                except Exception as e:
                    if not file.tell() == os.path.getsize(f.path):
                        raise e
                    else:
                        break

                compressedName = ''.join(f'{byte:08b}' for byte in byteCompressedName)
                outFile.compressedName = compressedName[:len(compressedName)-name_padding]
            
                compressedData = ''.join(f'{byte:08b}' for byte in byteCompressedData)
                outFile.compressedData = compressedData[:len(compressedData)-data_padding]
            
                outFilesList.append(createDecompressedFile(outFile, huffmantree))

            mesg = '\n'.join(f"{f}" for f in outFilesList)
            messagebox.showinfo("Succees", f"File decompressed and saved successfully!\nFiles:\n{mesg}")

    clearProgramInputs()

def createDecompressedFile(outFile, huffmanTree):
    assert isinstance(outFile, CostumeFile)

    outFileName = huffmanDecode(huffmanTree, outFile.compressedName).decode('utf-8')
    name, extension= os.path.splitext(outFileName)

    # If file already exists, add the duplication postfix to the name of the file
    duplication_count = 0
    name_aux = name
    while os.path.isfile(os.path.join(folderPath, name_aux + extension)):
        duplication_count += 1
        name_aux= name + '(' + str(duplication_count) + ')'
        
    name = name + '(' + str(duplication_count) + ')'

    with open(os.path.join(folderPath, name + extension), 'wb') as file:
        file.write(huffmanDecode(huffmanTree, outFile.compressedData))

    return name+extension

# Create the main window
root = tk.Tk()
root.geometry("400x300")
root.title("Huffman Compressor")

# Create and place the label
label = tk.Label(root, text="Upload your file(s) for compression")
label.pack(pady=10)

# Create and place the upload button
upload_button = tk.Button(root, text="upload file", command=uploadFile)
upload_button.pack(pady=5)

compress_button = tk.Button(root, text= "output directory", command=askOutputDirectory)
compress_button.pack(pady=5)

compress_button = tk.Button(root, text= "compress", command=compress)
compress_button.pack(pady=5)

decompress_button = tk.Button(root, text= "decompress", command=decompress)
decompress_button.pack(pady=5)

# Run the GUI event loop
root.mainloop()