import machine

# Setup for noise sensor max9814
SAMPLE_WINDOW = 50  # sample window width in ms (50ms = 20Hz)
sample = 0
adc = machine.ADC(bits=10)  # ADC object
nmpin = adc.channel(pin='P16')  # analog pin on P16
chrono = machine.Timer.Chrono()  # timing object for measuring low pulse
