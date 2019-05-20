from __future__ import division
from sklearn.externals import joblib
import Parser
import Support
import warnings

#FRANCE

warnings.filterwarnings("ignore", category=DeprecationWarning)


detailed_verbose = 0
training = 1


if training == 1:
    path_output_production_0 = "/Users/francesco/Desktop/train_model_0.txt"
    path_output_production_1 = "/Users/francesco/Desktop/train_model_1.txt"
    path_output_production_2 = "/Users/francesco/Desktop/train_model_2.txt"
    path_output_production_3 = "/Users/francesco/Desktop/train_model_3.txt"
    path_output_production_4 = "/Users/francesco/Desktop/train_model_4.txt"
    path_output_production_5 = "/Users/francesco/Desktop/train_model_5.txt"
else:
    path_output_production_0 = "/Users/francesco/Desktop/test_model_0.txt"
    path_output_production_1 = "/Users/francesco/Desktop/test_model_1.txt"
    path_output_production_2 = "/Users/francesco/Desktop/test_model_2.txt"
    path_output_production_3 = "/Users/francesco/Desktop/test_model_3.txt"
    path_output_production_4 = "/Users/francesco/Desktop/test_model_4.txt"
    path_output_production_5 = "/Users/francesco/Desktop/test_model_5.txt"

file_output_production_0 = open(path_output_production_0, "w+")
file_output_production_1 = open(path_output_production_1, "w+")
file_output_production_2 = open(path_output_production_2, "w+")
file_output_production_3 = open(path_output_production_3, "w+")
file_output_production_4 = open(path_output_production_4, "w+")
file_output_production_5 = open(path_output_production_5, "w+")

nation = "FR"
path_predictor_production_0 = "/Users/francesco/Desktop/best/" + nation + "/model_0.joblib"
path_predictor_production_1 = "/Users/francesco/Desktop/best/" + nation + "/model_1.joblib"
path_predictor_production_2 = "/Users/francesco/Desktop/best/" + nation + "/model_2.joblib"
path_predictor_production_3 = "/Users/francesco/Desktop/best/" + nation + "/model_3.joblib"
path_predictor_production_4 = "/Users/francesco/Desktop/best/" + nation + "/model_4.joblib"
path_predictor_production_5 = "/Users/francesco/Desktop/best/" + nation + "/model_5.joblib"


if training == 1:
    path_data_rf = "/Users/francesco/Desktop/dataset/" + nation + "/training_set_rf.txt"
    path_data_wpwl = "/Users/francesco/Desktop/dataset/" + nation + "/training_set_wpwl.txt"
else:
    path_data_rf = "/Users/francesco/Desktop/dataset/" + nation + "/test_set_rf.txt"
    path_data_wpwl = "/Users/francesco/Desktop/dataset/" + nation + "/test_set_wpwl.txt"

input_rf, expected_outputs_rf, input_size_rf, output_size_rf = Parser.parse_data(path_data_rf, 0)
input_wpwl, expected_outputs_wpwl, input_size_wpwl, output_size_wpwl = Parser.parse_data(path_data_wpwl, 0)

samples_quantity,_ = input_rf.shape

output_quantity_rf = len(expected_outputs_rf[0])
output_quantity_wpwl = len(expected_outputs_wpwl[0])

model_production_0 = joblib.load(path_predictor_production_0)
model_production_1 = joblib.load(path_predictor_production_1)
model_production_2 = joblib.load(path_predictor_production_2)
model_production_3 = joblib.load(path_predictor_production_3)
model_production_4 = joblib.load(path_predictor_production_4)
#model_production_5 = joblib.load(path_predictor_production_5)

# verifying
sum_relative_error_model = 0
for sample_selected in range(0, samples_quantity):
    expected_output_0 = expected_outputs_rf[sample_selected][0] #qui
    expected_output_1 = expected_outputs_rf[sample_selected][1]
    expected_output_2 = expected_outputs_wpwl[sample_selected][2]
    expected_output_3 = expected_outputs_wpwl[sample_selected][3]
    expected_output_4 = expected_outputs_rf[sample_selected][4]
    #expected_output_5 = expected_outputs_rf[sample_selected][5]

    real_output_production_0 = model_production_0.predict(input_rf[sample_selected].reshape(1, -1)) #qui
    real_output_production_1 = model_production_1.predict(input_rf[sample_selected].reshape(1, -1))
    real_output_production_2 = model_production_2.predict(input_wpwl[sample_selected].reshape(1, -1))
    real_output_production_3 = model_production_3.predict(input_wpwl[sample_selected].reshape(1, -1))
    real_output_production_4 = model_production_4.predict(input_rf[sample_selected].reshape(1, -1))
    #real_output_production_5 = model_production_5.predict(input_rf[sample_selected].reshape(1, -1))

    if detailed_verbose != 0:
        Support.colored_print("-------------------------------------------", "blue")
        Support.colored_print("model output 0: " + str(real_output_production_0) + " expected: " + str(expected_output_0), "green")
        Support.colored_print("model output 1: " + str(real_output_production_1) + " expected: " + str(expected_output_1), "green")
        Support.colored_print("model output 2: " + str(real_output_production_2) + " expected: " + str(expected_output_2), "green")
        Support.colored_print("model output 3: " + str(real_output_production_3) + " expected: " + str(expected_output_3), "green")
        Support.colored_print("model output 4: " + str(real_output_production_4) + " expected: " + str(expected_output_4), "green")
        #Support.colored_print("model output 5: " + str(real_output_production_5) + " expected: " + str(expected_output_5), "green")

    relative_error_production_0 = Support.calculate_relative_error(real_output_production_0, expected_output_0)
    relative_error_production_1 = Support.calculate_relative_error(real_output_production_1, expected_output_1)
    relative_error_production_2 = Support.calculate_relative_error(real_output_production_2, expected_output_2)
    relative_error_production_3 = Support.calculate_relative_error(real_output_production_3, expected_output_3)
    relative_error_production_4 = Support.calculate_relative_error(real_output_production_4, expected_output_4)
    #relative_error_production_5 = Support.calculate_relative_error(real_output_production_5, expected_output_5)

    for current_input in range(0, len(input_rf[sample_selected])):
        file_output_production_0.write("%f " % input_wpwl[sample_selected][current_input])  # qui
        file_output_production_1.write("%f " % input_rf[sample_selected][current_input]) #qui
        file_output_production_4.write("%f " % input_rf[sample_selected][current_input])
        #file_output_production_5.write("%f " % input_rf[sample_selected][current_input])

    for current_input in range(0, len(input_wpwl[sample_selected])):
        file_output_production_2.write("%f " % input_wpwl[sample_selected][current_input])
        file_output_production_3.write("%f " % input_wpwl[sample_selected][current_input])


    file_output_production_0.write("= %lf" % (relative_error_production_0 * 100))
    file_output_production_1.write("= %lf" % (relative_error_production_1 * 100))
    file_output_production_2.write("= %lf" % (relative_error_production_2 * 100))
    file_output_production_3.write("= %lf" % (relative_error_production_3 * 100))
    file_output_production_4.write("= %lf" % (relative_error_production_4 * 100))
    #file_output_production_5.write("= %lf" % (relative_error_production_5 * 100))

    file_output_production_0.write("\n")
    file_output_production_1.write("\n")
    file_output_production_2.write("\n")
    file_output_production_3.write("\n")
    file_output_production_4.write("\n")
    #file_output_production_5.write("\n")

file_output_production_0.close()
file_output_production_1.close()
file_output_production_2.close()
file_output_production_3.close()
file_output_production_4.close()
#file_output_production_5.close()

# end
Support.colored_print("Done!", "pink")


#SWITZERLAND

from __future__ import division
from sklearn.externals import joblib
import Parser
import Support
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)


detailed_verbose = 0
training = 1


if training == 1:
    path_output_production_0 = "/Users/francesco/Desktop/train_model_0.txt"
    path_output_production_1 = "/Users/francesco/Desktop/train_model_1.txt"
    path_output_production_2 = "/Users/francesco/Desktop/train_model_2.txt"
    path_output_production_3 = "/Users/francesco/Desktop/train_model_3.txt"
    path_output_production_4 = "/Users/francesco/Desktop/train_model_4.txt"
    path_output_production_5 = "/Users/francesco/Desktop/train_model_5.txt"
else:
    path_output_production_0 = "/Users/francesco/Desktop/test_model_0.txt"
    path_output_production_1 = "/Users/francesco/Desktop/test_model_1.txt"
    path_output_production_2 = "/Users/francesco/Desktop/test_model_2.txt"
    path_output_production_3 = "/Users/francesco/Desktop/test_model_3.txt"
    path_output_production_4 = "/Users/francesco/Desktop/test_model_4.txt"
    path_output_production_5 = "/Users/francesco/Desktop/test_model_5.txt"

file_output_production_0 = open(path_output_production_0, "w+")
file_output_production_1 = open(path_output_production_1, "w+")
file_output_production_2 = open(path_output_production_2, "w+")
file_output_production_3 = open(path_output_production_3, "w+")
file_output_production_4 = open(path_output_production_4, "w+")
file_output_production_5 = open(path_output_production_5, "w+")

nation = "CH"
path_predictor_production_0 = "/Users/francesco/Desktop/best/" + nation + "/model_0.joblib"
path_predictor_production_1 = "/Users/francesco/Desktop/best/" + nation + "/model_1.joblib"
path_predictor_production_2 = "/Users/francesco/Desktop/best/" + nation + "/model_2.joblib"
path_predictor_production_3 = "/Users/francesco/Desktop/best/" + nation + "/model_3.joblib"
path_predictor_production_4 = "/Users/francesco/Desktop/best/" + nation + "/model_4.joblib"
path_predictor_production_5 = "/Users/francesco/Desktop/best/" + nation + "/model_5.joblib"


if training == 1:
    path_data_rf = "/Users/francesco/Desktop/dataset/" + nation + "/training_set_rf.txt"
    path_data_wpwl = "/Users/francesco/Desktop/dataset/" + nation + "/training_set_wpwl.txt"
else:
    path_data_rf = "/Users/francesco/Desktop/dataset/" + nation + "/test_set_rf.txt"
    path_data_wpwl = "/Users/francesco/Desktop/dataset/" + nation + "/test_set_wpwl.txt"

input_rf, expected_outputs_rf, input_size_rf, output_size_rf = Parser.parse_data(path_data_rf, 0)
input_wpwl, expected_outputs_wpwl, input_size_wpwl, output_size_wpwl = Parser.parse_data(path_data_wpwl, 0)

samples_quantity,_ = input_rf.shape

output_quantity_rf = len(expected_outputs_rf[0])
output_quantity_wpwl = len(expected_outputs_wpwl[0])

model_production_0 = joblib.load(path_predictor_production_0)
#model_production_1 = joblib.load(path_predictor_production_1)
#model_production_2 = joblib.load(path_predictor_production_2)
#model_production_3 = joblib.load(path_predictor_production_3)
#model_production_4 = joblib.load(path_predictor_production_4)
#model_production_5 = joblib.load(path_predictor_production_5)

# verifying
sum_relative_error_model = 0
for sample_selected in range(0, samples_quantity):
    expected_output_0 = expected_outputs_wpwl[sample_selected][0] #qui
    #expected_output_1 = expected_outputs_rf[sample_selected][1]
    #expected_output_2 = expected_outputs_wpwl[sample_selected][2]
    #expected_output_3 = expected_outputs_wpwl[sample_selected][3]
    #expected_output_4 = expected_outputs_rf[sample_selected][4]
    #expected_output_5 = expected_outputs_rf[sample_selected][5]

    real_output_production_0 = model_production_0.predict(input_wpwl[sample_selected].reshape(1, -1)) #qui
    #real_output_production_1 = model_production_1.predict(input_rf[sample_selected].reshape(1, -1))
    #real_output_production_2 = model_production_2.predict(input_wpwl[sample_selected].reshape(1, -1))
    #real_output_production_3 = model_production_3.predict(input_wpwl[sample_selected].reshape(1, -1))
    #real_output_production_4 = model_production_4.predict(input_rf[sample_selected].reshape(1, -1))
    #real_output_production_5 = model_production_5.predict(input_rf[sample_selected].reshape(1, -1))

    if detailed_verbose != 0:
        Support.colored_print("-------------------------------------------", "blue")
        Support.colored_print("model output 0: " + str(real_output_production_0) + " expected: " + str(expected_output_0), "green")
        #Support.colored_print("model output 1: " + str(real_output_production_1) + " expected: " + str(expected_output_1), "green")
        #Support.colored_print("model output 2: " + str(real_output_production_2) + " expected: " + str(expected_output_2), "green")
        #Support.colored_print("model output 3: " + str(real_output_production_3) + " expected: " + str(expected_output_3), "green")
        #Support.colored_print("model output 4: " + str(real_output_production_4) + " expected: " + str(expected_output_4), "green")
        #Support.colored_print("model output 5: " + str(real_output_production_5) + " expected: " + str(expected_output_5), "green")

    relative_error_production_0 = Support.calculate_relative_error(real_output_production_0, expected_output_0)
    #relative_error_production_1 = Support.calculate_relative_error(real_output_production_1, expected_output_1)
    #relative_error_production_2 = Support.calculate_relative_error(real_output_production_2, expected_output_2)
    #relative_error_production_3 = Support.calculate_relative_error(real_output_production_3, expected_output_3)
    #relative_error_production_4 = Support.calculate_relative_error(real_output_production_4, expected_output_4)
    #relative_error_production_5 = Support.calculate_relative_error(real_output_production_5, expected_output_5)

   # for current_input in range(0, len(input_rf[sample_selected])):
        #file_output_production_0.write("%f " % input_rf[sample_selected][current_input])  # qui
        #file_output_production_1.write("%f " % input_rf[sample_selected][current_input]) #qui
        #file_output_production_4.write("%f " % input_rf[sample_selected][current_input])
        #file_output_production_5.write("%f " % input_rf[sample_selected][current_input])

    for current_input in range(0, len(input_wpwl[sample_selected])):
        file_output_production_0.write("%f " % input_wpwl[sample_selected][current_input])  # qui
        #file_output_production_2.write("%f " % input_wpwl[sample_selected][current_input])
        #file_output_production_3.write("%f " % input_wpwl[sample_selected][current_input])


    file_output_production_0.write("= %lf" % (relative_error_production_0 * 100))
    #file_output_production_1.write("= %lf" % (relative_error_production_1 * 100))
    #file_output_production_2.write("= %lf" % (relative_error_production_2 * 100))
    #file_output_production_3.write("= %lf" % (relative_error_production_3 * 100))
    #file_output_production_4.write("= %lf" % (relative_error_production_4 * 100))
    #file_output_production_5.write("= %lf" % (relative_error_production_5 * 100))

    #file_output_production_0.write("\n")
    #file_output_production_1.write("\n")
    #file_output_production_2.write("\n")
    #file_output_production_3.write("\n")
    #file_output_production_4.write("\n")
    #file_output_production_5.write("\n")

file_output_production_0.close()
file_output_production_1.close()
file_output_production_2.close()
file_output_production_3.close()
file_output_production_4.close()
#file_output_production_5.close()

# end
Support.colored_print("Done!", "pink")



#GERMANY

from __future__ import division
from sklearn.externals import joblib
import Parser
import Support
import warnings


warnings.filterwarnings("ignore", category=DeprecationWarning)


detailed_verbose = 0
training = 1


if training == 1:
    path_output_production_0 = "/Users/francesco/Desktop/train_model_0.txt"
    path_output_production_1 = "/Users/francesco/Desktop/train_model_1.txt"
    path_output_production_2 = "/Users/francesco/Desktop/train_model_2.txt"
    path_output_production_3 = "/Users/francesco/Desktop/train_model_3.txt"
    path_output_production_4 = "/Users/francesco/Desktop/train_model_4.txt"
    path_output_production_5 = "/Users/francesco/Desktop/train_model_5.txt"
    path_output_production_6 = "/Users/francesco/Desktop/train_model_6.txt"
else:
    path_output_production_0 = "/Users/francesco/Desktop/test_model_0.txt"
    path_output_production_1 = "/Users/francesco/Desktop/test_model_1.txt"
    path_output_production_2 = "/Users/francesco/Desktop/test_model_2.txt"
    path_output_production_3 = "/Users/francesco/Desktop/test_model_3.txt"
    path_output_production_4 = "/Users/francesco/Desktop/test_model_4.txt"
    path_output_production_5 = "/Users/francesco/Desktop/test_model_5.txt"
    path_output_production_6 = "/Users/francesco/Desktop/test_model_6.txt"

file_output_production_0 = open(path_output_production_0, "w+")
file_output_production_1 = open(path_output_production_1, "w+")
file_output_production_2 = open(path_output_production_2, "w+")
file_output_production_3 = open(path_output_production_3, "w+")
file_output_production_4 = open(path_output_production_4, "w+")
file_output_production_5 = open(path_output_production_5, "w+")
file_output_production_6 = open(path_output_production_6, "w+")

nation = "DE"
path_predictor_production_0 = "/Users/francesco/Desktop/best/" + nation + "/model_0.joblib"
path_predictor_production_1 = "/Users/francesco/Desktop/best/" + nation + "/model_1.joblib"
path_predictor_production_2 = "/Users/francesco/Desktop/best/" + nation + "/model_2.joblib"
path_predictor_production_3 = "/Users/francesco/Desktop/best/" + nation + "/model_3.joblib"
path_predictor_production_4 = "/Users/francesco/Desktop/best/" + nation + "/model_4.joblib"
path_predictor_production_5 = "/Users/francesco/Desktop/best/" + nation + "/model_5.joblib"
path_predictor_production_6 = "/Users/francesco/Desktop/best/" + nation + "/model_6.joblib"


if training == 1:
    path_data_rf = "/Users/francesco/Desktop/dataset/" + nation + "/training_set_rf.txt"
    path_data_wpwl = "/Users/francesco/Desktop/dataset/" + nation + "/training_set_wpwl.txt"
else:
    path_data_rf = "/Users/francesco/Desktop/dataset/" + nation + "/test_set_rf.txt"
    path_data_wpwl = "/Users/francesco/Desktop/dataset/" + nation + "/test_set_wpwl.txt"

input_rf, expected_outputs_rf, input_size_rf, output_size_rf = Parser.parse_data(path_data_rf, 0)
input_wpwl, expected_outputs_wpwl, input_size_wpwl, output_size_wpwl = Parser.parse_data(path_data_wpwl, 0)

samples_quantity,_ = input_rf.shape

output_quantity_rf = len(expected_outputs_rf[0])
output_quantity_wpwl = len(expected_outputs_wpwl[0])

model_production_0 = joblib.load(path_predictor_production_0)
model_production_1 = joblib.load(path_predictor_production_1)
model_production_2 = joblib.load(path_predictor_production_2)
model_production_3 = joblib.load(path_predictor_production_3)
model_production_4 = joblib.load(path_predictor_production_4)
model_production_5 = joblib.load(path_predictor_production_5)
model_production_6 = joblib.load(path_predictor_production_6)

# verifying
sum_relative_error_model = 0
for sample_selected in range(0, samples_quantity):
    expected_output_0 = expected_outputs_rf[sample_selected][0] #qui
    expected_output_1 = expected_outputs_wpwl[sample_selected][1]
    expected_output_2 = expected_outputs_rf[sample_selected][2]
    expected_output_3 = expected_outputs_rf[sample_selected][3]
    expected_output_4 = expected_outputs_rf[sample_selected][4]
    expected_output_5 = expected_outputs_rf[sample_selected][5]
    expected_output_6 = expected_outputs_rf[sample_selected][6]

    real_output_production_0 = model_production_0.predict(input_rf[sample_selected].reshape(1, -1)) #qui
    real_output_production_1 = model_production_1.predict(input_wpwl[sample_selected].reshape(1, -1))
    real_output_production_2 = model_production_2.predict(input_rf[sample_selected].reshape(1, -1))
    real_output_production_3 = model_production_3.predict(input_rf[sample_selected].reshape(1, -1))
    real_output_production_4 = model_production_4.predict(input_rf[sample_selected].reshape(1, -1))
    real_output_production_5 = model_production_5.predict(input_rf[sample_selected].reshape(1, -1))
    real_output_production_6 = model_production_6.predict(input_rf[sample_selected].reshape(1, -1))

    if detailed_verbose != 0:
        Support.colored_print("-------------------------------------------", "blue")
        Support.colored_print("model output 0: " + str(real_output_production_0) + " expected: " + str(expected_output_0), "green")
        Support.colored_print("model output 1: " + str(real_output_production_1) + " expected: " + str(expected_output_1), "green")
        Support.colored_print("model output 2: " + str(real_output_production_2) + " expected: " + str(expected_output_2), "green")
        Support.colored_print("model output 3: " + str(real_output_production_3) + " expected: " + str(expected_output_3), "green")
        Support.colored_print("model output 4: " + str(real_output_production_4) + " expected: " + str(expected_output_4), "green")
        #Support.colored_print("model output 5: " + str(real_output_production_5) + " expected: " + str(expected_output_5), "green")

    relative_error_production_0 = Support.calculate_relative_error(real_output_production_0, expected_output_0)
    relative_error_production_1 = Support.calculate_relative_error(real_output_production_1, expected_output_1)
    relative_error_production_2 = Support.calculate_relative_error(real_output_production_2, expected_output_2)
    relative_error_production_3 = Support.calculate_relative_error(real_output_production_3, expected_output_3)
    relative_error_production_4 = Support.calculate_relative_error(real_output_production_4, expected_output_4)
    relative_error_production_5 = Support.calculate_relative_error(real_output_production_5, expected_output_5)
    relative_error_production_6 = Support.calculate_relative_error(real_output_production_6, expected_output_6)

    for current_input in range(0, len(input_rf[sample_selected])):
        file_output_production_0.write("%f " % input_rf[sample_selected][current_input])  # qui
        file_output_production_2.write("%f " % input_rf[sample_selected][current_input])
        file_output_production_3.write("%f " % input_rf[sample_selected][current_input])
        file_output_production_4.write("%f " % input_rf[sample_selected][current_input])
        file_output_production_5.write("%f " % input_rf[sample_selected][current_input])
        file_output_production_6.write("%f " % input_rf[sample_selected][current_input])

    for current_input in range(0, len(input_wpwl[sample_selected])):
        file_output_production_1.write("%f " % input_wpwl[sample_selected][current_input]) #qui



    file_output_production_0.write("= %lf" % (relative_error_production_0 * 100))
    file_output_production_1.write("= %lf" % (relative_error_production_1 * 100))
    file_output_production_2.write("= %lf" % (relative_error_production_2 * 100))
    file_output_production_3.write("= %lf" % (relative_error_production_3 * 100))
    file_output_production_4.write("= %lf" % (relative_error_production_4 * 100))
    file_output_production_5.write("= %lf" % (relative_error_production_5 * 100))
    file_output_production_6.write("= %lf" % (relative_error_production_6 * 100))

    file_output_production_0.write("\n")
    file_output_production_1.write("\n")
    file_output_production_2.write("\n")
    file_output_production_3.write("\n")
    file_output_production_4.write("\n")
    file_output_production_5.write("\n")
    file_output_production_6.write("\n")

file_output_production_0.close()
file_output_production_1.close()
file_output_production_2.close()
file_output_production_3.close()
file_output_production_4.close()
file_output_production_5.close()
file_output_production_6.close()

# end
Support.colored_print("Done!", "pink")

#NLLLLLL



from __future__ import division
from sklearn.externals import joblib
import Parser
import Support
import warnings


warnings.filterwarnings("ignore", category=DeprecationWarning)


detailed_verbose = 0
training = 1


if training == 1:
    path_output_production_0 = "/Users/francesco/Desktop/train_model_0.txt"
    path_output_production_1 = "/Users/francesco/Desktop/train_model_1.txt"
else:
    path_output_production_0 = "/Users/francesco/Desktop/test_model_0.txt"
    path_output_production_1 = "/Users/francesco/Desktop/test_model_1.txt"

file_output_production_0 = open(path_output_production_0, "w+")
file_output_production_1 = open(path_output_production_1, "w+")


nation = "NL"
path_predictor_production_0 = "/Users/francesco/Desktop/best/" + nation + "/model_0.joblib"
path_predictor_production_1 = "/Users/francesco/Desktop/best/" + nation + "/model_1.joblib"



if training == 1:
    path_data_rf = "/Users/francesco/Desktop/dataset/" + nation + "/training_set_rf.txt"
    path_data_wpwl = "/Users/francesco/Desktop/dataset/" + nation + "/training_set_wpwl.txt"
else:
    path_data_rf = "/Users/francesco/Desktop/dataset/" + nation + "/test_set_rf.txt"
    path_data_wpwl = "/Users/francesco/Desktop/dataset/" + nation + "/test_set_wpwl.txt"

input_rf, expected_outputs_rf, input_size_rf, output_size_rf = Parser.parse_data(path_data_rf, 0)
input_wpwl, expected_outputs_wpwl, input_size_wpwl, output_size_wpwl = Parser.parse_data(path_data_wpwl, 0)

samples_quantity,_ = input_rf.shape

output_quantity_rf = len(expected_outputs_rf[0])
output_quantity_wpwl = len(expected_outputs_wpwl[0])

model_production_0 = joblib.load(path_predictor_production_0)
model_production_1 = joblib.load(path_predictor_production_1)


# verifying
sum_relative_error_model = 0
for sample_selected in range(0, samples_quantity):
    expected_output_0 = expected_outputs_rf[sample_selected][0] #qui
    expected_output_1 = expected_outputs_rf[sample_selected][1]


    real_output_production_0 = model_production_0.predict(input_rf[sample_selected].reshape(1, -1)) #qui
    real_output_production_1 = model_production_1.predict(input_rf[sample_selected].reshape(1, -1))


    if detailed_verbose != 0:
        Support.colored_print("-------------------------------------------", "blue")
        Support.colored_print("model output 0: " + str(real_output_production_0) + " expected: " + str(expected_output_0), "green")
        Support.colored_print("model output 1: " + str(real_output_production_1) + " expected: " + str(expected_output_1), "green")


    relative_error_production_0 = Support.calculate_relative_error(real_output_production_0, expected_output_0)
    relative_error_production_1 = Support.calculate_relative_error(real_output_production_1, expected_output_1)


    for current_input in range(0, len(input_rf[sample_selected])):
        file_output_production_0.write("%f " % input_rf[sample_selected][current_input])  # qui
        file_output_production_1.write("%f " % input_rf[sample_selected][current_input])


    for current_input in range(0, len(input_wpwl[sample_selected])):
        pass



    file_output_production_0.write("= %lf" % (relative_error_production_0 * 100))
    file_output_production_1.write("= %lf" % (relative_error_production_1 * 100))

    file_output_production_0.write("\n")
    file_output_production_1.write("\n")

file_output_production_0.close()
file_output_production_1.close()


# end
Support.colored_print("Done!", "pink")




from __future__ import division
from sklearn.externals import joblib
import Parser
import Support
import warnings

#BELGIUM

warnings.filterwarnings("ignore", category=DeprecationWarning)


detailed_verbose = 0
training = 1


if training == 1:
    path_output_production_0 = "/Users/francesco/Desktop/train_model_0.txt"
    path_output_production_1 = "/Users/francesco/Desktop/train_model_1.txt"
    path_output_production_2 = "/Users/francesco/Desktop/train_model_2.txt"
    path_output_production_3 = "/Users/francesco/Desktop/train_model_3.txt"
    path_output_production_4 = "/Users/francesco/Desktop/train_model_4.txt"
    path_output_production_5 = "/Users/francesco/Desktop/train_model_5.txt"
else:
    path_output_production_0 = "/Users/francesco/Desktop/test_model_0.txt"
    path_output_production_1 = "/Users/francesco/Desktop/test_model_1.txt"
    path_output_production_2 = "/Users/francesco/Desktop/test_model_2.txt"
    path_output_production_3 = "/Users/francesco/Desktop/test_model_3.txt"
    path_output_production_4 = "/Users/francesco/Desktop/test_model_4.txt"
    path_output_production_5 = "/Users/francesco/Desktop/test_model_5.txt"

file_output_production_0 = open(path_output_production_0, "w+")
file_output_production_1 = open(path_output_production_1, "w+")
file_output_production_2 = open(path_output_production_2, "w+")
file_output_production_3 = open(path_output_production_3, "w+")
file_output_production_4 = open(path_output_production_4, "w+")
file_output_production_5 = open(path_output_production_5, "w+")

nation = "BE"
path_predictor_production_0 = "/Users/francesco/Desktop/best/" + nation + "/model_0.joblib"
path_predictor_production_3 = "/Users/francesco/Desktop/best/" + nation + "/model_3.joblib"
path_predictor_production_5 = "/Users/francesco/Desktop/best/" + nation + "/model_5.joblib"


if training == 1:
    path_data_rf = "/Users/francesco/Desktop/dataset/" + nation + "/training_set_wp.txt"
    path_data_wpwl = "/Users/francesco/Desktop/dataset/" + nation + "/training_set_wpaw.txt"
else:
    path_data_rf = "/Users/francesco/Desktop/dataset/" + nation + "/test_set_wp.txt"
    path_data_wpwl = "/Users/francesco/Desktop/dataset/" + nation + "/test_set_wpaw.txt"

input_wp, expected_outputs_wp, input_size_rf, output_size_rf = Parser.parse_data(path_data_rf, 0)
input_wpaw, expected_outputs_wpaw, input_size_wpwl, output_size_wpwl = Parser.parse_data(path_data_wpwl, 0)

samples_quantity,_ = input_wp.shape

output_quantity_rf = len(expected_outputs_wp[0])
output_quantity_wpwl = len(expected_outputs_wpaw[0])

model_production_0 = joblib.load(path_predictor_production_0)
model_production_3 = joblib.load(path_predictor_production_3)
model_production_5 = joblib.load(path_predictor_production_5)

# verifying
sum_relative_error_model = 0
for sample_selected in range(0, samples_quantity):
    expected_output_0 = expected_outputs_wpaw[sample_selected][0] #qui
    expected_output_1 = expected_outputs_wp[sample_selected][1]
    expected_output_2 = expected_outputs_wp[sample_selected][2]
    expected_output_3 = expected_outputs_wp[sample_selected][3]
    expected_output_4 = expected_outputs_wp[sample_selected][4]
    expected_output_5 = expected_outputs_wp[sample_selected][5]

    real_output_production_0 = model_production_0.predict(input_wpaw[sample_selected].reshape(1, -1)) #qui
    real_output_production_3 = model_production_3.predict(input_wp[sample_selected].reshape(1, -1))
    real_output_production_5 = model_production_5.predict(input_wpaw[sample_selected].reshape(1, -1))

    if detailed_verbose != 0:
        Support.colored_print("-------------------------------------------", "blue")
        Support.colored_print("model output 0: " + str(real_output_production_0) + " expected: " + str(expected_output_0), "green")
        Support.colored_print("model output 3: " + str(real_output_production_3) + " expected: " + str(expected_output_3), "green")
        #Support.colored_print("model output 5: " + str(real_output_production_5) + " expected: " + str(expected_output_5), "green")

    relative_error_production_0 = Support.calculate_relative_error(real_output_production_0, expected_output_0)
    relative_error_production_3 = Support.calculate_relative_error(real_output_production_3, expected_output_3)
    relative_error_production_5 = Support.calculate_relative_error(real_output_production_5, expected_output_5)

    for current_input in range(0, len(input_wp[sample_selected])):
        file_output_production_3.write("%f " % input_wp[sample_selected][current_input]) #qui

    for current_input in range(0, len(input_wpaw[sample_selected])):
        file_output_production_0.write("%f " % input_wpaw[sample_selected][current_input])  # qui
        file_output_production_5.write("%f " % input_wpaw[sample_selected][current_input])

    file_output_production_0.write("= %lf" % (relative_error_production_0 * 100))
    file_output_production_3.write("= %lf" % (relative_error_production_3 * 100))
    file_output_production_5.write("= %lf" % (relative_error_production_5 * 100))

    file_output_production_0.write("\n")
    file_output_production_3.write("\n")
    file_output_production_5.write("\n")

file_output_production_0.close()
file_output_production_1.close()
file_output_production_2.close()
file_output_production_3.close()
file_output_production_4.close()
file_output_production_5.close()

# end
Support.colored_print("Done!", "pink")


#GERMANY

from __future__ import division
from sklearn.externals import joblib
import Parser
import Support
import warnings


warnings.filterwarnings("ignore", category=DeprecationWarning)


detailed_verbose = 0
training = 1


if training == 1:
    path_output_production_0 = "/Users/francesco/Desktop/train_model_0.txt"
    path_output_production_1 = "/Users/francesco/Desktop/train_model_1.txt"
    path_output_production_2 = "/Users/francesco/Desktop/train_model_2.txt"
    path_output_production_3 = "/Users/francesco/Desktop/train_model_3.txt"
    path_output_production_4 = "/Users/francesco/Desktop/train_model_4.txt"
    path_output_production_5 = "/Users/francesco/Desktop/train_model_5.txt"
    path_output_production_6 = "/Users/francesco/Desktop/train_model_6.txt"
else:
    path_output_production_0 = "/Users/francesco/Desktop/test_model_0.txt"
    path_output_production_1 = "/Users/francesco/Desktop/test_model_1.txt"
    path_output_production_2 = "/Users/francesco/Desktop/test_model_2.txt"
    path_output_production_3 = "/Users/francesco/Desktop/test_model_3.txt"
    path_output_production_4 = "/Users/francesco/Desktop/test_model_4.txt"
    path_output_production_5 = "/Users/francesco/Desktop/test_model_5.txt"
    path_output_production_6 = "/Users/francesco/Desktop/test_model_6.txt"

file_output_production_0 = open(path_output_production_0, "w+")
file_output_production_1 = open(path_output_production_1, "w+")
file_output_production_2 = open(path_output_production_2, "w+")
file_output_production_3 = open(path_output_production_3, "w+")
file_output_production_4 = open(path_output_production_4, "w+")
file_output_production_5 = open(path_output_production_5, "w+")
file_output_production_6 = open(path_output_production_6, "w+")

nation = "DE"
path_predictor_production_0 = "/Users/francesco/Desktop/best/" + nation + "/model_0.joblib"
path_predictor_production_1 = "/Users/francesco/Desktop/best/" + nation + "/model_1.joblib"
path_predictor_production_2 = "/Users/francesco/Desktop/best/" + nation + "/model_2.joblib"
path_predictor_production_3 = "/Users/francesco/Desktop/best/" + nation + "/model_3.joblib"
path_predictor_production_4 = "/Users/francesco/Desktop/best/" + nation + "/model_4.joblib"
path_predictor_production_5 = "/Users/francesco/Desktop/best/" + nation + "/model_5.joblib"
path_predictor_production_6 = "/Users/francesco/Desktop/best/" + nation + "/model_6.joblib"


if training == 1:
    path_data_rf = "/Users/francesco/Desktop/dataset/" + nation + "/training_set_wp.txt"
    path_data_wpwl = "/Users/francesco/Desktop/dataset/" + nation + "/training_set_wpaw.txt"
else:
    path_data_rf = "/Users/francesco/Desktop/dataset/" + nation + "/test_set_wp.txt"
    path_data_wpwl = "/Users/francesco/Desktop/dataset/" + nation + "/test_set_wpaw.txt"

input_wp, expected_outputs_wp, input_size_rf, output_size_rf = Parser.parse_data(path_data_rf, 0)
input_wpaw, expected_outputs_wpaw, input_size_wpwl, output_size_wpwl = Parser.parse_data(path_data_wpwl, 0)

samples_quantity,_ = input_wp.shape

output_quantity_wp = len(expected_outputs_wp[0])
output_quantity_wpaw = len(expected_outputs_wpaw[0])

model_production_0 = joblib.load(path_predictor_production_0)
model_production_1 = joblib.load(path_predictor_production_1)
model_production_3 = joblib.load(path_predictor_production_3)
model_production_4 = joblib.load(path_predictor_production_4)


# verifying
sum_relative_error_model = 0
for sample_selected in range(0, samples_quantity):
    expected_output_0 = expected_outputs_wp[sample_selected][0] #qui
    expected_output_1 = expected_outputs_wpaw[sample_selected][1]
    expected_output_3 = expected_outputs_wp[sample_selected][3]
    expected_output_4 = expected_outputs_wp[sample_selected][4]


    real_output_production_0 = model_production_0.predict(input_wp[sample_selected].reshape(1, -1)) #qui
    real_output_production_1 = model_production_1.predict(input_wpaw[sample_selected].reshape(1, -1))
    real_output_production_3 = model_production_3.predict(input_wp[sample_selected].reshape(1, -1))
    real_output_production_4 = model_production_4.predict(input_wp[sample_selected].reshape(1, -1))

    if detailed_verbose != 0:
        Support.colored_print("-------------------------------------------", "blue")
        Support.colored_print("model output 0: " + str(real_output_production_0) + " expected: " + str(expected_output_0), "green")
        Support.colored_print("model output 1: " + str(real_output_production_1) + " expected: " + str(expected_output_1), "green")
        Support.colored_print("model output 3: " + str(real_output_production_3) + " expected: " + str(expected_output_3), "green")
        Support.colored_print("model output 4: " + str(real_output_production_4) + " expected: " + str(expected_output_4), "green")
        #Support.colored_print("model output 5: " + str(real_output_production_5) + " expected: " + str(expected_output_5), "green")

    relative_error_production_0 = Support.calculate_relative_error(real_output_production_0, expected_output_0)
    relative_error_production_1 = Support.calculate_relative_error(real_output_production_1, expected_output_1)
    relative_error_production_3 = Support.calculate_relative_error(real_output_production_3, expected_output_3)
    relative_error_production_4 = Support.calculate_relative_error(real_output_production_4, expected_output_4)

    for current_input in range(0, len(input_wp[sample_selected])):
        file_output_production_0.write("%f " % input_wp[sample_selected][current_input])  # qui
        file_output_production_3.write("%f " % input_wp[sample_selected][current_input])
        file_output_production_4.write("%f " % input_wp[sample_selected][current_input])


    for current_input in range(0, len(input_wpaw[sample_selected])):
        file_output_production_1.write("%f " % input_wpaw[sample_selected][current_input])  # qui



    file_output_production_0.write("= %lf" % (relative_error_production_0 * 100))
    file_output_production_1.write("= %lf" % (relative_error_production_1 * 100))
    file_output_production_3.write("= %lf" % (relative_error_production_3 * 100))
    file_output_production_4.write("= %lf" % (relative_error_production_4 * 100))

    file_output_production_0.write("\n")
    file_output_production_1.write("\n")
    file_output_production_2.write("\n")
    file_output_production_3.write("\n")
    file_output_production_4.write("\n")
    file_output_production_5.write("\n")
    file_output_production_6.write("\n")

file_output_production_0.close()
file_output_production_1.close()
file_output_production_2.close()
file_output_production_3.close()
file_output_production_4.close()
file_output_production_5.close()
file_output_production_6.close()

# end
Support.colored_print("Done!", "pink")
