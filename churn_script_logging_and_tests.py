'''
Module containing unit tests for customer churn analysis

Author:  Jan Jacobs

Date: 20240613
'''

# Import libaries
import os
import logging
from math import ceil
import churn_library as clib

# Invoke basic logging configuration
logging.basicConfig(
    filename='./logs/unit_test_churn_library.log',
    level=logging.INFO,
    filemode='w',
    format='%(asctime)s - %(name)s - %(levelname)s: %(message)s')


def test_import():
    '''
    Test import_data() function from the churn_library module
    '''
    # Test if the CSV file is available
    try:
        dataframe = clib.import_data("./data/bank_data.csv")
        logging.info("INFO: Testing import_data: SUCCESS")
    except FileNotFoundError as err:
        logging.error("ERROR: Testing import_data: The file wasn't found")
        raise err

    # Test the dataframe
    try:
        assert dataframe.shape[0] > 0
        assert dataframe.shape[1] > 0
        logging.info(
            'INFO: Rows: %d\tColumns: %d',
            dataframe.shape[0],
            dataframe.shape[1])
    except AssertionError as err:
        logging.error(
            "ERROR: Testing import_data: The file doesn't appear to have rows and columns")
        raise err


def test_eda():
    '''
    Test perform_eda() function from the churn_library module
    '''
    dataframe = clib.import_data("./data/bank_data.csv")
    try:
        clib.perform_eda(dataframe=dataframe)
        logging.info("INFO: Testing perform_eda: SUCCESS")
    except KeyError as err:
        logging.error('ERROR: Column "%s" not found', err.args[0])
        raise err

    # Assert if `churn_distribution.png` is created
    try:
        assert os.path.isfile("./images/eda/churn_distribution.png") is True
        logging.info('INFO: File %s was found', 'churn_distribution.png')
    except AssertionError as err:
        logging.error('ERROR: Not such file on disk')
        raise err

    # Assert if `customer_age_distribution.png` is created
    try:
        assert os.path.isfile(
            "./images/eda/customer_age_distribution.png") is True
        logging.info(
            'INFO: File %s was found',
            'customer_age_distribution.png')
    except AssertionError as err:
        logging.error('ERROR: Not such file on disk')
        raise err

    # Assert if `marital_status_distribution.png` is created
    try:
        assert os.path.isfile(
            "./images/eda/marital_status_distribution.png") is True
        logging.info(
            'INFO: File %s was found',
            'marital_status_distribution.png')
    except AssertionError as err:
        logging.error('ERROR: Not such file on disk')
        raise err

    # Assert if `total_transaction_distribution.png` is created
    try:
        assert os.path.isfile(
            "./images/eda/total_transaction_distribution.png") is True
        logging.info(
            'INFO: File %s was found',
            'total_transaction_distribution.png')
    except AssertionError as err:
        logging.error('ERROR: Not such file on disk')
        raise err

    # Assert if `heatmap.png` is created
    try:
        assert os.path.isfile("./images/eda/heatmap.png") is True
        logging.info('INFO: File %s was found', 'heatmap.png')
    except AssertionError as err:
        logging.error('ERROR: Not such file on disk')
        raise err


def test_encoder_helper():
    '''
    Test encoder_helper() function from the churn_library module
    '''
    # Load DataFrame
    dataframe = clib.import_data("./data/bank_data.csv")

    # Create `Churn` feature
    dataframe['Churn'] = dataframe['Attrition_Flag'].\
        apply(lambda val: 0 if val == "Existing Customer" else 1)

    # Categorical Features
    cat_columns = ['Gender', 'Education_Level', 'Marital_Status',
                   'Income_Category', 'Card_Category']

    try:
        encoded_df = clib.encoder_helper(
            dataframe=dataframe,
            category_lst=[],
            response=None)

        # Data should be the same
        assert encoded_df.equals(dataframe) is True
        logging.info(
            "INFO: Testing encoder_helper(data_frame, category_lst=[]): SUCCESS")
    except AssertionError as err:
        logging.error(
            "ERROR: Testing encoder_helper(data_frame, category_lst=[])")
        raise err

    try:
        encoded_df = clib.encoder_helper(
            dataframe=dataframe,
            category_lst=cat_columns,
            response=None)

        # Column names should be same
        assert encoded_df.columns.equals(dataframe.columns) is True

        # Data should be different
        assert encoded_df.equals(dataframe) is False
        logging.info(
            "INFO: Testing encoder_helper(data_frame, category_lst=cat_columns, "
            "response=None): SUCCESS")
    except AssertionError as err:
        logging.error(
            "ERROR: Testing encoder_helper(data_frame, category_lst=cat_columns, "
            "response=None)")
        raise err

    try:
        encoded_df = clib.encoder_helper(
            dataframe=dataframe,
            category_lst=cat_columns,
            response='Churn')

        # Columns names should be different
        assert encoded_df.columns.equals(dataframe.columns) is False

        # Data should be different
        assert encoded_df.equals(dataframe) is False

        # Number of columns in encoded_df is the sum of columns in data_frame
        # and the newly created columns from cat_columns
        assert len(
            encoded_df.columns) == len(
            dataframe.columns) + len(cat_columns)
        logging.info(
            "INFO: Testing encoder_helper(data_frame, category_lst=cat_columns, "
            "response='Churn'): SUCCESS")
    except AssertionError as err:
        logging.error(
            "ERROR: Testing encoder_helper(data_frame, category_lst=cat_columns, "
            "response='Churn')")
        raise err


def test_perform_feature_engineering():
    '''
    Test perform_feature_engineering() function from the churn_library module
    '''
    # Load the DataFrame
    dataframe = clib.import_data("./data/bank_data.csv")

    # Churn feature
    dataframe['Churn'] = dataframe['Attrition_Flag'].\
        apply(lambda val: 0 if val == "Existing Customer" else 1)

    try:
        (_, x_test, _, _) = clib.perform_feature_engineering(
            dataframe=dataframe,
            response='Churn')

        # `Churn` must be present in `data_frame`
        assert 'Churn' in dataframe.columns
        logging.info(
            "INFO: Testing perform_feature_engineering. `Churn` column is present: SUCCESS")
    except KeyError as err:
        logging.error(
            'ERROR: The `Churn` column is not present in the DataFrame')
        raise err

    try:
        # x_test size should be 30% of `data_frame`
        assert (
            x_test.shape[0] == ceil(
                dataframe.shape[0] *
                0.3)) is True   # pylint: disable=E1101
        logging.info(
            'INFO: Testing perform_feature_engineering. DataFrame sizes are consistent: SUCCESS')
    except AssertionError as err:
        logging.error(
            'ERROR: Testing perform_feature_engineering. DataFrame sizes are not correct')
        raise err


def test_train_models():
    '''
    Test train_models() function from the churn_library module
    '''
    # Load the DataFrame
    dataframe = clib.import_data("./data/bank_data.csv")

    # Churn feature
    dataframe['Churn'] = dataframe['Attrition_Flag'].\
        apply(lambda val: 0 if val == "Existing Customer" else 1)

    # Feature engineering
    (x_train, x_test, y_train, y_test) = clib.perform_feature_engineering(
        dataframe=dataframe,
        response='Churn')

    # Assert if `logistic_model.pkl` file is present
    try:
        clib.train_models(x_train, x_test, y_train, y_test)
        assert os.path.isfile("./models/logistic_model.pkl") is True
        logging.info('INFO: File %s was found', 'logistic_model.pkl')
    except AssertionError as err:
        logging.error('ERROR: Not such file on disk')
        raise err

    # Assert if `rfc_model.pkl` file is present
    try:
        assert os.path.isfile("./models/rfc_model.pkl") is True
        logging.info('INFO: File %s was found', 'rfc_model.pkl')
    except AssertionError as err:
        logging.error('ERROR: Not such file on disk')
        raise err

    # Assert if `roc_curve_result.png` file is present
    try:
        assert os.path.isfile('./images/results/roc_curve_result.png') is True
        logging.info('INFO: File %s was found', 'roc_curve_result.png')
    except AssertionError as err:
        logging.error('ERROR: Not such file on disk')
        raise err

    # Assert if `rfc_results.png` file is present
    try:
        assert os.path.isfile('./images/results/rf_results.png') is True
        logging.info('INFO: File %s was found', 'rf_results.png')
    except AssertionError as err:
        logging.error('ERROR: Not such file on disk')
        raise err

    # Assert if `logistic_results.png` file is present
    try:
        assert os.path.isfile('./images/results/logistic_results.png') is True
        logging.info('INFO: File %s was found', 'logistic_results.png')
    except AssertionError as err:
        logging.error('ERROR: Not such file on disk')
        raise err

    # Assert if `feature_importances.png` file is present
    try:
        assert os.path.isfile(
            './images/results/feature_importances.png') is True
        logging.info('INFO: File %s was found', 'feature_importances.png')
    except AssertionError as err:
        logging.error('ERROR: Not such file on disk')
        raise err


if __name__ == "__main__":
    test_import()
    test_eda()
    test_encoder_helper()
    test_perform_feature_engineering()
    test_train_models()
