import sqlite3


def create_tables(cur):
    cur.execute('''CREATE TABLE orders (
                            id INTEGER PRIMARY KEY,
                            promocode_id INTEGER);''')

    cur.execute('''CREATE TABLE promocodes (
                                id INTEGER PRIMARY KEY,
                                name TEXT,
                                discount INTEGER NOT NULL);''')
    

def add_order(cur, promocode_id):
    cur.execute('''INSERT INTO orders(promocode_id)
                    VALUES(?)''', (promocode_id,))
    

def add_promocode(cur, name, discount):
    cur.execute('''INSERT INTO promocodes(name, discount)
                    VALUES(?,?)''', (name, discount))


def show_table(cur, table):
    print(f'---------------{table}------------------')
    for row in cur.execute(f'SELECT * FROM {table}'):
        print(row)
    print('-------------------------------------------')


def task_one(cur):
    for i in cur.execute('''SELECT AVG(promocode_id IS NOT NULL)
                            FROM orders;'''):
        print(i)
    
    for i in cur.execute('''SELECT 1.0 * COUNT(promocode_id) / COUNT(*)
                            FROM orders;'''):
        print(i)
        

def task_two(cur):
    for i in cur.execute('''SELECT name
                                FROM
                                    (SELECT discount, name
                                    FROM promocodes
                                    JOIN orders
                                    ON orders.promocode_id = promocodes.id)
                                GROUP BY name
                                ORDER BY SUM(discount) DESC
                                LIMIT 1
                            '''):
        print(i)


def main():
    con = sqlite3.connect('1.sqlite3')
    cur = con.cursor()
    
    con.commit()
    
    show_table(cur, 'promocodes')
    show_table(cur, 'orders')
    
    task_one(cur)
    task_two(cur)
    

if __name__ == '__main__':
    main()
