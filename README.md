# POSTER-COPYCATCH

## Model
### `SimSiam`: for Image Similarity Analytics
### `BLIP`: for Image Captioning
### `all-MiniLM-L6-v2`: for Text Similarity Analytics

## 5 steps for train with `CutMix`
1. **Load Image Batch**: Use a for loop to retrieve an image batch x from the data loader (loader). This batch consists of groups of images that will be fed into the model during the training process.

2. **Clone Batches**: Utilize the clone() method to create two copies of the original batch x. This allows for the application of various transformations to the same data without altering the original data.

3. **Apply CutMix**: Apply the cutmix_data function to each of the duplicated batches. This function mixes images within each batch in different ways, producing two modified image batches. Different pairs of images are selected for CutMix in each batch, so the two resulting batches may differ.

4. **Input to Model and Calculate Loss**: Input the modified batches into the model and use the output to calculate the loss. The loss function considers the mix ratio (lam) from CutMix, calculating based on the predictions and actual values from each batch.

5. **Backpropagation and Optimization**: Perform backpropagation based on the calculated loss and optimize the model’s weights. This process helps the model learn to make better predictions.

## Applied technologies in Training
- **Cosine decay + Warm up**: To improve training speed by reducing the number of epoches required, the training speed is initially gradually increased and then gradually decreased.
- **Early Stopping**: To prevent overfitting, if the number of epoches increases but the train loss does not decrease, then the training will be terminated.
