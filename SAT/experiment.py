from math import log

k = 3


def read_test_data():
    file = open("results/test.txt", "r")
    data = []
    for line in file:
        line = line.strip('\n').split(' ')
        if line[1] == '-S1':
            id = int(line[0])
            splits = int(line[2])
            data.append([id, splits, 0])
    file.close()
    return data


def maximization(data, means):
    for data_point in data:
        min_class = 0
        min_dist = 100000000
        for k, mean in enumerate(means):
            dist = get_distance(data_point, mean)
            if dist < min_dist:
                min_dist = dist
                min_class = k
        data_point[2] = min_class
    return data


def get_distance(data_point, mean):
    log_data_point = log(data_point[1] + 1)
    log_mean = log(mean + 1)
    return abs(log_data_point - log_mean)


def expectation(data, means):
    new_means = [0, 0, 0]
    for k, mean in enumerate(means):
        center = 0
        counter = 0
        for data_point in data:
            if data_point[2] == k:
                center += data_point[1]
                counter += 1
        new_means[k] = center / counter
    return new_means


def k_means(data):
    means = [1, 250, 500]

    for _ in range(1000):
        data = maximization(data, means)
        means = expectation(data, means)

    return data


def write_sudoko_classes(data):
    f = open("results/classes.txt", "w")
    for data_point in data:
        line = str(data_point[0]) + " " + str(data_point[2]) + "\n"
        f.write(line)
    f.close()


def read_sudoku_results():
    results = {}
    f = open("results/test.txt", "r")
    for line in f:
        line = line.strip('\n').split(' ')
        id = int(line[0])
        method = line[1]
        splits = int(line[2])
        if id not in results.keys():
            results[id] = [(method, splits)]
        else:
            results[id].append((method, splits))
    f.close()
    return results


def order_and_write_results(results, classes):
    file = open("results/rankings.txt", "w")
    for key in results.keys():
        all_equal = False
        result = results[key]
        random_splits = result[0][1]
        result = sorted(result, key=lambda x: x[1])
        if len(result) == 3:
            if result[0][1] == result[1][1] == result[2][1]:
                all_equal = True

            line = str(key) + " " + result[0][0] + " " + result[1][0] + " " + result[2][0] + " " + str(
                all_equal) + " " + str(classes[key]) + " " + str(random_splits) + "\n"
            file.write(line)
    file.close()


def get_classes(data):
    classes = {}
    for data_point in data:
        classes[data_point[0]] = data_point[2]
    return classes


def get_analysis():
    file = open("results/rankings.txt")
    S1_first = 0
    S2_first = 0
    S3_first = 0
    S1_second = 0
    S2_second = 0
    S3_second = 0
    S1_third = 0
    S2_third = 0
    S3_third = 0
    S1_0 = 0
    S2_0 = 0
    S3_0 = 0
    S1_1 = 0
    S2_1 = 0
    S3_1 = 0
    S1_2 = 0
    S2_2 = 0
    S3_2 = 0
    are_equal = 0
    very_difficult_3 = 0
    very_difficult_2 = 0
    for line in file:
        line = line.strip('\n').split(' ')
        sudoku_id = int(line[0])
        first = line[1]
        second = line[2]
        third = line[3]
        is_equal = line[4] == 'True'
        random_splits = int(line[6])
        sudoku_class = int(line[5])
        if not is_equal:
            if first == '-S1':
                S1_first += 1
            elif first == '-S2':
                S2_first += 1
            elif first == '-S3':
                S3_first += 1

            if second == '-S1':
                S1_second += 1
            elif second == '-S2':
                S2_second += 1
            elif second == '-S3':
                S3_second += 1

            if third == '-S1':
                S1_third += 1
            elif third == '-S2':
                S2_third += 1
            elif third == '-S3':
                S3_third += 1

            if sudoku_class == 0:
                if first == '-S1':
                    S1_0 += 1
                elif first == '-S2':
                    S2_0 += 1
                elif first == '-S3':
                    S3_0 += 1

            if sudoku_class == 1:
                if first == '-S1':
                    S1_1 += 1
                elif first == '-S2':
                    S2_1 += 1
                elif first == '-S3':
                    S3_1 += 1

            if sudoku_class == 2:
                if first == '-S1':
                    S1_2 += 1
                elif first == '-S2':
                    S2_2 += 1
                elif first == '-S3':
                    S3_2 += 1

            if random_splits >= 1000 and first == '-S3':
                very_difficult_3 +=1
            if random_splits >= 1000 and first == '-S2':
                very_difficult_2 +=1
        else:
            are_equal += 1
    file.close()
    file = open("results/analysis.txt", "w")
    line = str(S1_first) + " " + str(S2_first) + " " + str(S3_first) + "\n"
    file.write(line)
    line = str(S1_second) + " " + str(S2_second) + " " + str(S3_second) + "\n"
    file.write(line)
    line = str(S1_third) + " " + str(S2_third) + " " + str(S3_third) + "\n"
    file.write(line)
    line = str(S1_0) + " " + str(S2_0) + " " + str(S3_0) + "\n"
    file.write(line)
    line = str(S1_1) + " " + str(S2_1) + " " + str(S3_1) + "\n"
    file.write(line)
    line = str(S1_2) + " " + str(S2_2) + " " + str(S3_2) + "\n"
    file.write(line)
    line = str(very_difficult_2) + "\n"
    file.write(line)
    line = str(very_difficult_3) + "\n"
    file.write(line)
    line = str(are_equal) + "\n"
    file.write(line)
    file.close()


data = read_test_data()
data = k_means(data)
write_sudoko_classes(data)
classes = get_classes(data)
results = read_sudoku_results()
order_and_write_results(results, classes)
get_analysis()
