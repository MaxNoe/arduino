# Live Plotting Anolog of the Inputs

This is using google's protobufs to transmit the data over the serial port.
You will need the google protobuf library to convert the `.proto` file to python 
and `pb` code.
On the arduino, the nanopb library is used. Put it in `~/Arduino/libraries/` so
the arduino IDE can find it.
Run make to generate the protobuf files and put `./adcvalues.pb.h` and
`adcvalues.pb.c` also into a directory in `~/Arduino/libraries/`


