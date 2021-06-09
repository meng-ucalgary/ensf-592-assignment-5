# world_data.py
# Bhavyai Gupta
#
# A terminal-based application for computing and printing statistics based on given input.
# Detailed specifications are provided via the Assignment 5 git repository.
# You must include the main listed below. You may add your own additional classes, functions, variables, etc.
# You may import any modules from the standard Python library, including numpy and pandas.
# Remember to include docstrings and comments.

import pandas as pd
import colors
import os


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
                raise ValueError("\n{0}You must enter a valid UN Sub-Region name.{1}".format(colors.red, colors.reset))

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

    # compare the size without and with dropping NaN to check missing data
    if x.dropna().size == x.size:
        print("\n{0}There are no missing sq km values for this sub-region.{1}".format(colors.green, colors.reset))

    else:
        # print the missing values using masking operation
        print("\n{0}Sq Km measurements are missing for:{1}".format(colors.red, colors.reset))
        print(x[x.isnull()])


def main():
    # Windows Console does not recognize the ANSI escape sequence from external programs
    #
    # using os.system('') exploits a bug in cmd.exe, where cmd.exe is failing to disable the VT Mode,
    # and thus printing the colored output rather than the ANSI sequence itself
    #
    # For more information of this bug, go to https://bugs.python.org/issue30075
    #
    # This line (os.system("")) is added to make sure the colored output is printed when this application
    # is started in windows default console.
    os.system("")



    # Stage 1: Import data
    # --------------------------------------------------------------------------------
    # printing the program header
    print("\n{0}ENSF 592 World Data{1}".format(colors.yellow, colors.reset))

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
    # creating an object of IndexSlice
    idx = pd.IndexSlice

    # filtering the sorted world data based on the sub-region entered by user
    world_data_sorted_subregion = world_data_sorted.loc[idx[:, chosen_sub_region, :], idx["Sq Km": "2020 Pop"]]

    # alternate way of doing the above operation it without IndexSlice (using Masks)
    # world_data_sorted_subregion = world_data_sorted[world_data_sorted.index.get_level_values("UN Sub-Region") == chosen_sub_region]

    # print the data without truncation
    # with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.width', None, 'display.max_colwidth', -1):  # more options can be specified also
    #   print(world_data_sorted_subregion)

    # print if there is any missing values in the 'Sq Km' column
    find_null(world_data_sorted_subregion.loc[idx[:], idx["Sq Km"]])


    # Stage 4: Calculations and dataset printing for the chosen sub-region
    # --------------------------------------------------------------------------------
    print("\n\n{0}Calculating change in population and latest density...{1}".format(colors.cyan, colors.reset))
    world_data_sorted_subregion.loc[:, "Delta Pop"] = world_data_sorted_subregion.loc[:,"2020 Pop"] - world_data_sorted_subregion.loc[:, "2000 Pop"]
    world_data_sorted_subregion.loc[:, "Pop Density"] = world_data_sorted_subregion.loc[:,"2020 Pop"] / world_data_sorted_subregion.loc[:, "Sq Km"]

    print(world_data_sorted_subregion)


    print("\n\n{0}Number of threatened species in each country of the sub-region:{1}".format(colors.cyan, colors.reset))

    # filtering only the threatened species columns
    world_data_sorted_subregion_threatened = world_data_sorted_subregion.loc[idx[:], idx["Plants (T)" : "Mammals (T)"]]
    print(world_data_sorted_subregion_threatened)


    print("\n\n{0}The calculated sq km area per number of threatened species in each country is:{1}".format(colors.cyan, colors.reset))

    # using the computational method sum()
    print(world_data_sorted_subregion.loc[:, "Sq Km"] / world_data_sorted_subregion_threatened.sum(axis=1))


if __name__ == '__main__':
    main()
