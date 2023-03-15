% graph 4 - Ideal load data
formatString = repmat('%s', 1, 1);

time_vals = importdata("time_vals_4.txt", '%s');
time_vals = datetime(time_vals, 'Format', 'HH:mm');
power_vals = importdata("power_vals_4.txt"); 
m = mean(power_vals);

figure
plot(time_vals, ones(1, length(time_vals)) * m,  "markersize", 3)     
xlabel("Час, год")
ylabel("P_н, Вт")
title("Ідеальна крива потужності навантаженна")
ylim([0, 1.3 * m])
