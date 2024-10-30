from MySqlConnection import my_database, TicketModel
import json

with open('json-data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Insert data into the database
with my_database.atomic():  # Use atomic transactions for bulk inserts
    for item in data:

        # Check if a record with the same number_of_ticket exists
        existing_ticket = TicketModel.select().where(TicketModel.number_of_ticket == item['number_of_ticket']).first()
        if not existing_ticket:
            # Create a new record if no existing record is found
            TicketModel.create(
                number_of_ticket=item['number_of_ticket'],
                title=item['title'],
                text=item['text'],
                files=item['files']
            )
        else:
            pass
            #print(existing_ticket.title)


# Close the database connection
my_database.close()
