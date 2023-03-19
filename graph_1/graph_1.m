% graph 1 - Real SP data
formatString = repmat('%s', 1, 1);

time_vals = importdata("time_vals_1.txt", formatString);
time_vals = datetime(time_vals, 'Format', 'yyyy-MM-dd HH:mm:ss');
power_vals = importdata("data_vals_1.txt"); 

fig = figure
plot(time_vals, power_vals, "--.", "markersize", 3)
xlabel("„ас, год")
ylabel("P_в_и_х, ¬т")
title("ѕотужн≥сть на виходн≥ сон€чних панелей")
saveas(fig,'graph_1.png')
