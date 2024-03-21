from flask import Flask, redirect, request, jsonify, render_template, url_for
import pymysql.cursors

app = Flask(__name__)

def get_db_connection():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='1234',
                                 db='SYS',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection

@app.route('/')
def index():
    return render_template('inventory.html')

@app.route('/inventory', methods=['GET'])
def get_product():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM inventory")
        products = cursor.fetchall()
    conn.close()
    return render_template('display_inventory.html', products=products) 


@app.route('/inventory/new', methods=['GET'])
def create_product_form():
    return render_template('create_product.html')

@app.route('/inventory/update/<Pid>', methods=['GET'])
def show_update_product_form(Pid):
    conn = get_db_connection()
    product = None
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM inventory WHERE Pid = %s", (Pid,))
        product = cursor.fetchone()
    conn.close()
    if product:
        return render_template('update_product.html', product=product)
    else:
        return 'Product not found', 404

@app.route('/inventory/update/<Pid>', methods=['GET', 'POST','PUT'])
def update_products(Pid):
    conn = get_db_connection()
    if request.method == 'POST':
        data = request.form
        Pname = data['Pname']
        Pbrand = data['Pbrand']
        with conn.cursor() as cursor:
            sql = "UPDATE inventory SET Pname = %s, Pbrand = %s WHERE Pid = %s"
            cursor.execute(sql, (Pname, Pbrand, Pid))
        conn.commit()
        conn.close()
        return jsonify({'status': 'Product updated successfully'}), 200
    else:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM inventory WHERE Pid = %s", (Pid,))
            product = cursor.fetchone()
        conn.close()
        return render_template('update_product.html', product=product)


@app.route('/inventory/delete/<Pid>', methods=['DELETE'])
def delete_products(Pid):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        sql = "DELETE FROM inventory WHERE Pid = %s"
        cursor.execute(sql, (Pid,))
    conn.commit()
    conn.close()
    return jsonify({'status': 'Product deleted successfully'}), 200

@app.route('/inventory', methods=['POST'])
def create_product():
    data = request.form
    Pid = data['Pid']
    Pname = data['Pname']
    Pbrand = data['Pbrand']
    conn = get_db_connection()
    with conn.cursor() as cursor:
        sql = "INSERT INTO inventory (Pid, Pname, Pbrand) VALUES (%s, %s, %s)"
        cursor.execute(sql, (Pid, Pname, Pbrand))
    conn.commit()
    conn.close()
    return jsonify({'status': 'Product added successfully'}), 201


@app.route('/inventory/<Pid>', methods=['PUT'])
def update_product(Pid):
    data = request.form
    Pname = data['Pname']
    Pbrand = data['Pbrand']
    conn = get_db_connection()
    with conn.cursor() as cursor:
        sql = "UPDATE inventory SET Pname = %s, Pbrand = %s WHERE Pid = %s"
        cursor.execute(sql, (Pname, Pbrand, Pid))
    conn.commit()
    conn.close()
    return jsonify({'status': 'Product updated successfully'}), 200

@app.route('/inventory/<Pid>', methods=['DELETE'])
def delete_product(Pid):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        sql = "DELETE FROM inventory WHERE Pid = %s"
        cursor.execute(sql, (Pid,))
    conn.commit()
    conn.close()
    return jsonify({'status': 'Product deleted successfully'}), 200


if __name__ == '__main__':
    app.run(debug=True)