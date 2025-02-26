# -*- coding: utf-8 -*-
"""

Original file is located at    https://colab.research.google.com/drive/1-uJqGeKZfJegX0TmovhsO90iasyxZYiT

### Introduction
Tabular augmentation is a new experimental space that makes use of novel and traditional data generation and synthesisation techniques to improve model prediction success. It is in essence a process of modular feature engineering and observation engineering while emphasising the order of augmentation to achieve the best predicted outcome from a given information set.
Data augmentation can be defined as any method that could increase the size or improve the quality of a dataset by generating new features or instances without the collection of additional data-points. Data augmentation is of particular importance in image classification tasks where additional data can be created by cropping, padding, or flipping existing images.
Tabular cross-sectional and time-series prediction tasks can also benefit from augmentation. Here we divide tabular augmentation into columnular and row-wise methods. Row-wise methods are further divided into extraction and data synthesisation techniques, whereas columnular methods are divided into transformation, interaction, and mapping methods.
To take full advantage of tabular augmentation for time-series you would perform the techniques in the following order: (1) transforming, (2) interacting, (3) mapping, (4) extracting, and (5) synthesising (forthcoming). What follows is a practical example of how the above methodology can be used. The purpose here is to establish a framework for table augmentation and to point and guide the user to existing packages.
See the [Skeleton Example](#example), for a combination of multiple methods that lead to a halfing of the mean squared error.

Test sets should ideally not be preprocessed with the training data, as in such a way one could be peaking ahead in the training data. The preprocessing parameters should be identified on the test set and then applied on the test set, i.e., the test set should not have an impact on the transformation applied. As an example, you would learn the parameters of PCA decomposition on the training set and then apply the parameters to both the train and the test set.
The benefit of pipelines become clear when one wants to apply multiple augmentation methods. It makes it easy to learn the parameters and then apply them widely. For the most part, this notebook does not concern itself with 'peaking ahead' or pipelines, for some functions, one might have to restructure to code and make use of open source pacakages to create your preferred solution.


**Notebook Dependencies**
pip install deltapy pykalman tsaug ta tsaug pandasvault gplearn ta seasonal pandasvault


"""


"""Some of these categories are fluid and some techniques could fit into multiple buckets.
This is an attempt to find an exhaustive number of techniques, but not an exhuastive list of implementations of the techniques.

For example, there are thousands of ways to smooth a time-series, but we have only includes 1-2 techniques of interest under each category.

### **(1) [<font color="black">Transformation:</font>](#transformation)**
-----------------
1. Scaling/Normalisation
2. Standardisation
10. Differencing
3. Capping
13. Operations
4. Smoothing
5. Decomposing
6. Filtering
7. Spectral Analysis
8. Waveforms
9. Modifications
11. Rolling
12. Lagging
14. Forecast Model

### **(2) [<font color="black">Interaction:</font>](#interaction)**
-----------------
1. Regressions
2. Operators
3. Discretising
4. Normalising
5. Distance
6. Speciality
7. Genetic

### **(3) [<font color="black">Mapping:</font>](#mapping)**
-----------------
1. Eigen Decomposition
2. Cross Decomposition
3. Kernel Approximation
4. Autoencoder
5. Manifold Learning
6. Clustering
7. Neighbouring

### **(4) [<font color="black">Extraction:</font>](#extraction)**
-----------------
1. Energy
2. Distance
3. Differencing
4. Derivative
5. Volatility
6. Shape
7. Occurence
8. Autocorrelation
9. Stochasticity
10. Averages
11. Size
13. Count
14. Streaks
14. Location
15. Model Coefficients
16. Quantile
17. Peaks
18. Density
20. Linearity
20. Non-linearity
21. Entropy
22. Fixed Points
23. Amplitude
23. Probability
24. Crossings
25. Fluctuation
26. Information
27. Fractals
29. Exponent
30. Spectral Analysis
31. Percentile
32. Range
33. Structural
12. Distribution


"""
import warnings, os, sys
warnings.filterwarnings('ignore')

import pandas as pd, numpy as np
import re

from tsfresh import extract_relevant_features, extract_features
from tsfresh.utilities.dataframe_functions import roll_time_series


try :
  import pandasvault

except:
  pass




###########################################################################################
###########################################################################################
def data_copy():
  df = pd.read_csv("https://github.com/firmai/random-assets-two/raw/master/numpy/tsla.csv")
  df["Close_1"] = df["Close"].shift(-1)
  df = df.dropna()
  df["Date"] = pd.to_datetime(df["Date"])
  df = df.set_index("Date")
  return df



def test_prepro_all():
  from deltapy import transform, interact, mapper, extract
  df = data_copy(); df.head()

  df_out = transform.robust_scaler(df, drop=["Close_1"])
  df_out = transform.standard_scaler(df, drop=["Close"])
  df_out = transform.fast_fracdiff(df, ["Close","Open"],0.5)
  #df_out = transform.windsorization(df,"Close",para,strategy='both')
  df_out = transform.operations(df,["Close"])
  df_out= transform.triple_exponential_smoothing(df,["Close"], 12, .2,.2,.2,0);
  df_out = transform.naive_dec(df, ["Close","Open"])
  df_out = transform.bkb(df, ["Close"])
  df_out = transform.butter_lowpass_filter(df,["Close"],4)
  df_out = transform.instantaneous_phases(df, ["Close"])
  df_out = transform.kalman_feat(df, ["Close"])
  df_out = transform.perd_feat(df,["Close"])
  df_out = transform.fft_feat(df, ["Close"])
  df_out = transform.harmonicradar_cw(df, ["Close"],0.3,0.2)
  df_out = transform.saw(df,["Close","Open"])
  df_out = transform.modify(df,["Close"])
  df_out = transform.multiple_rolling(df, columns=["Close"])
  df_out = transform.multiple_lags(df, start=1, end=3, columns=["Close"])
  df_out  = transform.prophet_feat(df.reset_index(),["Close","Open"],"Date", "D")

  #**Interaction**
  df_out = interact.lowess(df, ["Open","Volume"], df["Close"], f=0.25, iter=3)
  df_out = interact.autoregression(df)
  df_out = interact.muldiv(df, ["Close","Open"])
  df_out = interact.decision_tree_disc(df, ["Close"])
  df_out = interact.quantile_normalize(df, drop=["Close"])
  df_out = interact.tech(df)
  df_out = interact.genetic_feat(df)

  #**Mapping**
  df_out = mapper.pca_feature(df,variance_or_components=0.80,drop_cols=["Close_1"])
  df_out = mapper.cross_lag(df)
  df_out = mapper.a_chi(df)
  df_out = mapper.encoder_dataset(df, ["Close_1"], 15)
  df_out = mapper.lle_feat(df,["Close_1"],4)
  df_out = mapper.feature_agg(df,["Close_1"],4 )
  df_out = mapper.neigh_feat(df,["Close_1"],4 )


  #**Extraction**
  extract.abs_energy(df["Close"])
  extract.cid_ce(df["Close"], True)
  extract.mean_abs_change(df["Close"])
  extract.mean_second_derivative_central(df["Close"])
  extract.variance_larger_than_standard_deviation(df["Close"])
  # extract.var_index(df["Close"].values,var_index_param)
  extract.symmetry_looking(df["Close"])
  extract.has_duplicate_max(df["Close"])
  extract.partial_autocorrelation(df["Close"])
  extract.augmented_dickey_fuller(df["Close"])
  extract.gskew(df["Close"])
  extract.stetson_mean(df["Close"])
  extract.length(df["Close"])
  extract.count_above_mean(df["Close"])
  extract.longest_strike_below_mean(df["Close"])
  extract.wozniak(df["Close"])
  extract.last_location_of_maximum(df["Close"])
  extract.fft_coefficient(df["Close"])
  extract.ar_coefficient(df["Close"])
  extract.index_mass_quantile(df["Close"])
  extract.number_cwt_peaks(df["Close"])
  extract.spkt_welch_density(df["Close"])
  extract.linear_trend_timewise(df["Close"])
  extract.c3(df["Close"])
  extract.binned_entropy(df["Close"])
  extract.svd_entropy(df["Close"].values)
  extract.hjorth_complexity(df["Close"])
  extract.max_langevin_fixed_point(df["Close"])
  extract.percent_amplitude(df["Close"])
  extract.cad_prob(df["Close"])
  extract.zero_crossing_derivative(df["Close"])
  extract.detrended_fluctuation_analysis(df["Close"])
  extract.fisher_information(df["Close"])
  extract.higuchi_fractal_dimension(df["Close"])
  extract.petrosian_fractal_dimension(df["Close"])
  extract.hurst_exponent(df["Close"])
  extract.largest_lyauponov_exponent(df["Close"])
  extract.whelch_method(df["Close"])
  extract.find_freq(df["Close"])
  extract.flux_perc(df["Close"])
  extract.range_cum_s(df["Close"])
  extract.structure_func(df["Close"])
  extract.kurtosis(df["Close"])
  extract.stetson_k(df["Close"])



def pd_ts_basic(df, input_raw_path = None, dir_out = None, features_group_name = None, auxiliary_csv_path = None, drop_cols = None, index_cols = None, merge_cols_mapping = None, cat_cols = None, id_cols = None, dep_col = None, coldate = None, max_rows = 10):
    df['date_t'] = pd.to_datetime(df[coldate])
    df['year'] = df['date_t'].dt.year
    df['month'] = df['date_t'].dt.month
    df['week'] = df['date_t'].dt.week
    df['day'] = df['date_t'].dt.day
    df['dayofweek'] = df['date_t'].dt.dayofweek
    return df[['year', 'month', 'week', 'day', 'dayofweek'] ], []



def pd_ts_identity(df, input_raw_path = None, dir_out = None, features_group_name = None, auxiliary_csv_path = None, drop_cols = None, index_cols = None, merge_cols_mapping = None, cat_cols = None, id_cols = None, dep_col = None, coldate = None, max_rows = 10):
    df_drop_cols = [x for x in df.columns.tolist() if x in drop_cols]
    df = df.drop(df_drop_cols, axis = 1)
    return df, cat_cols


def pd_ts_rolling(df, input_raw_path = None, dir_out = None, features_group_name = None, auxiliary_csv_path = None, drop_cols = None, index_cols = None, merge_cols_mapping = None, cat_cols = None, id_cols = None, dep_col = None, coldate = None, max_rows = 10):
    cat_cols = []
    created_cols = []

    len_shift = 28
    for i in [7,14,30,60,180]:
        print('Rolling period:', i)
        df['rolling_mean_'+str(i)] = df.groupby(['id'])[dep_col].transform(lambda x: x.shift(len_shift).rolling(i).mean())
        df['rolling_std_'+str(i)]  = df.groupby(['id'])[dep_col].transform(lambda x: x.shift(len_shift).rolling(i).std())
        created_cols.append('rolling_mean_'+str(i))
        created_cols.append('rolling_std_'+str(i))

    # Rollings
    # with sliding shift
    for len_shift in [1,7,14]:
        print('Shifting period:', len_shift)
        for len_window in [7,14,30,60]:
            col_name = 'rolling_mean_tmp_'+str(len_shift)+'_'+str(len_window)
            df[col_name] = df.groupby(['id'])[dep_col].transform(lambda x: x.shift(len_shift).rolling(len_window).mean())
            created_cols.append(col_name)


    for col_name in id_cols:
        created_cols.append(col_name)

    return df[created_cols], cat_cols



def pd_ts_lag(df, input_raw_path = None, dir_out = None, features_group_name = None, auxiliary_csv_path = None, drop_cols = None, index_cols = None, merge_cols_mapping = None, cat_cols = None, id_cols = None, dep_col = None, coldate = None, max_rows = 10):
    created_cols = []
    cat_cols = []

    lag_days = [col for col in range(28, 28+15)]
    for lag_day in lag_days:
        created_cols.append('lag_' + str(lag_day))
        df['lag_' + str(lag_day)] = df.groupby(['id'])[dep_col].transform(lambda x: x.shift(lag_day))


    for col_name in id_cols:
        created_cols.append(col_name)

    return df[created_cols], cat_cols



def pd_tsfresh_features_single_row(df_single_row, cols):
    """

    :param df_single_row:
    :param cols:
    :return:
    """
    df_cols = df_single_row.columns.tolist()
    selected_cols = [x for x in df_cols if re.match("d_[0-9]",x)]
    single_row_df_T = df_single_row[selected_cols].T
    single_row_df_T["time"] = range(0, len(single_row_df_T.index))
    single_row_df_T["id"] = range(0, len(single_row_df_T.index))
    single_row_df_T.rename(columns={ single_row_df_T.columns[0]: "val" }, inplace = True)

    X_feat = extract_features(single_row_df_T, column_id='id', column_sort='time')

    feat_col_names = X_feat.columns.tolist()
    feat_col_names_mapping = {}
    for feat_col_name in feat_col_names:
        feat_col_names_mapping[feat_col_name] = feat_col_name.replace('"','').replace(',','')

    X_feat = X_feat.rename(columns = feat_col_names_mapping)
    X_feat_T = X_feat.T

    for col in cols:
        X_feat_T[col] = np.repeat(df_single_row[col].tolist()[0], len(X_feat_T.index))
    # X_feat_T["item_id"] = np.repeat(df_single_row["item_id"].tolist()[0], len(X_feat_T.index))
    # X_feat_T["id"] = np.repeat(df_single_row["id"].tolist()[0], len(X_feat_T.index))
    # X_feat_T["cat_id"] = np.repeat(df_single_row["cat_id"].tolist()[0], len(X_feat_T.index))
    # X_feat_T["dept_id"] = np.repeat(df_single_row["dept_id"].tolist()[0], len(X_feat_T.index))
    # X_feat_T["store_id"] = np.repeat(df_single_row["store_id"].tolist()[0], len(X_feat_T.index))
    # X_feat_T["state_id"] = np.repeat(df_single_row["state_id"].tolist()[0], len(X_feat_T.index))
    X_feat_T["variable"] = X_feat_T.index

    df_single_row["variable"] = pd.Series(["demand"])
    X_feat_T = X_feat_T.append(df_single_row, ignore_index= True)
    return X_feat_T.set_index(cols + ['variable']).rename_axis(['day'], axis=1).stack().unstack('variable').reset_index()




########################################################################################################################
