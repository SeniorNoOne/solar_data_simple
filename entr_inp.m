time_vals = importdata("formatted_pv_array_time.txt");
time_vals = convertCharsToStrings(time_vals);
time_vals = datetime(time_vals, 'Format', '"HH:mm:ss"');

new_time_vals = importdata("filtered_pv_array_time.txt");
new_time_vals = convertCharsToStrings(new_time_vals);
new_time_vals = datetime(new_time_vals, 'Format', '"HH:mm:ss"');

prob = importdata("prob_inp.txt"); 
power = importdata("formatted_pv_array_power.txt"); 
entrp = importdata("entr_inp.txt"); 

plot(time_vals, power)
hold on
plot(new_time_vals(1:length(prob)), prob * 5000)
plot(new_time_vals(1:length(entrp)), entrp * 50)
legend('power', 'prob', 'entr')

figure()
plot(new_time_vals(1:length(prob)), prob)
hold on
plot(new_time_vals(1:length(entrp)), entrp / 100)
legend('prob', 'entr')