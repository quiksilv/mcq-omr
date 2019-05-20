# Upload and extraction

In the html index page, a simple form accepts ONLY zip files that contain the scanned image files with the png file format. `upload.py` extracts only the png files and creates them under `cgi-bin/tmp`. It then runs `imagepro.py` on all the image files.

# Optical Mark Recognition

Each image can be assumed to be unique due to random effects when scanning the physical paper, how each answer box is shaded and slight rotations of the paper itself. A position calibration step is necessary for alignment. This is done by looking for the coordinates of the first fully shaded answer box and also the positions of the answer boxes.

Then we load the answer sheets which may or may not contain the exact amount of answers per question. It may be possible for each question row to have no shaded answers or more than one shaded answer. We apply a mask of variable size based on the answer box and calculate the ratio of nonzero pixels to the total number of pixels in the box.

Since the answer sheet itself can be dirty with non-answer pencil marks, we plot a 20 bin histogram to separate noise from shaded answers (signal). The cut off threshold can be reliably estimated by summing backwards from the highest bin up to the point where the sum totals 40.

# Storage

The results from each answer sheet is stored in a simple Sqlite3 database and read out with `read.py`.

# Libraries used

* opencv2
* numpy
