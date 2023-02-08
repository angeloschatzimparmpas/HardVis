# HardVis: Visual Analytics to Handle Instance Hardness Using Undersampling and Oversampling Techniques

This Git repository contains the code that accompanies the research paper "HardVis: Visual Analytics to Handle Instance Hardness Using Undersampling and Oversampling Techniques". The details of the experiments and the research outcome are described in [the paper](https://arxiv.org/abs/2203.15753).

**Note:** HardVis is optimized to work better for standard resolutions (such as 1440p/QHD (Quad High Definition) and 1080p). Any other resolution might need manual adjustment of your browser's zoom level to work properly.

**Note:** The tag `paper-version` matches the implementation at the time of the paper's publication. The current version might look significantly different depending on how much time has passed since then.

**Note:** This software is based on the [XGBoost](https://github.com/dmlc/xgboost) and [Bayesian Optimization](https://github.com/fmfn/BayesianOptimization) libraries. Using the exact same input data, different systems might generate slightly different outputs due to the use of these libraries, and such differences will propagate to our software.

**Note:** As any other software, the code is not bug free. There might be limitations in the views and functionalities of the tool that could be addressed in a future code update.

# Data Sets #
All publicly available data sets used in the paper are in the `data` folder, formatted as comma separated values (csv). 
They are based on the data sets available online from the [UCI Machine Learning Repository](http://archive.ics.uci.edu/ml/index.php): Vehicle Recognition, Breast Cancer Wisconsin (Original), and Iris Flower.

# Requirements #
For the backend:
- [Python 3](https://www.python.org/downloads/) (Version: 3.8.x)
- [MongoDB](https://www.mongodb.com/try/download/community) (Version: 4.x)
- Other packages: `pymongo`, `Flask`, `Flask-PyMongo`, `flask_cors`, `numpy`, `pandas`, `joblib`, `xgboost`, `bayesian-optimization`, `scikit-learn`, `umap-learn`, `scipy`, and `imblearn`.

One way to install MongoDB in macOS is by using Homebrew:
```
brew tap mongodb/brew
brew install mongodb-community@5.0
```

You can install all the backend requirements for Python with the following command:
```
pip install -r requirements.txt
```

For the frontend:
- [Node.js](https://nodejs.org/en/) (including Webpack; to install it, `npm install webpack-dev-server@3.7.1`)

There is no need to install anything further for the frontend (e.g., D3 and Plotly.js), since all modules are in the repository.

For the reproducibility of the use case, the Vehicle Silhouette data set should be inserted to MongoDB by using the commands below:
```
# recommendation: use insertMongo script to add a data set in Mongo database
# for Python3
python3 insertMongo.py
```

# Usage #
Below is an example of how you can get HardVis running using Python and Node.js for the backend and frontend, respectively. The frontend is written in JavaScript/HTML with the help of Vue.js framework, so it could be hosted in any other web server of your preference. The only hard requirement (currently) is that both frontend and backend must be running on the same machine. 
```
# first terminal: hosting the visualization side (client)
# with Node.js
cd frontend
npm install webpack-dev-server@3.7.1
npm run dev
```

```
# second terminal: hosting the computational side (server)
FLASK_APP=run.py flask run
```

Then, open your browser and point it to `localhost:8080`. We recommend using an up-to-date version of Google Chrome.

# Reproducibility of the Results #
The following instructions describe how to reach the results present in Figure 1 of the article. The aforementioned figure is connected with Section 5.2 (*Use case: explorative sampling for better classification*), and it is the main use case described in the paper.

**Note:** We used OSX and Google Chrome in all our tests, so we cannot guarantee that it works in other OS or browser. However, since HardVis is written in JS and Python, it should work in all the most common platforms.

**Tip:** You will have to see a red loading bar on the very top of your browser whenever something is processing.

**Tip:** Our [demonstration video](https://vimeo.com/772796696) also presents the following steps, using the same data set (from 02:04 until 08:00).

- Step 1: Make sure the "Vehicle Silhouette" data set is selected (top-left corner), then reload/refresh the `localhost:8080` page open in your browser. **Please note** that the first time you execute the analysis and, consequently, run the hyperparameter search, it might take a few minutes before the XGBoost classifier's hyperparameters have been tuned, using Bayesian Optimization. After the first time, the results are cached and will be re-used to make the process faster.
- Step 2: When *Data Space* is populated with the data points, click on the stacked bar chart with value *13* for the *Number of Neighbors*, as is shown in Figure 6(a).
- Step 3: We continue by selecting *Undersampling (US)* from the *Data Sets and Sampling Techniques* panel, and then click on the *OSS* option to activate this undersampling algorithm.
- Step 4: After the loading process is over, we set the *Seeds* value to *250* (see Figure 6(c)). Please wait until the red loading bar on the very top is no longer visible. Afterward, we choose value *125* for this same parameter (cf. Figure 6(d)).
- Step 5: At this point, we click on *Rare* from the *Types* parameter to deactivate the algorithm's application to these types of instances. In Figure 6(f), we can observe the result of this action. After everything gets reloaded, we click on *Outlier* type to deactivate this particular type, too (visible due to the removal of the *tick* symbol).
- Step 6: Next, we select all data points in *Data Space* view by holding down the left click button and moving the mouse to surround all data points. This process is performed with the help of the lasso functionality implemented in HardVis, with dashed lines appearing in the *Data Space* view. After waiting a while until the dashed lines disappear, we press the *Execute Undersample* button in this same view.
- Step 7: Afterward, we try out another undersampling phase. Thus, we click on the *OSS* button again to repeat the process one more time. Since the results are becoming worse, we completely deactivate this undersampling algorithm by clicking on the *Disabled* option. Please wait until everything loads before proceeding to the next step.
- Step 8: To receive the image shown in Figure 1, we have to switch to the *Oversampling (OS)* and click on the *SMOTE* option to activate this oversampling algorithm, as illustrated in Figure 1(a). Please wait until everything loads. Finally, we deactivate the *Outlier* option from the *Types* parameter.

**Outcome:** The above process describes how you will be able to reproduce precisely the results presented in Figure 1 of the paper. Thank you for your time!

# Corresponding Author #
For any questions with regard to the implementation or the paper, feel free to contact [Angelos Chatzimparmpas](mailto:angelos.chatzimparmpas@lnu.se).