## Convert your dicom files into png files
With easy to use interface and effortless DICOM to PNG conversion, our program streamlines the process ensuring a user-friendly experience for efficient medical image processing.
Simplest usage:
```
    python makepngcopy.py -W /user/dicomfolder -D /user/destinationfolder
```

For resizing your images use `-R` or `--resize` command.
<details>
<summary>Example usage!<summary>
```
    python makepngcopy.py -W /user/dicomfolder -D /user/destinationfolder -R 512 512
```
Note: Requires 2 arguments. X value and Y value
</details>

Decide bit format for your image with `-B` or `--bit` command.
<details>
<summary>Example usage!<summary>
```
    python makepngcopy.py -W /user/dicomfolder -D /user/destinationfolder -B 16
```
Note: 
    Only 8 bit grayscale, 16 bit grayscale and 24 bit RGB is available.
    Default bit format is **24 RGB**. 
    Updates will be made to the application.
</details>