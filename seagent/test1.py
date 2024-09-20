import pypict.cmd

# Define the PICT input model as a string
# pict_input_text = """
# P0: 01, 02
# P1: 11, 12
# P2: 21, 22
# P3: 31, 32
# P4: 41, 42
# P5: 51, 52
# P6: 61, 62
# P7: 71, 72
# P8: 81, 82
# P9: 91, 92

# {P0, P1, P2, P3, P4, P5, P6, P7, P8, P9} @2
# """
pict_input_text = """
1986d600c928c547074999cd72968e1d:    8475fda6454b49c1a74585b05db588f3, 8d9299140c5e4d9aaa7ff5e268a9db46\nf140599cdf4140d50acc729531a484c7:    3eb7548d90c84599a676c886cf34fa7f, e80aed219421403784a4630401ed4234\ne53ccb0dcb614e075fa377bf91c98dfc:    b69a513d577e4b34a46a2b5012f36ed9, e861511bafe14f81afa5f8cdbf3d319e\n33b15f6a6cc0dd912b44503f987a29a2:    25cfb33bdecc47a8ad6aa6c9276110c1, 2e07a8d34f5f4616b2be88e47cbca516
"""
# /o:3

# Generate the test cases from the model
output = pypict.cmd.from_model(pict_input_text)



# Print the output
print(output)
print(len(output[1]))
