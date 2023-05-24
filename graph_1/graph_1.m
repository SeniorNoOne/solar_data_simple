% graph 1 - Real SP data
formatString = repmat('%s', 1, 1);

time_vals = importdata("time_vals_1.txt", formatString);
time_vals = datetime(time_vals, 'Format', 'yyyy-MM-dd HH:mm:ss');
power_vals = importdata("data_vals_1.txt"); 
power_vals_tr = importdata("power_data_vals_1.txt"); 
res_vals_tr = importdata("res_data_vals_1.txt"); 


figure
plot(time_vals, power_vals, "black--.", "markersize", 3)
hold on;
plot(time_vals, power_vals_tr, "markersize", 3)
plot(time_vals, 50 * res_vals_tr, "markersize", 3)
xlabel("„ас, год")
ylabel("P_в_и_х, ¬т")
legend("Initial data", "Truncated", "Resistance")
title("ѕотужн≥сть на виход≥ сон€чних панелей")
