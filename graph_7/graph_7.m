% entropy input
formatString = repmat('%s', 1, 1);

inp_time_vals = importdata("inp_diff_time_vals.txt", formatString);
inp_time_vals = datetime(inp_time_vals, 'Format', 'HH:mm');
inp_diff = importdata("inp_diff_entropy.txt"); 

out_time_vals = importdata("out_diff_time_vals.txt", formatString);
out_time_vals = datetime(out_time_vals, 'Format', 'HH:mm');
out_diff = importdata("out_diff_entropy.txt");

total_time_vals = importdata("total_time.txt", formatString);
total_time_vals = datetime(total_time_vals, 'Format', 'HH:mm');
total_diff = importdata("total_entropy_diff.txt");
total_relay = importdata("total_step.txt");


figure
plot(inp_time_vals, inp_diff)
hold on
plot(out_time_vals, out_diff)
xlabel("Час, год") 
ylabel("p")
legend('Ентропія джерела', 'Ентропія навантаження')
title("Часова залежність ентропії")


figure
plot(total_time_vals, total_diff, "black")
xlabel("Час, год")
ylabel("D")
title("Сигнал блоку визначення різниці")

figure
plot(total_time_vals, total_relay, "black")
xlabel("Час, год")
ylabel("R")
title("Сигнал керування релейним елементом")
ylim([-0.1, 1.1])
