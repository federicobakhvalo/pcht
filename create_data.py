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

print('hello world')

# def create_new_json(file):
#     all_types=TicketModel.select()
#     arr=[]
#     for type in all_types:
#         print(type.number_of_ticket)
#         arr.append({'number_of_ticket':type.number_of_ticket,'title':type.title,'text':type.text,'files':type.files})
#
#     with open(file,'w' ,encoding='utf-8') as f:
#         new_dumps=json.dumps(arr)
#         f.writelines(new_dumps)
#         print('success update dupmp')
#
# print(create_new_json('json-data.json'))

