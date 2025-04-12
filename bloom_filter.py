import hashlib
import os


class SimpleBloomFilter:
    """
    A simple implementation of a Bloom Filter, which is a probabilistic data structure
    used to test whether an element is a member of a set. It allows for fast membership testing
    with a small chance of false positives but no false negatives. If an item is not in the filter,
    it is guaranteed to not be in the set. However, if it is marked as present, it may or may not be.

    Attributes:
        size (int): The size of the bit array used to store hash values. The default size is 100,000.
        num_hashes (int): The number of hash functions used to calculate hash values for the given item.
        file_name (str): The name of the file to load or save the Bloom filter's bit array.
        bit_array (list): A list representing the bit array, initialized with 0's, used to track the presence of elements.
        current_path (str): The current working directory, used to determine where the Bloom filter's file is stored.
    """

    def __init__(self, size=100000, num_hashes=6,
                 file_name="bloom_filter_data.txt") -> None:
        """
        Initializes a new Bloom filter with the specified size, number of hash functions,
        and file name for saving/loading the filter data.

        Parameters:
            size (int): The size of the bit array used by the Bloom filter. Default is 100,000.
            num_hashes (int): The number of hash functions to use for each item. Default is 6.
            file_name (str): The name of the file where the bit array will be saved or loaded. Default is "bloom_filter_data.txt".
        """
        self.size = size
        self.num_hashes = num_hashes
        self.file_name = file_name
        self.bit_array = [0] * size  # Initialize bit array with 0's
        self.current_path = os.getcwd()  # Get the current working directory
        self.load_filter()  # Load any previously saved filter data from a file

    def _hashes(self, item):
        """
        Generates hash values for a given item using multiple hash functions.

        Parameters:
            item (str): The item to hash (e.g., an email address).

        Returns:
            list: A list of `num_hashes` hash values calculated from the item.
        """
        hash_values = []
        for i in range(self.num_hashes):
            # Create a unique hash value for each hash function
            hash_value = int(hashlib.sha256(f"{item}{i}".encode()).hexdigest(),
                             16) % self.size
            hash_values.append(hash_value)
        print(hash_values)  # Print the hash values (for debugging purposes)
        return hash_values

    def add(self, item):
        """
        Adds an item to the Bloom filter by setting the corresponding positions in the bit array.

        Parameters:
            item (str): The item to add (e.g., an email address).
        """
        for hash_value in self._hashes(item):
            self.bit_array[
                hash_value] = 1  # Set the bit at the hash value position to 1

    def check(self, item):
        """
        Checks if an item is likely present in the Bloom filter.

        Parameters:
            item (str): The item to check (e.g., an email address).

        Returns:
            bool: True if the item is likely in the filter, False if it is definitely not.
        """
        for hash_value in self._hashes(item):
            if self.bit_array[hash_value] == 0:
                return False  # If any hash value is not set, the item is definitely not present
        return True  # If all hash positions are set, the item is likely present

    def save_filter(self):
        """
        Saves the current Bloom filter's bit array to a file.

        This method writes the bit array to a file specified by the `file_name` attribute,
        allowing the filter's state to be preserved between program executions.
        """
        file_path = os.path.join(self.current_path, self.file_name)
        with open(file_path, 'w') as f:
            f.write(''.join(map(str,
                                self.bit_array)))  # Write the bit array as a string to the file

    def load_filter(self):
        """
        Loads a previously saved Bloom filter's bit array from a file.

        This method reads the bit array from a file if it exists, restoring the filter's state.
        """
        file_path = os.path.join(self.current_path, self.file_name)
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                self.bit_array = list(map(int,
                                          f.read()))  # Read and convert the bit array back from the file


# Example usage:
bloom_filter = SimpleBloomFilter()  # Initialize the Bloom filter
email = "mk@gmail.com"

# Check if the email is already in the filter
if bloom_filter.check(email):
    print("Exists")  # Print if the email is likely present
else:
    bloom_filter.add(email)  # Add the email to the filter
    bloom_filter.save_filter()  # Save the updated filter state to the file
