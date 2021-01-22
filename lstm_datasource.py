import database
import shelve

def download_training_data():
    cxn = database.connection()
    cxn.connect()
    dataset = cxn.get_popular_comments('aww')
    training_db = shelve.open('Data/trainingdata.db')
    index = 0
    for row in dataset:
        training_db[str(index)] = row
        index = index + 1

def get_training_data(maxsize):
    res = []
    with shelve.open('Data/trainingdata.db') as trainingdata:
        for d in trainingdata:
            post, comment = trainingdata[d]
            if len(post) <= 80 and len(comment) <= 80:
                res.append(trainingdata[d])
    trainingdata.close()
    return res[:maxsize]
