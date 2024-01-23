import paho.mqtt.client as mqtt
from db_management import select_all
BROKER_IP = "10.108.33.123"
BUS_ID = 1
CARD_ID = 'W12345'

client = mqtt.Client()


def publish_message(topic: str, message: str):
    client.publish(topic, payload=message)


def connect_to_broker():
    client.connect(BROKER_IP)


def disconnect_from_broker():
    client.disconnect()


def next_stop():
    publish_message("buses/driver", f"next_stop?bus={str(BUS_ID)}")


def choose_course(course_name):
    publish_message("buses/driver", f'choose_course?bus={BUS_ID}&course={course_name}')


def use_card():
    publish_message("buses/worker", f'use_card?card={CARD_ID}&bus={BUS_ID}')


def process_message(client, userdata, message):
    message_decoded = (str(message.payload.decode("utf-8"))).split(".")[0]
    print(f'\n{message_decoded}\n')


def run():
    connect_to_broker()
    client.on_message = process_message
    client.loop_start()
    client.subscribe('response/#')
    while True:
        option = input('\n\n[1] Next stop\n[2] Choose course\n[3] Use card\n')
        if option == '1':
            next_stop()
        elif option == '2':
            print('\n')
            courses = select_all('Courses', ['CourseID', 'CourseName'])
            courses_dict = {}
            for course_id, course_name in courses:
                courses_dict[course_id] = course_name
                print(f'{course_id}. {course_name}')
            choose_course(courses_dict[int(input())])
        elif option == '3':
            use_card()
        else:
            pass


if __name__ == "__main__":
    run()
