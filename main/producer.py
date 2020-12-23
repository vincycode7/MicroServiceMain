# amqps://yfofakbv:zuY0LXSRMOWaz5y9p50V-cLiyccXQi_y@rattlesnake.rmq.cloudamqp.com/yfofakbv
import pika, json

params = pika.URLParameters("amqps://yfofakbv:zuY0LXSRMOWaz5y9p50V-cLiyccXQi_y@rattlesnake.rmq.cloudamqp.com/yfofakbv")

connection = pika.BlockingConnection(params)

channel = connection.channel()

def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='',routing_key='admin',body=json.dumps(body), properties=properties)