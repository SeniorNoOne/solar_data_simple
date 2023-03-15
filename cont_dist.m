time_vals = importdata("formatted_household_datetime.txt");
time_vals = convertCharsToStrings(time_vals);
time_vals = datetime(time_vals, 'Format', '"HH:mm:ss"');

energy_vals = importdata("formatted_household_energy.txt"); 

len = length(time_vals);
val = mean(energy_vals);
level = val * ones(len, 1);

plot(time_vals, level)
