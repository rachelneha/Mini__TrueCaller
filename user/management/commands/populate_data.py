from django.core.management import BaseCommand

from user.models import Contact

DATASET = [
  {
    "name": "John Doe",
    "phone_number": "1234567890",
    "added_by_id": 1,
    "no_of_spam_count": 0,
    "created_at": "2023-07-24T00:00:00Z"
  },
  {
    "name": "Alice Smith",
    "phone_number": "9876543210",
    "added_by_id": 2,
    "no_of_spam_count": 2,
    "created_at": "2023-07-24T10:15:00Z"
  },
  {
    "name": "Bob Johnson",
    "phone_number": "4567891230",
    "added_by_id": 1,
    "no_of_spam_count": 1,
    "created_at": "2023-07-23T20:30:00Z"
  },
  {
    "name": "Eve Brown",
    "phone_number": "6549873210",
    "added_by_id": 3,
    "no_of_spam_count": 0,
    "created_at": "2023-07-22T12:45:00Z"
  },
  {
    "name": "Michael Lee",
    "phone_number": "7891234560",
    "added_by_id": 2,
    "no_of_spam_count": 0,
    "created_at": "2023-07-22T15:20:00Z"
  },
  {
    "name": "Jane Davis",
    "phone_number": "3698521470",
    "added_by_id": 3,
    "no_of_spam_count": 3,
    "created_at": "2023-07-23T08:00:00Z"
  },
  {
    "name": "William Wilson",
    "phone_number": "1593578520",
    "added_by_id": 1,
    "no_of_spam_count": 0,
    "created_at": "2023-07-23T18:10:00Z"
  },
  {
    "name": "Linda Martinez",
    "phone_number": "8529637410",
    "added_by_id": 2,
    "no_of_spam_count": 1,
    "created_at": "2023-07-24T06:30:00Z"
  },
  {
    "name": "David Robinson",
    "phone_number": "2581473690",
    "added_by_id": 1,
    "no_of_spam_count": 0,
    "created_at": "2023-07-23T14:50:00Z"
  },
  {
    "name": "Susan Miller",
    "phone_number": "7539514680",
    "added_by_id": 3,
    "no_of_spam_count": 2,
    "created_at": "2023-07-22T22:05:00Z"
  }
]


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        for row in DATASET:
            if not Contact.objects.filter(phone_number=row['phone_number']).exists():
                print('adding', row['name'])
                Contact.objects.create(**row)
