% entropy input
formatString = repmat('%s', 1, 1);

ideal_time_vals = importdata("out_ideal_time_vals.txt", formatString);
ideal_time_vals = datetime(ideal_time_vals, 'Format', 'HH:mm');
ideal_entropy = importdata("out_ideal_entropy.txt"); 
ideal_prob = importdata("out_ideal_prob.txt"); 

real_time_vals = importdata("out_real_time_vals.txt", formatString);
real_time_vals = datetime(real_time_vals, 'Format', 'HH:mm:ss');
real_entropy = importdata("out_real_entropy.txt");
real_prob = importdata("out_real_prob.txt");

diff_time_vals = importdata("out_diff_time_vals.txt", formatString);
diff_time_vals = datetime(diff_time_vals, 'Format', 'HH:mm');
diff_entropy = importdata("out_diff_entropy.txt"); 


figure
plot(real_time_vals, real_prob)
hold on
plot(ideal_time_vals, ideal_prob)
xlabel("���, ���")
ylabel("p")
legend('������� ������������', '�������� ������������')
title("������ ��������� ���������")


figure
plot(real_time_vals, real_entropy, "black")
hold on
plot(ideal_time_vals, ideal_entropy, "black--")
legend('������� ������������', '�������� ������������', 'Location', 'southeast')
xlabel("���, ���")
ylabel("H")
title("������ ��������� �����ﳿ ������������")
ylim([3.5, 4.15])


figure
plot(diff_time_vals, diff_entropy, "black")
xlabel("���, ���")
ylabel("D")
title("������ ��������� ��������� ����������� ������������")
ylim([-0.05, 0.55])
