import pandas as pd


def concat_id_number_of_sample(path_coffee_names, path_id_and_numbers, column_for_merge='number_of_sample'):
    df_coffee_names = pd.read_csv(path_coffee_names)
    df_id_and_numbers = pd.read_csv(path_id_and_numbers)
    try:
        df_id_and_numbers[column_for_merge] = df_id_and_numbers[column_for_merge].astype('str')
        df_coffee_names[column_for_merge] = df_coffee_names[column_for_merge].astype('str')
        df = df_coffee_names.merge(df_id_and_numbers, on=column_for_merge)
    except:
        print(f"Are you sure there's such a column: {column_for_merge}?")
        return False
    return df
