% graph 2 - Ideal SP curve
% data obtained manually
formatString = repmat('%s', 1, 1);

time_vals = importdata("time_vals_2.txt", formatString);
time_vals = datetime(time_vals, 'Format', 'HH:mm');
power_vals = importdata("data_vals_2.txt"); 

figure
plot(time_vals, power_vals, "--.", "markersize", 3)
xlabel("���, ���")
ylabel("P_�_�_�, ��")
title("�������� ����� ��������� �� ������ �������� �������")
