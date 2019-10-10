"""
Author: Ken Holm
Purpose: List all the pets and allow the customer to
          see information about a chosen pet
"""
import pymysql.cursors
from creds import *
from petsClass import *

"""
 Initializing our pets dictionary
"""
petsDict = {}

"""
 Give our user a list of pets from which to choose
"""
def listChoices():
    """
     Print a nice header
     :rtype: None
    """
    print("*".center(30, "*"))
    print(" Pet Chooser ".center(30, "*"))
    print("*".center(30, "*"))

    """
     And now, our list of pets with their IDs
    """
    for petId in petsDict:
        print(f"[{petId}] {petsDict[petId].getPetName()}")

    """
     And the option to quit
    """
    print("[Q] Quit")


"""
 Connect to the database
"""
try:
    connection = pymysql.connect(host=host,
                                 user=username,
                                 password=password,
                                 db=database,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

except Exception as e:
    print("An error has occurred.  Exiting.")
    print(e)
    print()
    exit()

"""
 Now that we are connected, execute a query
  and do something with the result set.
"""
try:
    with connection.cursor() as cursor:
        """
         Our sql statement, easy to read
        """
        sql = """
        select
          pets.id as id
          , pets.name as pet
          , pets.age
          , owners.name as owner
          , types.animal_type as animal
        from
          pets
        join
          owners
        on pets.owner_id = owners.id
        join
          types
        on pets.animal_type_id = types.id;
        """

        """
         Execute query
        """
        cursor.execute(sql)

        """
         Loop through all the results
          Append a new Pet object to our pets dictionary
        """
        for row in cursor:
            tempPet = Pet(petId=row['id'],
                          animalType=row['animal'],
                          ownerName=row['owner'],
                          petAge=row['age'],
                          petName=row['pet'])
            petsDict[row['id']] = tempPet

except Exception as e:
    print("An error has occurred.  Exiting.")
    print(e)
    print()

finally:
    connection.close()

"""
 Now, we have a list of pets in petsDict
  Print our list from which to choose,
  allow our user to choose
"""
while True:
    listChoices()
    pet = None

    try:
        pet = input("Please choose from the list above: ")

        if pet == "Q" or pet == "q":
            print("Thank you.")
            break

        elif int(pet) in petsDict:
            tempPet = petsDict[int(pet)]
            print(f"You have chosen {tempPet.getPetName()}, the {tempPet.getAnimalType()}.  {tempPet.getPetName()} is {tempPet.getPetAge()} years old.  {tempPet.getPetName()}'s owner is {tempPet.getOwnerName()}.")
            print()

        else:
            print(f"There is no pet with ID {pet}.")

    except ValueError as e:
        print(f"It appears that '{pet}' is not a Pet ID or 'Q'")

    except Exception as e:
        print(f"{pet} is an invalid choice")
        print(f"Error message: {e}")
