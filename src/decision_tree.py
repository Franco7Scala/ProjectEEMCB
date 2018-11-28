import numpy
import matplotlib.pyplot as plotter
from sklearn.tree import DecisionTreeRegressor


#TODO to complete


model = DecisionTreeRegressor(criterion="mse", min_samples_leaf=5)
model.fit(training_data.iloc[:, :-1], training_data.iloc[:, -1:])
# predict unseen query instances
predicted = model.predict(testing_data.iloc[:, :-1])
# compute and plot the RMSE
RMSE = numpy.sqrt(numpy.sum(((testing_data.iloc[:,-1]-predicted)**2)/len(testing_data.iloc[:,-1])))


fig = plotter.figure()
ax0 = fig.add_subplot(111)
RMSE_train = []
RMSE_test = []
for i in range(1, 100):
    # parametrize the model and let i be the number of minimum instances per leaf node
    regression_model = DecisionTreeRegressor(criterion="mse", min_samples_leaf=i)
    # train the model
    regression_model.fit(training_data.iloc[:, :-1], training_data.iloc[:, -1:])
    # predict query instances
    predicted_train = regression_model.predict(training_data.iloc[:, :-1])
    predicted_test = regression_model.predict(testing_data.iloc[:, :-1])
    # calculate and append the RMSEs
    RMSE_train.append(
        numpy.sqrt(numpy.sum(((training_data.iloc[:, -1] - predicted_train) ** 2) / len(training_data.iloc[:, -1]))))
    RMSE_test.append(
        numpy.sqrt(numpy.sum(((testing_data.iloc[:, -1] - predicted_test) ** 2) / len(testing_data.iloc[:, -1]))))

ax0.plot(range(1, 100), RMSE_test, label='Test_Data')
ax0.plot(range(1, 100), RMSE_train, label='Train_Data')
ax0.legend()
ax0.set_title('RMSE with respect to the minumim number of instances per node')
ax0.set_xlabel('#Instances')
ax0.set_ylabel('RMSE')
plotter.show()