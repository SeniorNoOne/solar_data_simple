% entropy input
formatString = repmat('%s', 1, 1);

inp_time_vals = importdata("inp_diff_data_time_vals.txt", formatString);
inp_time_vals = datetime(inp_time_vals, 'Format', 'HH:mm');
inp_diff = importdata("inp_diff_entropy.txt"); 

out_time_vals = importdata("out_diff_data_time_vals.txt", formatString);
out_time_vals = datetime(out_time_vals, 'Format', 'HH:mm');
out_diff = importdata("out_diff_entropy.txt");

total_time_vals = importdata("total_entropy_time.txt", formatString);
total_time_vals = datetime(total_time_vals, 'Format', 'HH:mm');
total_diff = importdata("total_entropy_diff.txt");
total_relay = importdata("total_step.txt");


figure
plot(inp_time_vals, inp_diff)
hold on
plot(out_time_vals, out_diff)
legend('Ідеальна крива', 'Реальна крива')
xlabel("Час, год")
ylabel("p")
title("Часова залежність ймовірності")


figure
plot(total_time_vals, total_diff)
hold on
plot(total_time_vals, total_relay)
legend('Ентропійна дивергенція', 'Релейний сигнал')
xlabel("Час, год")
ylabel("p")
