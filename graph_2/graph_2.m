% graph 2 - Ideal SP curve
% data obtained manually
formatString = repmat('%s', 1, 1);

time_vals = importdata("time_vals_2.txt", formatString);
time_vals = datetime(time_vals, 'Format', 'HH:mm');
power_vals = importdata("data_vals_2.txt"); 

figure
plot(time_vals, power_vals, "--.", "markersize", 3)
xlabel("„ас, год")
ylabel("P_в_и_х, ¬т")
title("≤деальна крива потужност≥ на виходн≥ сон€чних панелей")
