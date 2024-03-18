# project_census_crime

## What do we aim to do?
With this model we want to define a benchmark prediction versus crime statistics, so we may extrapolate the model to daily CSAM reports. 
The steps are:

### Benchmark
<ol>
  <li>Cross reference Features from NSW Census with target features from the Crime statistics by LGA.</li>
  <li>Calculate Pearson correlations and focus on any feature with a correlation greater than .5.</li>
  <li>Create a gradient boosted decision tree heuristic to identify the non linear feature importance of each of those features vs our target features.</li>
  <li>Perform Feature Engineering <a href="https://en.wikipedia.org/wiki/Feature_engineering"> (LINK) </a> and iterate feature importance findings to identify typologies.</li>
</ol>

### Extrapolation
<ol>
  <li>Identify statistical significance of a correlation and feature importance analysis with crime statistics as features and daily CSAM reports as target features through LGA.</li>
  <li>Work on typologies following the benchmark, but for daily CSAM reports.</li>
  <li>Perform Feature Engineering on mixed variables from all three datasets to increase the quality of the typologies.</li>
</ol>

## What's in here?
### ETLs
<dl>
  <dt>Description</dt>
    <dd>These libraries and notebook "Extract-Transform-Load" (ETL) the data from:
      <ul>
        <li>Census 2021 Data Packs <a href="https://www.abs.gov.au/census/find-census-data/datapacks">LINK</a>
          <ul>
            <li>General Community Profile. </li>
            <li>Place of Enumeration Profile. </li>
            <li>Working Population Profile. </li>
          </ul>
        <li>BOCSAR crime statistics filtered to juveniles <a href="https://www.bocsar.nsw.gov.au/Pages/bocsar_datasets/Datasets.aspx">LINK</a></li>
      </ul>
    </dd>
  <dt>Files</dt>
    <dd>
      <ul>
      <li><strong>census_etl_notebook.ipynb</strong> is the notebook with the code for executing the ETL that creates the census datasets</li>
      <li><strong>crime_etl_notebook.ipynb</strong> is the notebook with the code for executing the ETL that creates the crime datasets</li>
      <li><strong>census_crime_merge_notebook.ipynb</strong> is the notebook with the code for merging the census and crime datasets</li>
      <li><strong>etl_helper.py</strong> is an auxiliary library where functions reside for running the ETL</li>
      </ul>
    </dd>
</dl>

### EDA
<dl>
  <dt>Description</dt>
    <dd>"Exploratory Data Analysis" (EDA) is the part where we attempt to make sense of the data.
        We'll do this in two main ways:
      <ul>
        <li>Pearson Correlation <a href="https://en.wikipedia.org/wiki/Pearson_correlation_coefficient">LINK</a>.
        <li>Feature importance from a decision tree heuristic named XGBoost. <a href="https://en.wikipedia.org/wiki/XGBoost">LINK</a></li>
      </ul>
    </dd>
  <dt>Files</dt>
    <dd>
      <ul>
      <li><strong>pipeline.py</strong> is an auxiliary library where functions reside for running the model's notebook</li>
      <li><strong>model.ipynb</strong> is the notebook with the code for executing the EDA.</li>
      </ul>
    </dd>
</dl>

## Next Steps

We are interested in gathering additional datasets to expand our daily CSAM reference, as well as perform periodic Quality Assurance on the typologies developed.
