all: adcvalues.pb.c adcvalues.pb.h adcvalues_pb2.py

adcvalues_pb2.py: adcvalues.proto
	protoc -I. --python_out=. adcvalues.proto

adcvalues.pb.c adcvalues.pb.h: adcvalues.pb
	~/Arduino/libraries/nanopb/generator/nanopb_generator.py \
		adcvalues.pb

adcvalues.pb: adcvalues.proto
	protoc -o adcvalues.pb adcvalues.proto
