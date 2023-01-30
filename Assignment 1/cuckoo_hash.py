# explanations for member functions are provided in requirements.py
# each file that uses a cuckoo hash should import it from this file.
import random as rand
from typing import List

class CuckooHash:
	def __init__(self, init_size: int):
		self.__num_rehashes = 0
		self.CYCLE_THRESHOLD = 10

		self.table_size = init_size
		self.tables = [[None]*init_size for _ in range(2)]
		
		self.current_table, self.current_evictions = 0, 0

	def hash_func(self, key: int, table_id: int) -> int:
		key = int(str(key) + str(self.__num_rehashes) + str(table_id))
		rand.seed(key)
		return rand.randint(0, self.table_size-1)

	def get_table_contents(self) -> List[List[int]]:
		return self.tables

	# you should *NOT* change any of the existing code above this line
	# you may however define additional instance variables inside the __init__ method.

	def insert(self, key: int) -> bool:
		# TODO
		self.current_table, self.current_evictions = 0, 0
		while self.current_evictions<=self.CYCLE_THRESHOLD:
			hash_value = self.hash_func(key, self.current_table)
			if self.tables[self.current_table][hash_value] is not None:
				current_value = self.tables[self.current_table][hash_value]
				self.tables[self.current_table][hash_value] = key
				key = current_value
				self.current_table = 1-self.current_table
				self.current_evictions += 1
			else:
				self.tables[self.current_table][hash_value] = key
				return True
		return False

	def lookup(self, key: int) -> bool:
		# TODO
		return self.tables[0][self.hash_func(key, 0)] == key or self.tables[1][self.hash_func(key, 1)] == key

	def delete(self, key: int) -> None:
		# TODO
		hash_zero, hash_one = self.hash_func(key, 0), self.hash_func(key, 1)
		if self.tables[0][hash_zero] == key:
			self.tables[0][hash_zero] = None
		elif self.tables[1][hash_one] == key:
			self.tables[1][hash_one] = None

	def rehash(self, new_table_size: int) -> None:
		self.__num_rehashes += 1; self.table_size = new_table_size # do not modify this line
		# TODO
		old_tables = self.tables.copy()
		self.tables = [[None]*self.table_size for _ in range(2)]
		for table in old_tables:
			for element in table:
				if element is not None:
					self.insert(element)

	# feel free to define new methods in addition to the above
	# fill in the definitions of each required member function (above),
	# and for any additional member functions you define

