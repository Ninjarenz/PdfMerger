# PDF Merger

This is a simple Python script that provides a graphical user interface (GUI) for merging multiple PDF files into a single PDF document. It's built using Tkinter for the UI and relies on the `pypdf` (or `PyPDF2` as a fallback) library for PDF manipulation.

## Features

*   Add multiple PDF files to a list.
*   Reorder PDF files before merging.
*   Remove selected PDF files from the list.
*   Merge all selected PDF files into one output file.
*   Simple and intuitive Tkinter-based user interface.

## Installation

1.  **Prerequisites:** Ensure you have Python 3 installed on your system.

2.  **Install Dependencies:** Open your terminal or command prompt and install the required Python packages:

    ```bash
    pip install pypdf
    ```

    *(Optional: If `pypdf` causes issues, `PyPDF2` can be used as a fallback, but `pypdf` is recommended.)*

## How to Use

1.  **Run the Application:**
    Navigate to the directory containing `Main.py` in your terminal or command prompt and run:

    ```bash
    python Main.py
    ```

2.  **Add PDF Files:**
    *   Click the "Hinzufügen" (Add) button.
    *   Select one or more PDF files from your computer. These will appear in the list on the left.

3.  **Manage Files (Optional):**
    *   **Remove:** Select one or more files in the list and click "Entfernen" (Remove) to remove them.
    *   **Reorder:** Select a file and use the "Nach oben" (Move Up) or "Nach unten" (Move Down) buttons to change its position in the merge order.

4.  **Choose Output Location (Optional but Recommended):**
    *   Click the "Als... (Ziel wählen)" (Save As... (Choose Target)) button to specify the name and location for your merged PDF file. If you don't do this, you will be prompted to choose a location when you click "Zusammenführen".

5.  **Merge PDFs:**
    *   Click the "Zusammenführen (Merge)" button.
    *   If you haven't already specified an output file, a dialog will appear asking you to choose a save location and filename for the merged PDF.
    *   The application will merge the PDFs in the order they appear in the list and save the result to the specified location.

6.  **Clear List:**
    *   Click "Liste leeren" (Clear List) to remove all files from the current list.

## License

```
MIT License

Copyright (c) 2023 [Your Name/Organization Here]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
