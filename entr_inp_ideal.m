%time_vals = importdata("formatted_pv_array_time.txt");
%time_vals = convertCharsToStrings(time_vals);
%time_vals = datetime(time_vals, 'Format', '"HH:mm:ss"');

time_vals = importdata("formatted_time_file.txt");
time_vals = convertCharsToStrings(time_vals);
time_vals = datetime(time_vals, 'Format', '"HH:mm"');

prob = importdata("prob_inp_ideal.txt"); 
power = importdata("formatted_power_file.txt"); 
entrp = importdata("entr_inp_ideal.txt"); 

plot(time_vals, power)
hold on
plot(time_vals(1:length(prob)), prob * 5000)
plot(time_vals(1:length(entrp)), entrp * 50)
legend('power', 'prob', 'entr')

figure()
plot(time_vals(1:length(prob)), 100 * prob)
hold on
plot(time_vals(1:length(entrp)), entrp)
legend('prob', 'entr')