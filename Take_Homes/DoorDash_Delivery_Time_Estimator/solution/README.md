# DoorDash

## Setup

- Copy data from 'doordash.zip/data/' into `./data/`
- Use `docker-compose build` for quick and clean setup.

## Data Engineering

- #### Setup jupyter notebook environment
```shell script
docker-compose up notebooks
```
To open jupyter notebooks click shown `http://127.0.0.1:8888/?token=...` link

- #### EDA
http://127.0.0.1:8888/notebooks/EDA.ipynb 

- #### Pre-processing
http://127.0.0.1:8888/notebooks/pre-processing.ipynb


- #### Model tuning
http://127.0.0.1:8888/notebooks/xgboost_model.ipynb

## Predictions

#### through docker container

Params configurable from entrypoint in [docker-compose.yml](docker-compose.yml)

```shell script
docker-compose up predict
```
By default results available under `./outputs/`.

#### through linux terminal

1. Shell initialization:
    ```.shell script
    export PYTHONPATH="$PYTHONPATH:${HOME}/path/to/project/repo/doordash"
    ```
  
2. Dependencies installation (recommended running in virtual environment):
    ```.shell script
    pip install -r app/requirements.txt
    ```

3. Script description:
    ```shell script
    python predict.py --help
    ```

4. Example prediction:
    ```shell script
    python app/predict.py \
        data/data_to_predict.json \
        models/xgboost_model_with_encoders_2020-03-12T14\:47\:23.005373.pickle \
        --output outputs/output.tsv
    ```
    where: 
    - `data/data_to_predict.json` is file from received `doordash.zip`
    - `models/xgboost_model...` is pickled trained model from [xgboost_model.ipynb](notebooks/xgboost_model.ipynb)
    - `--output outputs/output.tsv` is TSV file with predictions for each `delivery_id` from input data
    

## Tests

```shell script
docker-compose up tests
```
