% ideal power curve
time_vals = importdata("formatted_household_datetime.txt");
time_vals = convertCharsToStrings(time_vals);
time_vals = datetime(time_vals, 'Format', '"HH:mm:ss"');
energy_vals = importdata("formatted_household_energy.txt"); 

plot(time_vals, energy_vals * 6)
hold on

