# Text-2-Strokes (WIP)

An attempt to implement handwriting synthesis basing the paper '[Generating Sequences with Recurrent Neural Networks](https://arxiv.org/abs/1308.0850)' by Alex Graves. GUI is built with electron.js.

## Demo
![GUI_workflow](https://raw.githubusercontent.com/rahul96rajan/text-2-strokes/main/results/samples/gui_example.gif)

## Dependencies
Python libraries required:
```
numpy==1.19.5
matplotlib==3.2.2
torch==1.7.1
```

npm dependencies:
```
electron.js
```

## How to use
<b><ins>Prerequisites :</ins></b>  A working installation of python3 and npm.

After cloning repo, install python packages using ```pip install -r requirements.txt``` (virtual environment recommended)

And similarly install node-modules using ```npm install```

### 1. Download dataset
Download [IAM On-Line Handwriting Database]((http://www.fki.inf.unibe.ch/databases/iam-on-line-handwriting-database). Place the extracted folder `original-xml-part` under `text-2-strokes/data/`.

### 2. Preprocess dataset
```
python extract_data.py
```
This scipt searches `original-xml-part` directory for `xml` files with handwriting data > converts coordinates to offsets > saves the output as `./data/strokes.npy` and `./data/sentences.txt`.

### 3. Train model
```
python train.py --n_epochs 100 --model synthesis --batch_size 32 --text_req 
```

A number of arguments can be set for training if you wish to experiment with the parameters.  The default values are in `train.py`

```
  --hidden_size   #hidden states for LSTM layer
  --n_layers      #LSTM layer
  --batch_size    size of training batch
  --step_size     step size for learning rate decay
  --n_epochs      #Training epochs
  --lr            learning rate
  --patience      patience for early stopping
  --model_type    train model type
  --data_path     path to processed training data
  --save_path     path where training weights are stored
  --text_req      flag indicating to fetch text data also
  --data_aug      flag to whether data augmentation required
  --seed          random seed
```

### 4. Generate handwriting
```
python generate.py --char_seq "input text for handwriting synthesis" --save_img --style 4
```
Similarly a number of arguments can be set for generation also, if you wish to experiment with the parameters. The default values are in `generate.py`

```
  --model        type of model
  --model_path   path to trained weights
  --save_path    output path
  --seq_len      length of input sequence
  --bias         bias term
  --char_seq     input text
  --text_req     flag indicating to fetch text data also
  --seed         random seed
  --data_path    path to processed training data
  --style        style number [0,4]
  --save_img     save output as .png
  --save_gif     save output as .gif
```

#### To run GUI execute:
```npm start```

### Examples
```
python generate.py --char_seq "A sample of generated text" --save_gif --style 1
```
![sample1](https://raw.githubusercontent.com/rahul96rajan/text-2-strokes/main/results/samples/generated_samples1.gif)
</br>
```
python generate.py --char_seq "I am Rahul" --save_gif --style 4
```
![sample2](https://raw.githubusercontent.com/rahul96rajan/text-2-strokes/main/results/samples/generated_samples2.gif)
