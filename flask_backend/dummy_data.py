import random
import json
from faker import Faker

# Initialize Faker
fake = Faker()

# Sample data pools
sample_positions = [
    "Software Engineer", "Senior Software Engineer", "Lead Developer", "Full Stack Developer",
    "Product Manager", "Senior Product Manager", "Product Owner", "Product Director",
    "UX Designer", "UI/UX Designer", "Senior Designer", "Design Lead",
    "Data Analyst", "Data Scientist", "Data Engineer", "Analytics Lead"
]

sample_statuses = ["Active", "On Leave", "Remote", "Inactive", "Probation", "Contract"]

def generate_dummy_users(total_users=1000):
    users = []
    for i in range(total_users):
        user = {
            "id": i + 1,
            "name": fake.name(),
            "position": random.choice(sample_positions),
            "address": fake.address().replace('\n', ', '),
            "status": random.choice(sample_statuses),
            "email": fake.email(),
            "phone": fake.phone_number(),
            "department": fake.company_suffix(),
            "hire_date": fake.date_between(start_date='-5y', end_date='today').strftime('%Y-%m-%d'),
            "employee_id": fake.unique.random_number(digits=6)
        }
        users.append(user)
    return users


def generate_dummy_documents(total_documents=1000):
    documents = []
    for i in range(total_documents):
        document = {
            "id": fake.uuid4(),
            "name": fake.file_name(),
            "description": fake.paragraph(),
            "filrecent_datetimee": fake.file_path(),
            "category": random.choice(["Document", "Image", "Video"]),
            "status": random.choice(["Active", "Inactive", "Pending"]),
            "tags": [fake.word() for _ in range(random.randint(1, 5))],
            "createdAt": fake.past_datetime().isoformat(),
            "updatedAt": fake.past_datetime().isoformat()
        }
        documents.append(document)
    return documents

# Generate users
USERS = generate_dummy_users(1000)

# Generate documents
DOCUMENTS = generate_dummy_documents(1000)

