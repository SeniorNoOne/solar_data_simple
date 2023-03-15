time_vals_ideal = importdata("formatted_time_file.txt");
time_vals_ideal = convertCharsToStrings(time_vals_ideal);
time_vals_ideal = datetime(time_vals_ideal, 'Format', '"HH:mm"');  
entrp_ideal = importdata("entr_inp_ideal.txt"); 


new_time_vals = importdata("filtered_pv_array_time.txt");
new_time_vals = convertCharsToStrings(new_time_vals);
new_time_vals = datetime(new_time_vals, 'Format', '"HH:mm:ss"');
prob = importdata("entr_inp.txt"); 


plot(time_vals_ideal(1:length(entrp_ideal)), entrp_ideal)
hold on
plot(new_time_vals(1:length(prob)), prob)
legend('ideal', 'real')