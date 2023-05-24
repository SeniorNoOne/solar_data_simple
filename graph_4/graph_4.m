% graph 4 - Ideal load data
formatString = repmat('%s', 1, 1);

time_vals = importdata("time_vals_4.txt", '%s');
time_vals = datetime(time_vals, 'Format', 'HH:mm');
power_vals = importdata("data_vals_4.txt"); 

figure
plot(time_vals, power_vals, "black", "markersize", 3)     
xlabel("Час, год")
ylabel("P_н, Вт")
title("Ідеальна крива потужності навантаження")
ylim([0, 1.3 * power_vals(1)])
