% graph 1 - pv array output
time_vals = importdata("formatted_pv_array_time.txt");
time_vals = convertCharsToStrings(time_vals);
time_vals = datetime(time_vals, 'Format', '"HH:mm:ss"');
energy_vals = importdata("formatted_pv_array_power.txt"); 

plot(time_vals, energy_vals)

