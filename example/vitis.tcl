# Create a project with a proper name
open_component -reset project_name -flow_target vivado

# Add design files
add_files test.cpp
# Add test bench (could be the same file as the design)
add_files -tb test.cpp
# Set the top-level function
set_top top

# Define the FPGA board - not important
set_part  {xcvu9p-flga2104-2-i}
# Define the clock rate in ns
create_clock -period 4

# Simulate your design in C
csim_design
# Translate your design to RTL
csynth_design
# Run hardware simulation and check the equivalence between C & RTL
cosim_design -trace_level all
