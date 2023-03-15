% graph 2 - ideal power curve
time_vals = importdata("formatted_time_file.txt");
time_vals = convertCharsToStrings(time_vals);
time_vals = datetime(time_vals, 'Format', '"HH:mm"');
power_vals = importdata("formatted_power_file.txt"); 

plot(time_vals, power_vals)
