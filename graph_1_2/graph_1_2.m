% graph 1 and graph 2
formatString = repmat('%s', 1, 1);

time_vals_1 = importdata("time_vals_1_no_date.txt", formatString);
time_vals_1 = datetime(time_vals_1, 'Format', 'HH:mm:ss');
power_vals_1 = importdata("data_vals_1.txt"); 

time_vals_2 = importdata("time_vals_2.txt", formatString);
time_vals_2 = datetime(time_vals_2, 'Format', 'HH:mm');
power_vals_2 = importdata("data_vals_2.txt"); 

figure
plot(time_vals_1, power_vals_1, "black--.", "markersize", 3)
hold on;
plot(time_vals_2, power_vals_2, "black", "markersize", 3)
xlabel("Час, год")
ylabel("P_в_и_х, Вт")
legend("Реальні дані", "Теоретична крива")
title("Потужність на виході сонячних панелей")