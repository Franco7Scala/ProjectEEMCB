import numpy 
import random
import knn


if __name__ == '__main__':
    best_k = 1
    weighted = False
    # loading data
    set_training_big_i = None
    set_training_little_i = None
    set_test_i = None
    set_training_big_o = None
    set_training_little_o = None
    set_test_o = None

    quantity_neighbors = 500

    # training to find weights
    for i in range(len(set_training_big_i)):
        # finding neighbors
        current_input = set_training_big_i[i]
        neighbors = knn.find_k_neighbors(current_input, set_training_big_i, set_training_big_o, quantity_neighbors)
        # saving neighbors
        
        # calculate weights

        # saving weights

    # testing on test set
    for i in range(len(set_test_i)):
        # calculating error
        current_input = set_test_i[i]
        error = knn.get_error_estimation_weighted_on_input(current_input, set_training_big_i, set_training_big_o, best_k, weighted)
        # calculating statistics

    # printing results

    # saving results

























# m denotes the number of examples here, not the number of features
def gradient_descent(x, y, theta, alpha, m, numIterations):
    x_trans = x.transpose()
    for i in range(0, numIterations):
        hypothesis = numpy.dot(x, theta)
        loss = hypothesis - y
        # avg cost per example (the 2 in 2*m doesn't really matter here.
        # But to be consistent with the gradient, I include it)
        cost = numpy.sum(loss ** 2) / (2 * m)
        print("Iteration %d | Cost: %f" % (i, cost))
        # avg gradient per example
        gradient = numpy.dot(x_trans, loss) / m
        # update
        theta = theta - alpha * gradient
    return theta


def gen_data(num_points, bias, variance):
    x = numpy.zeros(shape=(num_points, 2))
    y = numpy.zeros(shape=num_points)
    # basically a straight line
    for i in range(0, num_points):
        # bias feature
        x[i][0] = 1
        x[i][1] = i
        # our target variable
        y[i] = (i + bias) + random.uniform(0, 1) * variance
    return x, y

# gen 100 points with a bias of 25 and 10 variance as a bit of noise
x, y = gen_data(100, 25, 10)
m, n = numpy.shape(x)
numIterations = 100000
alpha = 0.0005
theta = numpy.ones(n)
theta = gradient_descent(x, y, theta, alpha, m, numIterations)
print(theta)


























import numpy
#trovare a priori i 500 punti piu vicini per ognuno nel training set

#calcolare la discesa del gradiente per diminuire l'errore di previsione dell'errore,
#pesando i valori di inumpyut del training set, quindi va calcolato il peso per ogni
#valore del training set al fine di diminuire l'errore.










cur_x = 3 # The algorithm starts at x=3
rate = 0.01 # Learning rate
precision = 0.000001 #This tells us when to stop the algorithm
previous_step_size = 1 #
max_iters = 10000 # maximum number of iterations
iters = 0 #iteration counter
df = lambda x: 2*(x+5) #Gradient of our functi

while previous_step_size > precision and iters < max_iters:
    prev_x = cur_x  # Store current x value in prev_x
    cur_x = cur_x - rate * df(prev_x)  # Grad descent
    previous_step_size = abs(cur_x - prev_x)  # Change in x
    iters = iters + 1  # iteration count
    print("Iteration", iters, "\nX value is", cur_x)  # Print iterations

print("The local minimum occurs at", cur_x)













def gradient_descent(x, y, theta, alpha, iters):
    m = len(y)
    j_history = numpy.matrix(numpy.zeros((iters, 1)))
    for i in range(iters):
        prediction = x*theta.T
        margin_error = prediction - y
        gradient = 1/m * (alpha * (x.T * margin_error))
        theta = theta - gradient.T
        j_history[i] = compute_cost(x, y, theta)

    return theta, j_history


def compute_cost(x, y, theta):
    m = len(y)
    # We get theta transpose because we are working with a numpy array [0,0] for example
    prediction = x * theta.T
    j = 1/(2*m) * numpy.sum(numpy.power((prediction - y), 2))
    return j