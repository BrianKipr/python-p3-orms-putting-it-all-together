
import sqlite3

# Connect to the database
CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    def __init__(self, name, breed, id=None):
        self.id = id
        self.name = name
        self.breed = breed

    @classmethod
    def create_table(cls):
        # Create the 'dogs' table if it doesn't exist
        CURSOR.execute('''CREATE TABLE IF NOT EXISTS dogs
                          (id INTEGER PRIMARY KEY, name TEXT, breed TEXT)''')
        CONN.commit()

    @classmethod
    def drop_table(cls):
        # Drop the 'dogs' table if it exists
        CURSOR.execute("DROP TABLE IF EXISTS dogs")
        CONN.commit()

    def save(self):
        if self.id is None:
            # Insert a new dog record
            CURSOR.execute("INSERT INTO dogs (name, breed) VALUES (?, ?)",
                           (self.name, self.breed))
            CONN.commit()
            self.id = CURSOR.lastrowid
        else:
            # Update an existing dog record
            CURSOR.execute("UPDATE dogs SET name=?, breed=? WHERE id=?",
                           (self.name, self.breed, self.id))
            CONN.commit()

    @classmethod
    def create(cls, name, breed):
        dog = cls(name, breed)
        dog.save()
        return dog

    @classmethod
    def new_from_db(cls, data):
        id, name, breed = data
        return cls(name, breed, id)

    @classmethod
    def get_all(cls):
        CURSOR.execute("SELECT * FROM dogs")
        rows = CURSOR.fetchall()
        return [cls.new_from_db(row) for row in rows]

    @classmethod
    def find_by_name(cls, name):
        CURSOR.execute("SELECT * FROM dogs WHERE name=?", (name,))
        row = CURSOR.fetchone()
        if row:
            return cls.new_from_db(row)
        else:
            return None

    def __str__(self):
        return f"ID: {self.id}, Name: {self.name}, Breed: {self.breed}"

if __name__ == '__main__':
    Dog.drop_table()  # Drop the table if it exists (for testing purposes)
    Dog.create_table()  # Create the 'dogs' table

    # Create and save a new dog
    my_dog = Dog.create(name='Buddy', breed='Golden Retriever')
    
    # Fetch and print all dogs
    all_dogs = Dog.get_all()
    for dog in all_dogs:
        print(dog)
    
    # Find a dog by name
    found_dog = Dog.find_by_name('Buddy')
    if found_dog:
        print("Found Dog:", found_dog)
    else:
        print("Dog not found.")

    # Close the database connection
    CONN.close()






