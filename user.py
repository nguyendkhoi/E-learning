from django.contrib.auth import get_user_model
import random

User = get_user_model()

# List of Vietnamese first names and last names for generating random full names
first_names = ["Minh", "Hoa", "Tuan", "Linh", "Quan", "Mai", "Duc", "Thao", "Nam", "Hang"]
last_names = ["Nguyen", "Tran", "Le", "Pham", "Hoang", "Vu", "Do", "Bui"]

def create_sample_users():
    # List to store created users
    created_users = []
    
    for i in range(20):
        # Generate random full name
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        full_name = f"{last_name} {first_name}"
        
        # Create username from full name (lowercase, no spaces)
        username = f"{first_name.lower()}{last_name.lower()}{i+1}"
        
        # Create email from username
        email = f"{username}@gmail.com"
        
        # Create user with consistent password
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=username,  # Password same as username
                full_name=full_name,
                role=random.choice(['student', 'teacher'])  # Randomly assign role
            )
            created_users.append(user)
            print(f"Created user: {username} ({full_name})")
            
        except Exception as e:
            print(f"Error creating user {username}: {str(e)}")
    
    # Print summary
    print(f"\nCreated {len(created_users)} users successfully")
    return created_users

# Run the function to create users
if __name__ == "__main__":
    users = create_sample_users()