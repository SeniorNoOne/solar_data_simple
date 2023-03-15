% graph 1 - Real SP data
formatString = repmat('%s', 1, 1);

time_vals = importdata("time_vals_1.txt", formatString);
time_vals = datetime(time_vals, 'Format', 'yyyy-MM-dd HH:mm:ss');
power_vals = importdata("power_vals_1.txt"); 

figure
plot(time_vals, power_vals, "--.", "markersize", 3)
xlabel("���, ���")
ylabel("P_�_�_�, ��")
title("���������� �� ������� �������� �������")
