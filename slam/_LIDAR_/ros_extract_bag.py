import rosbag

bag = rosbag.Bag('basic_localization_stage.bag')
topics = bag.get_type_and_topic_info()[1].keys()
types = []
#for i in range(0,len(bag.get_type_and_topic_info()[1].values())):
#    print(bag.get_type_and_topic_info())

messages = bag.read_messages()
for topic, msg, t in messages:
    print(topic)
    print(msg)
    print("\n\n\n")