import pika, json

from main import Product, db

params = pika.URLParameters("amqps://yfofakbv:zuY0LXSRMOWaz5y9p50V-cLiyccXQi_y@rattlesnake.rmq.cloudamqp.com/yfofakbv")

connection= pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue="main")

def callback(ch, method, properties, body):
    print('Recieved in main')
    data = json.loads(body)
    print(data, properties.content_type)

    if properties.content_type == 'product_created':
        product = Product(id=data['id'], title=data['title'], image=data['image'])
        db.session.add(product)
        db.session.commit()
        print('Product created in main')
    elif properties.content_type == 'product_updated':
        try:
            product = Product.query.get(data['id'])
            product.title = data['title']
            product.image = data['image']
        except:
            product = Product(id=data['id'], title=data['title'], image=data['image'])
            db.session.add(product)
        db.session.commit()
        print('Product updated in main')
    elif properties.content_type == 'product_deleted':
        try:
            product = Product.query.get(data)
            db.session.delete(product)
            db.session.commit()
        except:
            return
        print('Product deleted in main')

channel.basic_consume(queue="main", on_message_callback=callback, auto_ack=True)
print('Started Consuming')

channel.start_consuming()
channel.close()