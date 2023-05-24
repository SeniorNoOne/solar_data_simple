% graph 3 - Real load data
formatString = repmat('%s', 1, 1);

time_vals = importdata("time_vals_3.txt", formatString);
time_vals = datetime(time_vals, 'Format', 'yyyy/MM/dd,HH:mm:ss');
power_vals = importdata("data_vals_3.txt"); 
power_vals_tr = importdata("power_data_vals_tr_3.txt"); 
res_vals_tr = importdata("res_data_vals_3.txt"); 


figure
plot(time_vals, power_vals, "black--.", "markersize", 3)
hold on;
plot(time_vals, power_vals_tr, "markersize", 3)
xlabel("Час, год")
ylabel("P_н, Вт")
title("Потужність навантаження")
