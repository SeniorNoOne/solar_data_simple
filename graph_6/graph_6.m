% entropy input
formatString = repmat('%s', 1, 1);

ideal_time_vals = importdata("out_ideal_data_time_vals.txt", formatString);
ideal_time_vals = datetime(ideal_time_vals, 'Format', 'HH:mm');
ideal_entropy = importdata("out_ideal_data_entropy.txt"); 
ideal_prob = importdata("out_ideal_data_prob.txt"); 

real_time_vals = importdata("out_real_data_time_vals.txt", formatString);
real_time_vals = datetime(real_time_vals, 'Format', 'HH:mm:ss');
real_entropy = importdata("out_real_data_entropy.txt");
real_prob = importdata("out_real_data_prob.txt");

diff_time_vals = importdata("out_diff_data_time_vals.txt", formatString);
diff_time_vals = datetime(diff_time_vals, 'Format', 'HH:mm');
diff_entropy = importdata("out_diff_entropy.txt"); 


figure
plot(real_time_vals, real_prob)
hold on
plot(ideal_time_vals, ideal_prob)
legend('Ідеальна крива', 'Реальна крива')
xlabel("Час, год")
ylabel("p")
title("Часова залежність ймовірності")


figure
plot(ideal_time_vals, ideal_entropy)
hold on
plot(real_time_vals, real_entropy)
legend('Ідеальна крива', 'Реальна крива')
xlabel("Час, год")
ylabel("H")
title("Часова залежність ентропії навантаження")


figure
plot(diff_time_vals, diff_entropy)
xlabel("Час, год")
ylabel("D")
title("Часова залежність ентропії навантаження")
