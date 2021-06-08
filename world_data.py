# world_data.py
# Bhavyai Gupta
#
# A terminal-based application for computing and printing statistics based on given input.
# Detailed specifications are provided via the Assignment 5 git repository.
# You must include the main listed below. You may add your own additional classes, functions, variables, etc.
# You may import any modules from the standard Python library, including numpy and pandas.
# Remember to include docstrings and comments.

import pandas as pd


def get_user_input(valid_options):
    """Function to get a valid user input. The user input is valid if it is present in the object passed as the parameter

        Parameters:
            valid_options (pandas.core.indexes.base.Index): an index of valid input options that the user can enter

        Returns:
            user_input (str): the valid input by the user
    """

    while(True):
        user_input = input("\nEnter a valid UN Sub-Region: ")

        try:
            # if user has not entered a valid UN Sub-Region, throw ValueError
            if user_input not in valid_options:
                raise ValueError(
                    "\nYou must enter a valid UN Sub-Region name.")

            # if user has entered a valid UN Sub-Region, return the user_input
            else:
                return user_input

        except ValueError as e:
            print("", e)


def find_null(x):
    """
    Function to print the which data is missing the Sq Km values

        Parameters:
            x (pandas.core.series.Series): an object of Series where null values need to be checked

        Return:
            None
    """
    x = pd.Series(x)

    # compare the size without and with dropping NaN to check missing data
    if x.dropna().size == x.size:
        print("\n\nThere are no missing sq km values for this sub-region.")

    else:
        print("\n\nSq Km measurements are missing for: \n")
        print(x[x.isnull()])


def main():
    # Stage 1: Import data
    # --------------------------------------------------------------------------------
    # printing the program header
    print("\nENSF 592 World Data")

    # reading the world data as is from the source
    world_data_raw = pd.read_excel(r'Assign5Data.xlsx', index_col=[1, 2, 0])

    # sorting the indexes of world data
    world_data_sorted = world_data_raw.sort_index()

    # Stage 2: Request user input
    # --------------------------------------------------------------------------------
    # get a valid sub-region from the user
    chosen_sub_region = get_user_input(
        world_data_sorted.index.get_level_values(1))

    # Stage 3: Find any missing sq km data values for the chosen sub-region
    # --------------------------------------------------------------------------------
    # filtering the sorted world data based on the sub-region entered by user
    world_data_sorted_subregion = world_data_sorted[world_data_sorted.index.get_level_values(
        "UN Sub-Region") == chosen_sub_region]

    # print if there is any missing values in the 'Sq Km' column
    find_null(world_data_sorted_subregion.loc[:, "Sq Km"])

    # Stage 4: Calculations and dataset printing for the chosen sub-region
    # --------------------------------------------------------------------------------
    print("\n\nCalculating change in population and latest density...\n")
    world_data_sorted_subregion.loc[:, "Delta Pop"] = world_data_sorted_subregion.loc[:,
                                                                                      "2020 Pop"] - world_data_sorted_subregion.loc[:, "2000 Pop"]
    world_data_sorted_subregion.loc[:, "Pop Density"] = world_data_sorted_subregion.loc[:,
                                                                                        "2020 Pop"] / world_data_sorted_subregion.loc[:, "Sq Km"]

    print(world_data_sorted_subregion)

    print("\n\nNumber of threatened species in each country of the sub-region:\n")
    print(
        world_data_sorted_subregion.loc[:, ("Plants (T)", "Fish (T)", "Birds (T)", "Mammals (T)")])

    print("\n\nThe calculated sq km area per number of threatened species in each country is:\n")

    sum_of_threatened_species = world_data_sorted_subregion.loc[:, "Plants (T)"] + world_data_sorted_subregion.loc[:, "Fish (T)"] + \
        world_data_sorted_subregion.loc[:, "Birds (T)"] + \
        world_data_sorted_subregion.loc[:, "Mammals (T)"]
    print(world_data_sorted_subregion.loc[:, "Sq Km"] / sum_of_threatened_species)


if __name__ == '__main__':
    main()
