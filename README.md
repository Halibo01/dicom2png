# Convert your dicom files into png files
With easy to use interface and effortless DICOM to PNG conversion, our program streamlines the process ensuring a user-friendly experience for efficient medical image processing.
Simplest usage:
```
    python makepngcopy.py -W /user/dicomfolder
```
WARNING: In this usage png files and dicom files will be in same location but it wont change the files, dont worry this usage is also safe.

Seperate dicom files and png files from each other:
```
    python makepngcopy.py -W /user/dicomfolder -D /user/destinationfolder
```
For resizing your images use `-R` or `--resize` command.

### Example usage!
```
    python makepngcopy.py -W /user/dicomfolder -D /user/destinationfolder -R 512 512
```
<details>
<summary>Note:</summary>
Requires 2 arguments. X value and Y value
</details>

Decide bit format for your image with `-B` or `--bit` command.
### Example usage!
```
    python makepngcopy.py -W /user/dicomfolder -D /user/destinationfolder -B 16
```
<details>
<summary>Note:</summary>
    Only 8 bit grayscale, 16 bit grayscale and 24 bit RGB is available.
    Default bit format is 24 RGB. 
    Updates will be made to the application.
</details>
made with python version 3.12