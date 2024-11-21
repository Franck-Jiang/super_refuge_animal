# Super animal refuge of rainbow city 

## Usage
This is a fastapi website used for an animal refuge manager.  
As a guest user you can have access to : 
- `/animal/show` to list all animals eligible for adoption

but you are needed to sign up first for any other operation.

As a logged `user` you can have access to :
- `/animal/adopt` to select and adopt an eligible animal

As a logged `worker` you can have access to :
- `/animal/add_animal` to add a new animal to the refuge
- `/animal/valid_adopt` to validate an adoption

As a logged `admin` you can have access to :
- `/animal/add_species` to add a new animal species
- `/animal/remove_species` to remove an animal species
- `/add_worker` to change a user into worker
- `/remove_worker` to change a worker to user
- `/remove_user` to remove a user

## Database :


animal_species
---------------
- id (PK)
- species_name
- food
    - not used but could be implemented somewhere I guess ...

animal_records
---------------
- id (PK)
- name
- description
- weight
- arrival_date
- animal_id (FK -> animal_species.id)
- adopted

adoption_list
---------------
- id (PK)
- animal_id (FK -> animal_records.id)
- user_adopter_id (FK -> user.id)
- validated
- worker_validation_id (FK -> user.id)
- adoption_date

user_category
---------------
- id (PK)
- category
    - 1 = admin
    - 2 = user
    - 3 = worker

user
---------------
- id (PK)
- username
- password
    - hashed ! 
- category_id (FK -> user_category.id)
- created_at
- updated_at

This api is not polished but it works, some button and html are missing but lacking time to finish all the front. :D

Implemented :
=> Error 403 When not authenticated or not enought privileges
=> 


