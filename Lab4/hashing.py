
"""
This file contains a simple implementation of extendable hashing.
DO NOT USE ANY OTHER IMPORTS BESIDES THE ONES ALREADY INCLUDED IN THIS FILE
"""
import copy

from typing import Dict, List, Union


class Bucket:
    """
    A class representing a bucket in extendable hashing. DO NOT MODIFY THIS CLASS
    """

    def __init__(self, ij: int = 1, init_records: Union[List[str], None] = None):
        self.ij: int = ij
        self.capacity: int = 2
        self.records: List[str] = [] if init_records is None else init_records
        self.overflow: Union[Bucket, None] = None

    def __eq__(self, other) -> bool:
        """
        Check if two buckets are equal and all overflow buckets are equal
        """
        contents_eq = (
            self.ij == other.ij
            and self.capacity == other.capacity
            and self.records == other.records
        )
        overflow = self.overflow
        other_overflow = other.overflow
        while overflow is not None and other_overflow is not None:
            if overflow != other_overflow:
                return False
            overflow = overflow.overflow
            other_overflow = other_overflow.overflow

        return contents_eq and overflow is None and other_overflow is None

    def __repr__(self):
        """
        Returns a string representation of the bucket and overflow contents for printing.
        """
        # get the records in the bucket
        internal_records = self.records[:]
        overflow_records = []
        current_overflow = self.overflow
        while current_overflow is not None:
            overflow_records.extend(current_overflow.records)
            current_overflow = current_overflow.overflow

        # split overflow_records into chunks of self.capacity
        overflow_chunks = [
            overflow_records[i : i + self.capacity]
            for i in range(0, len(overflow_records), self.capacity)
        ]

        return f"{[internal_records] + overflow_chunks}"

    def add_record(self, new_record) -> None:
        """
        Add a record to the bucket if it is not full
        """
        if self.is_full:
            raise ValueError("Bucket is full")

        self.records.append(new_record)

    @property
    def is_full(self) -> bool:
        """
        Return True if the bucket is at capacity, False otherwise
        """
        return len(self.records) == self.capacity


class BucketAddressTable:
    """
    Class representing the address table for extendable hashing
    """

    def __init__(self, max_bits: int = 5):
        self.i: int = 1
        self.max_bits = max_bits
        self.address_table: Dict[str, Bucket] = {"0": Bucket(), "1": Bucket()}

    def __eq__(self, other) -> bool:
        return isinstance(other, BucketAddressTable) and self.address_table == other.address_table

    def __str__(self):
        return str(self.address_table)

    def __repr__(self):
        return repr(self.address_table)

    def _add_to_overflow(self, bucket: Bucket, key: str):
        """
        Adds the key to the overflow bucket chain. DO NOT MODIFY THIS FUNCTION
        """
        # if the current bucket has no overflow bucket, create one
        if bucket.overflow is None:
            bucket.overflow = Bucket(ij=self.i)
            bucket.overflow.add_record(key)
        # else, add the record to the last overflow bucket
        else:
            # traverse to the last overflow bucket
            last_overflow = bucket.overflow
            while last_overflow.overflow is not None:
                last_overflow = last_overflow.overflow

            # Check if the last overflow bucket is full
            if last_overflow.is_full:
                # If the last overflow bucket is full, create a new
                # overflow bucket and add it to the chain
                last_overflow.overflow = Bucket(ij=self.i)
                last_overflow = last_overflow.overflow

            # Add the record to the last overflow bucket
            last_overflow.add_record(key)

    def _print_bucket_and_overflow(self, b_key, bucket):
        """
        Print the bucket and its overflow buckets
        """
        print(f"Bucket {b_key} ({bucket.ij}): {bucket.records}")
        overflow = bucket.overflow
        idx = 1
        while overflow is not None:
            print(f"Overflow bucket {idx} for {b_key} ({overflow.ij}): {overflow.records}")
            overflow = overflow.overflow
            idx += 1

    def pretty_print(self):
        """
        Pretty print the address table
        """
        print_map = {}
        for k, v in self.address_table.items():
            b_k = k if v.ij == self.i else k[-v.ij :]
            if v.ij == self.i or (b_k not in print_map and len(v.records) > 0):
                self._print_bucket_and_overflow(b_k, v)
                print_map[b_k] = 1

    def hash_function(self, key: str) -> str:
        """
        Hashes the key by considering the index in the alphabet of the
        first letter (lowercase) using the last self.i bits regardless
        of casing.

        Example (self.i = 5):
            A -> 00001
            a -> 00001
            B -> 00010
            b -> 00010
        """
        # TODO: implement the hash function (~1 to 4 lines)
        first_letter_to_int = ord(key[0].lower()) - ord('a') + 1 # e.g. "Apple" -> 1
        binary_eq = format(first_letter_to_int, f'0{self.max_bits}b')
        return binary_eq[-self.i:] # return as a binary string of last i bits
        

    def _insert_helper(self, key: str, bucket: Bucket):
        """
        Helper function to handle the splitting and redistribution of records
        when inserting a key into a bucket.
        """
        # TODO: implement the helper function (~ 30 lines to implement total)
        # validation to prevent common bug -- DO NOT DELETE
        if self.i < bucket.ij:
            raise ValueError("Cannot insert into a bucket with greater depth")

        # if the current bucket is using the same depth to determine presence
        if bucket.ij == self.i:
            # if we are at the maximum bit depth, use overflow buckets
            if self.i == self.max_bits:
                self._add_to_overflow(bucket, key)
            else:
                # TODO: implement the case when the bucket is full and the
                # address table needs to be doubled (~ 7 lines)
                self.i += 1
                old_table = self.address_table
                new_table = {}
                # double buckets and assign expanded bitstring key
                for k, b in old_table.items():
                    # root keys keep the same values
                    new_table["0" + k] = b
                    new_table["1" + k] = b
                self.address_table = new_table
                # recompute new table entry for key and insert
                new_value = self.hash_function(key)
                self._insert_helper(key, self.address_table[new_value])

        # if the address table is using more bit depth then the current bucket
        if self.i > bucket.ij:
            # TODO: finish the i > ij case (~ 20 lines)
            # alloc new bucket z and set ij += 1 and iz += 1
            old_d = bucket.ij
            bucket.ij += 1
            z = Bucket(ij=bucket.ij)
            
            # change pointers in addr table to correct buckets
            for addr, b in self.address_table.items():
                # only reassign what's pointed to this bucket
                if b is bucket:
                    # new depth to compare at
                    new_suffix = addr[-bucket.ij:] # e.g. addr[-5] -> "..10101"
                    # split on highest bit
                    if new_suffix[0] == '1':
                        self.address_table[addr] = z 
                    else:
                        self.address_table[addr] = bucket

            # remove each record in bucket j and reinsert
            old_records = bucket.records[:]
            bucket.records.clear()
            bucket.overflow = None # reset overflow chain on split
            for r in old_records:
                self.insert(r)

            # recompute the bucket for k and insert record
            # recomp. since bucket referencing addr are different now 
            self.insert(key)


    def insert(self, key):
        """
        Insert a key into a bucket. DO NOT MODIFY THIS FUNCTION
        """
        bval = self.hash_function(key)
        current_bucket = self.address_table[bval]

        # if the current bucket is not full, we can directly place this key
        if not current_bucket.is_full:
            current_bucket.add_record(key)
        # otherwise, we have to split the bucket and redistribute contents until stable
        else:
            self._insert_helper(key, current_bucket)
