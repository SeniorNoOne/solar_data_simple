% graph 4 - Ideal load data
formatString = repmat('%s', 1, 1);

time_vals = importdata("time_vals_4.txt", '%s');
time_vals = datetime(time_vals, 'Format', 'HH:mm');
power_vals = importdata("power_vals_4.txt"); 

figure
plot(time_vals, power_vals,  "markersize", 3)     
xlabel("���, ���")
ylabel("P_�, ��")
title("�������� ����� ��������� ������������")
ylim([0, 1.3 * power_vals(1)])
