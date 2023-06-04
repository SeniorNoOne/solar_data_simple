% graph 1 and graph 2
formatString = repmat('%s', 1, 1);

time_vals_3 = importdata("time_vals_3_no_date.txt", formatString);
time_vals_3 = datetime(time_vals_3, 'Format', 'HH:mm:ss');
power_vals_3 = importdata("data_vals_3.txt"); 

time_vals_4 = importdata("time_vals_4.txt", formatString);
time_vals_4 = datetime(time_vals_4, 'Format', 'HH:mm:ss');
power_vals_4 = importdata("data_vals_4.txt"); 

figure
plot(time_vals_3, power_vals_3, "black--.", "markersize", 3)
hold on;
plot(time_vals_4, power_vals_4, "black", "markersize", 3)
xlabel("Час, год")
ylabel("P_в_и_х, Вт")
legend("Реальні дані", "Теоретична крива")
title("Потужність споживання")