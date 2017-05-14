import yaml
import os
import logging
import csv

def load_files(path):
    path_to_experiments = ""
    for chunk in path:
        path_to_experiments = os.path.join(path_to_experiments, chunk)
        
    files = list()
    for f in os.listdir(path_to_experiments):
        abs_path = os.path.join(path_to_experiments, f)
        if os.path.isfile(abs_path) and not f == "_README.txt":
            files.append(abs_path)
    
    data = list()
    for f in files:
        with open(f) as stream:
            try:
                element = yaml.load(stream)
            except yaml.YAMLError, e:
                print("Error loading %s: %s" % (f, e))
            else:
                data.append(element)
                        
    return data
            
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    path = ["/","home","firefoxmetzger","Documents","naoProject","experimentData"]
    
    data = load_files(path)
    logger.info("Loaded %i datasets" % len(data))
    
    MIN_NUMBER_OF_GAMES = 4
    
    #extract (unique) users:
    users = list()
    for trial in data:
        user = trial["user"]
        if not user in users:
            users.append(user)
    logger.debug("Found %i unique users" % len(users))
    
    #number of games per user
    num_trials = dict()
    
    for user in users:
        num_trials[user] = 0
        for trial in data:
            if trial["user"] == user:
                num_trials[user] += 1
    logger.debug("Games per user: %s" % str(num_trials))
    
    #mean values per user per game
    means = list()
    for user in users:
        new_means = list()
        for trial in data:
            if trial["user"] == user:
                detections = trial["recognized"]
                confidence = [d["confidence"] for d in detections]
                mean_value = sum(confidence)/len(confidence)
                new_means.append(mean_value)
        means.append(new_means)
    logger.debug("Extracted means per game")
    
    #number of users for amount of games
    amount = dict()
    for mean_values in means:
        for idx in range(1,len(mean_values)+1):
            try:
                amount[idx] += 1
            except KeyError:
                amount[idx] = 1
    logger.info("Amount: %s" % amount)
    
    #wite all data to file
    with open("meanPerGame_v3.csv","w") as output:
        wr = csv.writer(output, quoting=csv.QUOTE_ALL)
        title_row = ["user", "game", "performance"]
        wr.writerow(title_row)
        for user_idx in range(0,len(users)):
            if 2 <= len(means[user_idx]):
                for game in range(1,min(len(means[user_idx]), 5) + 1):
                    data_row = list()
                    data_row.append(users[user_idx])
                    data_row.append(game)
                    data_row.append(means[user_idx][game-1])
                    wr.writerow(data_row)
    
    #write to file
    with open("meanPerGame_v1.csv","w") as output:
        wr = csv.writer(output, quoting=csv.QUOTE_ALL)
        title_row = ["user", "game", "performance"]
        wr.writerow(title_row)
        for user_idx in range(0,len(users)):
            if len(means[user_idx])>=MIN_NUMBER_OF_GAMES:
                for game in range(1,MIN_NUMBER_OF_GAMES+1):
                    data_row = list()
                    data_row.append(users[user_idx])
                    data_row.append(game)
                    data_row.append(means[user_idx][game-1])
                    wr.writerow(data_row)
                
    #write to file
    with open("meanPerGame_v2.csv","w") as output:
        wr = csv.writer(output, quoting=csv.QUOTE_ALL)
        
        title_row = ["user"]
        for idx in range(1,MIN_NUMBER_OF_GAMES+1):
            title_row.append("game%i" % idx)
        wr.writerow(title_row)
        for user_idx in range(0,len(users)):
            if len(means[user_idx]) >= MIN_NUMBER_OF_GAMES:
                data_row = means[user_idx][:MIN_NUMBER_OF_GAMES]
                data_row.insert(0,users[user_idx])
                wr.writerow(data_row)
    
