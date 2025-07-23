import slypi.ps.upload_csv as uc
from typing import NamedTuple
import slypi.ensemble.algorithms.reduction as algorithms
import pandas as pd
import numpy as np

class ModelPayload(NamedTuple):

    slycatProjectURL: str
    slycatPort: str
    username: str
    password: str

    slycatProjectName: str
    slycatModelName: str

# this function uses slypi to create a new table with columns for PCA
# (note that we could do this directly using sci-kit learn, and that normally
# you would only use slypi on ensembles, but this is just a demonstration)
def do_PCA(inFile, outFile):

    # read csv file
    df = pd.read_csv(inFile)

    # keep only the numeric columns
    numeric_df = df[['MPG', 'Cylinders', 'Displacement', 
                     'Horsepower', 'Weight', 'Acceleration', 'Year']]

    # set up PCA
    arg_list = ['--algorithm', 'PCA', '--num-dim', '2', '--whiten']
    algorithm = algorithms.DimensionReduction(arg_list=arg_list)
    
    # remove NaNs, do PCA
    X = numeric_df.to_numpy()
    algorithm.fit(X)
    reduced_data = algorithm.transform(X)

    # add columns back to table
    pca_df = df
    pca_df["[XYpair X]PCA X"] = pd.Series(reduced_data[:,0])
    pca_df["[XYpair Y]PCA Y"] = pd.Series(reduced_data[:,1])

    # pca_df = df.assign(PCA_X = pd.Series(reduced_data[:,0]), 
    #                    PCA_Y = pd.Series(reduced_data[:,1]))
    
    # now save a new .csv file
    pca_df.to_csv(outFile, index=False)

def create_ps_model(payload: ModelPayload, inFile):

    pzr = uc.parser()
    proj = ["--project-name", payload.slycatProjectName]
    model_name = ["--model-name", payload.slycatModelName]

    myFile = [inFile]

    inCols = ["--input-columns", "Cylinders", "Displacement", "Year"]
    outCols = ["--output-columns", "Horsepower", "MPG"]
 
    host = [
        "--host",
        payload.slycatProjectURL,
        "--kerberos"
        # "--port",
        # payload.slycatPort,
        # "--user",
        # payload.username,
        # "--password",
        # payload.password,
        # "--no-verify",
    ]

    args = pzr.parse_args(myFile + inCols + outCols + host + proj + model_name)

    result = uc.create_model(args, uc.log)

    return result

if __name__ == "__main__":

    # model without PCA
    payload = ModelPayload("https://slycat-qual2.sandia.gov", "9000", "slycat", "slycat", "Cars", "Cars")
    url = create_ps_model(payload, 'example-data/cars-no-nans.csv')

    # create PCA table
    do_PCA('example-data/cars-no-nans.csv', 'example-data/cars-pca.csv')

    payload = ModelPayload("https://slycat-qual2.sandia.gov", "9000", "slycat", "slycat", "Cars", "Cars w/ PCA")
    url = create_ps_model(payload, 'example-data/cars-pca.csv')