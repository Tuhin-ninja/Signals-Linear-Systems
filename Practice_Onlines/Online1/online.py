import import_ipynb
import Discrete


degree1 = int(input("Degree of the first polynomial: "))
input_signal = Discrete.DiscreteSignal(10)
coeff1 = []
for i in range(degree1+1):
    # print("Enter the coefficient of x^", i)
    # coeff1.append(float(input()))
    input_signal.set_value_at_time(i, float(input("Enter the coefficient of x^"+str(-i+degree1)+": ")))

input_signal.shift_signal(2)
input_signal.plot("input signal")

degree2 = input("Degree of the second polynomial: ")
impulse_response = Discrete.DiscreteSignal(10)
# input("Coefficients : ")
# coeff2 = []
for i in range(degree2+1):
    # coeff2.append(float(input()))
    impulse_response.set_value_at_time(i, float(input()))
impulse_response.plot("impulse response")


