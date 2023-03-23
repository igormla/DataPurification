import pandas as pd
import re
import cleanco


class TransformText:
    """Utility class for transforming text."""

    @staticmethod
    def capitalize_acronyms(text: str):
        """
        Capitalizing acronyms in text.
        Recognises as an acronym a string occurrence if an `&` sign
        is wrapped by 1 to 2 alphanumerical characters, ex. Is&Hs.

        :param text: Original string to be processed.
        :return: Processed string.
        """

        # Find a string occurrence in which an "&" sigh is wrapped by 1 to 2 characters, ex. Is&Hs
        acronym = re.findall(r"\w{1,2}&\w{1,2}", text)

        # Convert the found string occurrence, convert it to uppercase string and return it
        text = re.sub(r"\w{1,2}&\w{1,2}", str(acronym).upper(), text)
        return str(text)

    @staticmethod
    def clean_text_data(data: list):
        """
        Clean text from the key name of every dictionary from the provided data as a list of dictionaries.

        The function cleans text in the following order:

        1. Capitalizes the first letter of every word and replaces the word "Uk" with "UK".

        2. Capitalizes the acronyms of the whole text using the ``capitalize_acronyms()`` method.

        3. Finds " - " and replaces it with "-".

        4. Finds everything between "()" and replaces it with "".

        5. Finds multiple whitespace characters and replaces them with single whitespace character.

        6. Finds every non word character except " ", "&" and "-", then replaces it with " ".

        The function returns the same provided data, only clean processed and updated.

        :param data: A list of dictionaries
        :return: The same provided data, only clean, processed and updated.
        """

        # Find " - " and replace it with "-"
        find_replace_pattern_1 = {r"(\s-\s)": "-"}
        # Find everything between "()" and replace with "" (nothing, just delete it)
        find_replace_pattern_2 = {r"\(.+\)": ""}
        # Find multiple whitespace characters and replace them with single whitespace character
        find_replace_pattern_3 = {r"\s+": " "}
        # Find every non word character except " ", "&" and "-", then and replace with " "
        find_replace_pattern_4 = {r"[^\w\s&-]": " "}

        # Store the regex find and replace patterns in a list
        regex_patterns: list = [find_replace_pattern_1,
                                find_replace_pattern_2,
                                find_replace_pattern_3,
                                find_replace_pattern_4]

        # Iterate over the data nad get each dictionary
        for element in data:

            # Get the name of the first key in the dictionary
            old_text_data = next(iter(element.keys()))
            # Convert the string to titlecase and replace the word "Uk" with "UK"
            new_text_data = str(old_text_data).title().replace("Uk", "UK")
            # Capitalize the acronyms
            new_text_data = TransformText.capitalize_acronyms(new_text_data)
            # Apply the regex patterns to the string
            for regex_pattern in regex_patterns:
                for pattern, replace_string in regex_pattern.items():
                    new_text_data = re.sub(pattern, replace_string, new_text_data)
            # Clean the names of the company's entity type using the "cleanco" library
            new_text_data = cleanco.basename(new_text_data)

            # Update the name of the first key in the dictionary with the new clean name
            element[new_text_data] = element.pop(old_text_data)

        # Return
        return data


class TransformData:
    """Utility class for transforming data."""

    @staticmethod
    def set_first_column(data: pd.DataFrame, column: str):
        """
        Sets the desired first column on a copy of the provided Pandas DataFrame.

        :param data: Provide data in Pandas DataFrame type.
        :param column: Chosen column in string type of the provided data.
        :return: Returns modified copy of the original provided DataFrame.
        """

        # Extract the chosen column in a copy of the provided data and insert it at the beginning (or the first index)
        processed_data = data.copy()
        chosen_column = processed_data.pop(column)
        processed_data.insert(0, column, chosen_column)

        # Return the modified copy of the original provided DataFrame
        return processed_data

    @staticmethod
    def reorder(data: pd.DataFrame):
        """
        Sets the value of first column in each record as a key in a new dictionary.
        Afterwards, sets the column names and values of the rest of the records as the values of the new dictionary,
        but does that in "key: value" model.

        :param data: Provide data in Pandas DataFrame type.
        :return: Returns a list of dictionaries with the modified and reordered data.
        """
        # New list for storing the modified dictionaries
        processed_data = []

        # Convert the provided DataFrame into a list of dictionaries
        records = data.to_dict(orient="records")

        # Iterate over the converted data
        for record in records:

            # Get the name of the first key in the first dictionary
            first_key = next(iter(record))

            # Extract the value of the first key in the first dictionary
            first_value = record.pop(first_key)

            # Set the "first_value" as the key in a dictionary and set the modified dictionary in the current
            # iteration as value in a new dictionary, and at the end append the new dictionary in the created
            # processed_data list
            processed_data.append({first_value: record})

        # Return the process_data list
        return processed_data

    @staticmethod
    def process_data(data: pd.DataFrame, column: str):
        """
        Processes the provided data in Pandas DataFrame format in the following order:

        1. Sets the first column of the DataFrame based on the provided ``column`` argument.

        2. Reorders the data based on the algorithm in the ``reorder()`` method.

        :param data: Provide data in Pandas DataFrame type.
        :param column: Chosen column in string type of the provided data.
        :return: Returns the processed data.
        """
        processed_data = TransformData.set_first_column(data, column)
        processed_data = TransformData.reorder(processed_data)
        return processed_data
