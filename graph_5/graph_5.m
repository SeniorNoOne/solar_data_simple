% entropy input
formatString = repmat('%s', 1, 1);

ideal_time_vals = importdata("inp_ideal_data_time_vals.txt", formatString);
ideal_time_vals = datetime(ideal_time_vals, 'Format', 'HH:mm');
ideal_entropy = importdata("inp_ideal_data_entropy.txt"); 
ideal_prob = importdata("inp_ideal_data_prob.txt"); 

real_time_vals = importdata("inp_real_data_time_vals.txt", formatString);
real_time_vals = datetime(real_time_vals, 'Format', 'HH:mm:ss');
real_entropy = importdata("inp_real_data_entropy.txt");
real_prob = importdata("inp_real_data_prob.txt");

diff_time_vals = importdata("inp_diff_data_time_vals.txt", formatString);
diff_time_vals = datetime(diff_time_vals, 'Format', 'HH:mm');
diff_entropy = importdata("inp_diff_entropy.txt"); 


figure
plot(real_time_vals, real_prob)
hold on
plot(ideal_time_vals, ideal_prob)
legend('������� �������', '�������� �������')
xlabel("���, ���")
ylabel("p")
title("������ ���������� ���������")


figure
plot(real_time_vals, real_entropy)
hold on
plot(ideal_time_vals, ideal_entropy)
legend('������� �������', '�������� �������')
xlabel("���, ���")
ylabel("H")
title("������ ���������� �����ﳿ �������")


figure
plot(diff_time_vals, diff_entropy)
xlabel("���, ���")
ylabel("D")
title("������ ���������� ��������� ����������� �������")


