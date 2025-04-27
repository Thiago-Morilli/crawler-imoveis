from itemadapter import ItemAdapter
from  SpiderHouse.Database.mysql import Mysql_Connector

class SpiderhousePipeline:
    def process_item(self, item, spider):
       self.save_mysql(item)

    def save_mysql(self, item):
        connector = Mysql_Connector.Connection()
        cursor = connector[0]
        db_connection = connector[1]

        cursor.execute(
           '''CREATE TABLE IF NOT EXISTS Properties(
            Title VARCHAR(150), 
            Location VARCHAR(150),
            Price VARCHAR(50),
            Property_Type VARCHAR(30),
            Rooms INT (20),
            Size VARCHAR(20)
            );''' 
        )

        db_connection.commit()      

        insert_query = """
                        INSERT INTO  Properties(Title, Location, Price, Property_Type, Rooms, Size)
                        VALUES (%s, %s, %s, %s, %s, %s)""" 
        
        cursor.execute(insert_query, [
                item.get("Title"),
                item.get("Location"),
                item.get("Price"),
                item.get("Property_Type"),
                item.get("Rooms"),
                item.get("Size")
            ])
        db_connection.commit()
        print("Dados salvos com sucesso!")

        cursor.close()
        db_connection.close()