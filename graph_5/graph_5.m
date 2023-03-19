% entropy input
formatString = repmat('%s', 1, 1);

ideal_time_vals = importdata("inp_ideal_time_vals.txt", formatString);
ideal_time_vals = datetime(ideal_time_vals, 'Format', 'HH:mm');
ideal_entropy = importdata("inp_ideal_entropy.txt"); 
ideal_prob = importdata("inp_ideal_prob.txt"); 

real_time_vals = importdata("inp_real_time_vals.txt", formatString);
real_time_vals = datetime(real_time_vals, 'Format', 'HH:mm:ss');
real_entropy = importdata("inp_real_entropy.txt");
real_prob = importdata("inp_real_prob.txt");

diff_time_vals = importdata("inp_diff_time_vals.txt", formatString);
diff_time_vals = datetime(diff_time_vals, 'Format', 'HH:mm');
diff_entropy = importdata("inp_diff_entropy.txt"); 


figure
plot(real_time_vals, real_prob)
hold on
plot(ideal_time_vals, ideal_prob)
legend('Реальне джерело', 'Ідеальне джерело')
xlabel("Час, год")
ylabel("p")
title("Часова залежність ймовірності")
ylim([0, 0.045])


figure
plot(real_time_vals, real_entropy)
hold on
plot(ideal_time_vals, ideal_entropy)
legend('Реальне джерело', 'Ідеальне джерело')
xlabel("Час, год")
ylabel("H")
title("Часова залежність ентропії джерела")
ylim([3.75, 4.2])


figure
plot(diff_time_vals, diff_entropy)
xlabel("Час, год")
ylabel("D")
title("Часова залежність ентропійної дивергенції джерела")


