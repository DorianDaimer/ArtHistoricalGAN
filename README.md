# ArtHistoricalGAN
This repository contains the code for the thesis "Latent Space Analysis in an Art creating Generative Adversarial Network".

Due to the file size limits on Github the data folder only contains a 64x64 pixel data set.
The 128x128 pixel data set used in the thesis can be downloaded from Google Drive [here](https://drive.google.com/file/d/1Xjwd_MHNUgoMfN4p76wcv5X57M2TTlJP/view?usp=sharing).

## Usage

### 1. Gather training data

I used training data from wikiart.org, but any training data can be used in principle

There is a zip folder with 64x64 pixel images in the data folder. A larger data set can be downloaded from Drive.

- [Google Drive file](https://drive.google.com/file/d/1Xjwd_MHNUgoMfN4p76wcv5X57M2TTlJP/view?usp=sharing)

 If diffrent paintings are to be used [WikiArt_scrapper.py](utility/WikiArt_scrapper.py) can be used to scrape WikiArt. However WikiArt often changes their side, making older scrappers outdated.

### 2. Prepare the training data

Use [resize_rename.py](utility/resize_rename_images.py) to create image data set of 128x128 pixel images for art scraped from [wikiart.org](https://www.wikiart.org):

```python
python utility/resize_rename_images.py
```

Set the appropriate paths before using this script!

### 3. Modify files

Update the `styles` variable in [wikiart_genre.py](utility/wikiart_genre.py) dictating the number of training images per genre. If using the traning data set from Drive or frome the data directory use:

```python
styles = {
    "Impressionism": 12956,
    "Expressionism": 6736,
    "vincent_van_gogh": 1889,
    "paul_cezanne": 579,
    "paul_gauguin": 499,
}
```


## Credits

Utility functions and README heavily inspired and built off of the GANGogh code available and found at [rkjones4/GANGogh](https://github.com/rkjones4/GANGogh)
