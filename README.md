# TODO

- finish readme
- add license

# Project Title

CENACT - Carbon-based Encoding of Neighbourhoods with Atom Count Tables

## Authors

- [@MoritzWeckbecker](https://www.github.com/MoritzWeckbecker)


## Manuscript
This package is created for a paper currently in peer review. 

Abstract:
 > To use machine learning methods in the field of organic chemistry for tasks such as similarity search, virtual screening or drug design, fingerprinting algorithms are required to render peptides and other organic compounds interpretable by machines. Simultaneously, the success of such models is contingent upon both the nature of the information that is encoded in the fingerprint as well as the manner in which this information is presented.
 A recently published encoding, motivated by the carbon backbone of organic compounds, captures the neighbourhoods of these carbon atoms in form of a numerical array.
 We propose a new Carbon-based Encoding of Neighbourhoods using Atom Count Tables (CENACT), which employs the same idea of carbon neighbourhoods but saves this information in a more rigid count table. This rigid structure strongly improves the benefit of the encoding for machine learning models.
 Applied to the task of binary peptide classification using a Random Forest Classifier, our proposed encoding significantly improves upon its predecessor on 52 out of 60 datasets.
 In comparison with 45 peptide encodings applied to 50 datasets from various biomedical fields, the encoding performed well on the entire scope and even achieved the best results on two datasets.
 The approach is domain- and task-agnostic and can be applied to all organic molecules including unnatural and exotic amino acids as well as cyclic peptides and larger proteins, which we demonstrate in our experiments. The new encoding was developed as a Python package (CENACT), the source code and corresponding datasets can be found at [https://github.com/MoritzWeckbecker/CENACT](https://github.com/MoritzWeckbecker/CENACT).

## Dependencies

## Data
The example datasets which are used to evaluate CENACT are collecte from the [peptidereactor](https://doi.org/10.1093/nargab/lqab039) [repository](https://github.com/spaenigs/peptidereactor/tree/master/data). We took all datasets from that repository and placed them at [Data/Original_datasets/](Data/Original_datasets/). Each data set has a separate README file that contains the additional information of that data set. For the comparison between CENACT and its predecessor encoding, CMANGOES, we collected additional datasets which can only be handled by these molecular encodings but not by the encodings in [peptidereactor](https://doi.org/10.1093/nargab/lqab039).

## Code
|Script|Description|
|---|---|
|[Source/](./Source/)|contains all scripts necessary to run the tool.
|[Source/cenact.py](./Source/cenact.py)|contains the code that creates the CENACT encoding.
|[Source/encoding.py](./Source/encoding.py)|contains the code that encodes all datasets in Data folder.
|[Source/rfc_with_cv.py](./Source/rfc_with_cv.py)|contains the code that does training and prediction based on the encoded datasets using Random Forest Classifiers with Cross-Validation splits.
|[Source/benchmark.py](./Source/benchmark.py)|contains the code that benchmarks the runtime of the algorithm.
|[Source/cnn.py](./Code/Machine_Learning.Rmd)|contains the code that does training and prediction based on the encoded datasets using a basic Convolutional Neural Network.

## Running the encoding for a single dataset
Place yourself in the [Source](./Source) directory, then run the following command `python cenact.py --help` to see how to run the tool for a single dataset. The output of this option is presented here:

```
usage: CENACT [-h]
              [--alphabet_mode {without_hydrogen,with_hydrogen,data_driven}]
              [--level LEVEL] [--image {0,1}] [--show_graph SHOW_GRAPH]
              [--output_path OUTPUT_PATH]
              input_file
              
CENACT - Carbon-based Encoding of Neighbourhoods with Atom Count Tables

positional arguments:
  input_file            A required path-like argument

optional arguments:
  -h, --help            show this help message and exit
  --alphabet_mode {without_hydrogen,with_hydrogen,data_driven}
                        An optional string argument that specifies which
                        alphabet of elements the algorithm should use:
                        Possible options are only using the most abundant
                        elements in proteins and excluding hydrogen, i.e. C,
                        N, O, S ('without_hydrogen'); using the most abundant
                        elements including hydrogen, i.e. H, C, N, O, S
                        ('with_hydrogen'); and using all elements which appear
                        in the smiles strings of the dataset ('data_driven').
  --level LEVEL         An optional integer argument that specifies the upper
                        boundary of levels that should be considered. Default:
                        2 (levels 1 and 2). Any integer returns neighbourhoods
                        up to that level.
  --image {0,1}         An optional integer argument that specifies whether
                        images should be created or not. Default: 0 (without
                        images).
  --show_graph SHOW_GRAPH
                        An optional integer argument that specifies whether a
                        graph representation should be created or not.
                        Default: 0 (without representation). The user should
                        provide the number between 1 and the number of
                        sequences in the parsed input file. Example: if number
                        5 is parsed for this option, a graph representation of
                        the 5th sequence of the input file shall be created
                        and placed in the corresponding images folder.
  --output_path OUTPUT_PATH
                        An optional path-like argument. For parsed paths, the
                        directory must exist beforehand. Default:
                        ./CENACT_Encodings
```

## Running the encoding and prediction pipeline for all datasets
To encode the datasets using CENACT, run the [Source/encoding.py](./Source/encoding.py) script. To get prediction scores using Random Forest Classifiers, run the [Source/rfc_with_cv.py](./Source/rfc_with_cv.py) script afterwards.

You can add your own datasets to the pipeline by adding a folder under [Data/Original_datasets](./Data/original_datasets/) which includes:

1. The sequences of the compounds for which a property should be predicted. Sequences should be saved in a file called seqs.fasta if their sequences are provided in FASTA format or seqs.smiles if their sequences are provided in SMILES format.
2. The prediction array that contains for each compound either a 1 if the compound has the desired property, or a 0 if it lacks the desired property. The array should be saved in a filed called classes.txt with one entry per line.

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Contribution

Any contribution intentionally submitted for inclusion in the work by you, shall be licensed under the MIT Licence.